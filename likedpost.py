import facebook
import requests
import json
import re
def likescount(post,graph):
	count = 0
	id = post['id']
	if 'likes' in post:
		likes = post['likes']
		while(True):
			count = count + len(likes['data'])
			if 'paging' in likes and 'after' in likes['paging']['cursors']:
				likes = graph.get_connections(id,'likes',after = likes['paging']['cursors']['after'])
			else:
				break 
		return count
	else:
		return 0
		
token = raw_input("Enter your access token:")
limit = int(raw_input("Enter the number of posts you want to scan(enter in multiples of 10):"))
graph = facebook.GraphAPI(token)
posts = graph.get_connections('me','posts',limit=10)
count = 0
mx = 0
plink = ""
while(True):
	for post in posts['data']:
		count = count + 1
		likecnt = likescount(post,graph)
		if(likecnt > mx):
			mx = likecnt
			plink = post['actions'][0]['link']
	if(count >= limit): #the number  of posts you want to scan from begining
		break
	if('paging' in posts and 'next' in posts['paging']):
		match = re.search(r'.+until=([\w]+)&__paging_token=[\w+]',posts['paging']['next'])
		posts = graph.get_connections('me','posts',until = match.group(1))
	else:
		break
print plink

