Pocket-API
=======================

[![Build Status](https://travis-ci.org/rakanalh/pocket-api.svg?branch=master)](https://travis-ci.org/rakanalh/pocket-api)

This package provides a wrapper class around [GetPocket](http://getpocket.com) V3 APIs.

Pocket-CLI
----------

You can checkout [pocket-cli](https://www.github.com/rakanalh/pocket-cli), which is an application for reading / listing /managing your pocket articles from the terminal

Installation
------------

		pip install pocket-api

Usage
--------

First, you have to [Create your consumer key](https://getpocket.com/developer/apps/new) from getpocket's developer console. To get the access token, you have to authorize the app on your own account. There are tools on the web that can automate this for you such as [fxneumann's OneClickPocket](http://reader.fxneumann.de/plugins/oneclickpocket/auth.php)

	from pocket import Pocket, PocketException


	p = Pocket(
		consumer_key='<Your Consumer Key>',
		access_token='<Your Access Token>'
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


Methods
-------

* Add an article

		add(url, title, tags, tweet_id)

* Retrieve articles

	    retrieve(state, favorite, tag, contentType,
                 sort, detailType, search, domain,
                 since, count, offset)

Bulk Actions
------------
* Add an article to bulktime_of_action

		bulk_add(item_id, ref_id, tags, time_of_action, title, url)

* Archive article

	    archive(item_id, time_of_action)

* Reread an article

	    readd(item_id, time_of_action)

* Mark article as favorite

	    favorite(item_id, time_of_action)

* Remove favorite mark from article

	    unfavorite(item_id, time_of_action)

* Delete an article from list

	    delete(item_id, time_of_action)

* Add tag to article

	    tags_add(item_id, tags, time_of_action)

* Remove tag from article

	    tags_remove(item_id, tags, time_of_action)

* Replace tags on article

	    tags_replace(item_id, tags, time_of_action)

* Clear tags from article

	    tags_clear(item_id, time_of_action)

* Rename a tag

	    tag_rename(old_tag, new_tag, time_of_action)

* Reset bulk actions (removes all previously registered actions)

	    reset()

* Send request of all bulk items to getpocket

	    commit()
