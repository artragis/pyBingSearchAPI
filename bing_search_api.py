# coding: utf-8
'''
This is designed for the new Azure Marketplace Bing Search API (released Aug 2012)

Inspired by https://github.com/mlagace/Python-SimpleBing and 
http://social.msdn.microsoft.com/Forums/pl-PL/windowsazuretroubleshooting/thread/450293bb-fa86-46ef-be7e-9c18dfb991ad
'''

import requests
from SearchSources.sources import WebSearch, ImageSearch, VideoSearch, SpellingSearch, RelatedSearch, \
    NewsSearch, CompositeSearch, JSON_RESPONSE, XML_RESPONSE

class BingSearchAPI():
    
    def __init__(self, key):
        self.key = key

    def image(self):
        return ImageSearch()

    def web(self):
        return WebSearch()

    def video(self):
        return VideoSearch()

    def related(self):
        return RelatedSearch()

    def spell(self):
        return SpellingSearch()

    def news(self):
        return NewsSearch()

    def composite(self, sources):
        """

        :param sources: a list with all sources you want in "web", "image", "video", "news", "spell"
        :return: a composite search source
        """
        return CompositeSearch("web" in sources, "image" in sources, "video" in sources,
                               "news" in sources, "spell" in sources)

    def search(self, source):
        """
        :param source: SearchSource well configured
        :return: the result as "Response" object
        """
        request = source.build_query()
        return requests.get(request, auth=(self.key, self.key))
 

