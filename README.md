Pocket-API
=======================

This package provides a wrapper class around [GetPocket](http://getpocket.com) V3 APIs.

Installation
------------

		pip install pocket-api

Usage
--------

	from pocket import Pocket, PocketException


	p = Pocket(
		consumer_key='51178-761fe72fba8f7c8db74c6d56', 
		access_token='f33bdcb3-2c7d-6dbe-6dbb-4f109d'
	)
	
	# Fetch a list of articles
	try:
    	print(p.retrieve(offset=0, count=10))
	except PocketException as e:
    	print(e.message)
    
    # Add an article
    p.add('https://pymotw.com/3/asyncio/')	
	
	# Start a bulk operation and commit
	p.archive(1186408060).favorite(1188103217).tags_add(
		1168820736, 'Python'
	).tags_add(
		1168820736, 'Web Development'
	).commit()


Bulk Actions
------------
1. bulk_add
2. archive
3. readd
4. favorite
5. unfavorite
6. delete
7. tags_add
8. tags_remove
9. tags_replace
10. tags_clear
11. tag_rename


The class also provides a ```reset``` method to restart bulk operations at anytime and a ```commit``` method to perform the bulk request to pocket's APIs.
