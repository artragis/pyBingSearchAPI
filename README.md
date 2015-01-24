pyBingSearchAPI
===============

Python Bing Search API for new Azure Marketplace version (Aug 2012 release)

Inspired by https://github.com/mlagace/Python-SimpleBing (designed for outdated Bing API 2.0),
this class basically encodes your query parameters as a url request 
but also makes sure the parameters are in the right order, 
case is correct for the mandatory parameters, and quotes are added.
Details are in the source comments.

To use:
Get your API key from http://www.bing.com/developers/

For the Bing Search API schema, go to http://www.bing.com/developers/
Click on Bing Search API, then download the Bing API Schema Guide (which is oddly a Word document)

The parameters are just accepted as a dictionary. 
Note from the documentation quotations are required for some filters.
I've mapped both " and ' to be the desired urlencoding to make it more python-esque

Example:

    from bing_search_api import BingSearchAPI
    
    my_key = "[your key]"
    query_string = "Gandalf"
    bing = BingSearchAPI(my_key)
    # prepare
    query = bing.image().large().photo().take(25).skip(0) # will take the 25 first large photos
    # execute
    result = bing.search(query) # result is a well parsed json
