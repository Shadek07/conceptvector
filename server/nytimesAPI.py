
# coding: utf-8

# # New York Times API 
# 
# ## API Key
#  - community API key
#    - 0292ebefdcaf75b2fb0d7e7d1404cf09:10:71572358
#  - Article Search API key
#    - c473062c4108d294756e7b3ebf2b318c:9:71572358
#  - Most Popular API key
#    - 3971a4b7969eb05ae3959d0747e76a04:13:71572358
#    
# 
# ## Reference 
#  - http://developer.nytimes.com/apps/mykeys
#  - http://docs.python-requests.org/en/master/
#  
# 

# In[37]:

import requests
from time import sleep
import pickle
from sqlalchemy import create_engine
from models import Article, Comment
from sqlalchemy.orm import sessionmaker
import pdb


# Most popular API
# Get most popular articles from last 30 days

article_file_name = 'data/most_popular_articles.pkl'
comment_file_name = 'data/comments.pkl'
engine = create_engine('postgresql://localhost/conceptvector_dev',echo=False)
Session = sessionmaker(bind=engine)
session = Session()
cache = False


def download_articles():
	offset = 0
	apikey = '3971a4b7969eb05ae3959d0747e76a04:13:71572358'

	payload = {'api-key':apikey, 'offset': offset}
	url = 'http://api.nytimes.com/svc/mostpopular/v2/mostviewed/all-sections/30.json'

	most_popular_request = requests.get(url, params=payload)
	num_results = most_popular_request.json()['num_results']
	most_popular_articles = most_popular_request.json()['results']

	for offset in range(20,num_results,20):
	    payload = {'api-key':apikey, 'offset': offset}
	    most_popular_request = requests.get(url, params=payload)
	    most_popular_articles += most_popular_request.json()['results']
	    sleep(0.2)
	    
	if len(most_popular_articles) != num_results:
		print "Error: Articles number does not match"

	output = file(article_file_name,'wb')
	pickle.dump(most_popular_articles, output)

# Now Add these articles into Database

def add_articles_database():

	input = file(article_file_name,'rb')
	most_popular_articles = pickle.load(input)

	for a in most_popular_articles:
		if a['id'] > 10000:
			if session.query(Article).filter_by(id=a['id']).count() == 0:
				print a['url']
				aquery = Article(a)
				try:
					session.add(aquery)
					download_add_comments(a)
					session.commit()
				except Exception as e:
					pdb.set_trace()
					session.rollback()
					print a['id']
					print e


def add_replies(all, node, stacklevel):

	all.append(node)
    
	for n in node['replies']:
		add_replies(all, n, stacklevel+1 )
    
    
def download_add_comments(a):
	article_url = a['url']
	apikey = '0292ebefdcaf75b2fb0d7e7d1404cf09:10:71572358'
	payload = {'api-key': apikey, 'url': article_url, 'replyLimit': 10000}
	url = 'http://api.nytimes.com/svc/community/v3/user-content/url.json'

	try:

		comment_request = requests.get(url, params=payload)
		num_parent_results = comment_request.json()['results']['totalParentCommentsFound']
		num_results = comment_request.json()['results']['totalCommentsFound']
		comments = comment_request.json()['results']['comments']
		output = file(comment_file_name,'rb')

		if cache:
			output = file(comment_file_name,'rb')
			commments = pickle.load(output)

		else:
			for offset in range(25,num_parent_results,25):
			    payload = {'api-key':apikey, 'offset': offset, 'url':article_url , 'replyLimit': 1000}
			    comment_request = requests.get(url, params=payload)

			    while (comment_request.status_code != requests.codes.ok):
			    	print 'Retrying Download', comment_request.status_code, article_url
			    	print comment_request.text
			    	sleep(1)
			    	comment_request = requests.get(url, params=payload)
			    	 

			    comments += comment_request.json()['results']['comments']
			    sleep(0.1)

			if len(comments) != num_parent_results:
				# pdb.set_trace()
				print "Error: Parent Comments number does not match",  a['url'], len(comments), num_parent_results

			
			output = file(comment_file_name,'wb')
			pickle.dump(comments, output)
			output.close()
		
		all_comments = []
		for c in comments:
			add_replies(all_comments, c, 0)

		if len(all_comments) != num_results:
			# pdb.set_trace()
			print "Error: All Comments number does not match", a['url'], len(all_comments), num_results

	except Exception as e:
		pdb.set_trace()
		print e

	for c in all_comments:
		cquery = Comment(c)
		try:
			
			if session.query(Comment).filter_by(commentID=cquery.commentID).count() == 0:
				session.add(cquery)
		except Exception as e:
			pdb.set_trace()
			session.rollback()
			print a['commentID']
			print e 








add_articles_database()