
XML_RESPONSE = 'atom'
JSON_RESPONSE = 'json'
NO_ADULT_FILTERING = "Off"
MODERATE_ADULT_FILTERING = "Moderate"
STRICT_ADULT_FILTERING = "Strict"

class SearchSource():
    """This class represent the very basis of a search source. It
        also implements the filters which are used in every source"""

    # dictionary that will store the filters in the "filter":"value" format
    # values are not yet url encoded
    _filters = {}
    _url = "https://api.datamarket.azure.com/Data.ashx/Bing/Search/v1/"
    _format = JSON_RESPONSE
    _first_query_char = '?'
    def query(self, query):
        """The search query as a raw data that can be represented as string"""
        self._filters['Query'] = "'" + query + "'" #query must be wrapped by quotes
        return self

    def take(self, number_of_result):
        """Specifies the number of results to return.
        The default is 50 for Web, Image, and Video searches, 15 for News."""
        self._filters['$top'] = number_of_result
        return  self

    def skip(self, offset):
        """Specifies the starting point offset for the results. The default is zero."""
        self._filters['$skip'] = offset
        return self

    def format(self, format):
        """Define the expected response format. Use the XML_RESPONSE and JSON_RESPONSE to specify it.
            Default is JSON_RESPONSE"""

        assert format == XML_RESPONSE or format == JSON_RESPONSE
        self._format = format
        self._filters['$format'] = format
        return self

    def adult(self, level):
        """Explicitely fix the adult filtering level. This can prevent getting sexual content.
            If no adult filtering is provided, Bing API will try to guess the user's country and apply its
            default filtering level"""
        assert level == NO_ADULT_FILTERING or level == MODERATE_ADULT_FILTERING or level == STRICT_ADULT_FILTERING
        self._filters['Adult'] = level
        return self

    def geolocate(self, latitude, longitude):
        """geolocate your query"""
        self._filters['Latitude'] = float(latitude)
        self._filters['Longitude'] = float(longitude)
        return self

    def for_market(self, market):
        """
            specify the "market" (basicaly the country) concerned by the query
            this is specialy useful when you want to force one market even if your user is abroad
            or if you want to use some us-only features
        """
        self._filters['Market'] = market
        return self

    def enable_highlighting(self):
        """
        Bing will use a special character to identify the beginning and the end of
        a query term that appears in results. For more information, see Hit Highlighting on the MSDN website.
        """
        if "Options" in self._filters:
            self._filters['Option'] += '+EnableHighlighting'
        else:
            self._filters['Option'] = 'EnableHighlighting'
        return self

    def disable_location_detection(self):
        """
        Prevents Bing from inferring location from the terms of a query.
        """
        if "Options" in self._filters:
            self._filters['Option'] += '+DisableLocationDetection'
        else:
            self._filters['Option'] = 'DisableLocationDetection'
        return self

    def replace_symbols(self, request):
        """ Custom urlencoder.
         They specifically want %27 as the quotation which is a single quote '
         We're going to map both ' and " to %27 to make it more python-esque
        """""
        request = request.replace("'", '%27')
        request = request.replace('"', '%27')
        request = request.replace('+', '%2b')
        request = request.replace( ' ', '%20')
        request = request.replace(':', '%3a')
        return request

    def build_query(self):
        final_url = ""
        i = 0
        for key,value in self._filters.items():
            if i == 0:
                final_url += self._first_query_char
                i += 1
            else:
                final_url += '&'
            final_url += key + '=' + str(value)
        return self._url + self.replace_symbols(final_url)



class WebSearch(SearchSource):

    def __init__(self):
        self._url += "Web"


class ImageSearch(SearchSource):

    def __init__(self):
        self._url += "Image"


class VideoSearch(SearchSource):

    def __init__(self):
        self._url += "Video"


class NewsSearch(SearchSource):

    def __init__(self):
        self._url += "News"


class SpellingSearch(SearchSource):

    def __init__(self):

        self._url += "SpellingSuggestion"

class RelatedSearch(SearchSource):

    def __init__(self):
        self._url += "RelatedSearch"


class CompositeSearch(WebSearch, ImageSearch, VideoSearch, NewsSearch, SpellingSearch):

    def __init__(self, web = True, image = False, video = False, news = False, spell = False ):
        sources = ""

        if web:
            sources += "web+"
        if image:
            sources += "image+"
        if video:
            sources += "video+"
        if news:
            sources += "news"
        if spell:
            sources += "spell"

        self._url = "https://api.datamarket.azure.com/Data.ashx/Bing/Search/v1/Composite?Sources="+sources
        self._first_query_char = '&'