XML_RESPONSE = 'atom'
JSON_RESPONSE = 'json'
NO_ADULT_FILTERING = "Off"
MODERATE_ADULT_FILTERING = "Moderate"
STRICT_ADULT_FILTERING = "Strict"
SHORT_VID = 300
MEDIUM_VID = 12000
LONG_VID = 42000

class SearchSource():
    """This class represent the very basis of a search source. It
        also implements the filters which are used in every source"""

    # dictionary that will store the filters in the "filter":"value" format
    # values are not yet url encoded
    _filters = {}
    _url = "https://api.datamarket.azure.com/Data.ashx/Bing/Search/v1/"
    _format = JSON_RESPONSE
    _first_query_char = '?'

    def __init__(self):
        self.format(JSON_RESPONSE)

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

    def _replace_symbols(self, request):
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
        return self._url + self._replace_symbols(final_url)



class WebSearch(SearchSource):

    def __init__(self):
        self._url += "Web"


class ImageSearch(SearchSource):
    _image_filters = {}
    def __init__(self):
        self._url += "Image"

    def _build_image_filters(self):
        temp = "+".join(key + ":" + value for (key, value) in self._image_filters)
        self._filters['ImageFilters'] = "'" + temp + "'"

    def large(self):
        """Select only large size image"""
        self._image_filters['Size'] = "Large"
        self._build_image_filters()
        return self

    def medium(self):
        """Select only medium size image"""
        self._image_filters['Size'] = "Medium"
        self._build_image_filters()
        return self

    def small(self):
        """Select only small image"""
        self._image_filters['Size'] = "Small"
        self._build_image_filters()
        return self

    def width(self, width):
        self._image_filters['Size'] = "Width:" + str(width)
        self._build_image_filters()
        return self

    def height(self, height):
        self._image_filters['Size'] = "Height:" + str(height)
        self._build_image_filters()
        return self

    def square(self):
        """Select only image whose aspect is square (width = height) if no aspect is specified this is used by
        default"""
        self._image_filters['Aspect'] = "Square"
        self._build_image_filters()
        return self

    def widescreen(self):
        """Select only image whose aspect is widescreen (landscape)"""
        self._image_filters['Aspect'] = "Wide"
        self._build_image_filters()
        return self

    def tall(self):
        """Select only image whose aspect is in tall ration (portrait)"""
        self._image_filters['Aspect'] = "Tall"
        self._build_image_filters()
        return self

    def isColorized(self, colorized = True):
        """
        filter the image by chosing only colorized (colorized = True) or Monochrome (colorized = False)
        :param colorized:
        :return:
        """
        if colorized:
            self._image_filters['Color'] = "Color"
        else:
            self._image_filters['Color'] = "Monochrome"
        self._build_image_filters()
        return self

    def photo(self):
        """
        Select only photos
        """
        self._image_filters['Style'] = "Photo"
        self._build_image_filters()
        return self

    def illustration(self):
        """
        Select graphics or illustrations
        """
        self._image_filters['Style'] = "Graphics"
        self._build_image_filters()
        return self

    def head_only(self):
        """get photos with head only (without shoulders, body...)"""
        self._image_filters['Face'] = "Face"
        self._build_image_filters()
        return self

    def head_and_shoulder(self):
        """get photos with portrait of head + shoulders"""
        self._image_filters['Face'] = "Portrait"
        self._build_image_filters()
        return self

    def any_subject(self):
        """get photos with faces but without any other restriction about the body, the landscape...)"""
        self._image_filters['Face'] = "Other"
        self._build_image_filters()
        return self


class VideoSearch(SearchSource):

    _video_filters = {}

    def __init__(self):
        self._url += "Video"

    def _build_video_filters(self):
        temp = "+".join(key + ":" + value for (key, value) in self._video_filters)
        self._filters['VideoFilters'] = "'" + temp + "'"

    def low_resolution(self):
        """Select only low resolution video"""
        self._video_filters['Resolution'] = "Low"
        self._build_video_filters()
        return self

    def standard_resolution(self):
        """Select only stantard resolution video"""
        self._video_filters['Resolution'] = "Medium"
        self._build_video_filters()
        return self

    def high_resolution(self):
        """Select only high resolution video"""
        self._video_filters['Resolution'] = "High"
        self._build_video_filters()
        return self

    def duration(self, seconds):
        """
        Select video by eliminating too short or too long vid
        :param seconds: The number of second the video has to have. Please use LONG_VID, MEDIUM_VID and SHORT_VID
        :return:
        """
        if seconds <= SHORT_VID:
            self._video_filters['Duration'] = "Short"
        elif seconds <= MEDIUM_VID:
            self._video_filters['Duration'] = "Medium"
        else:
            self._video_filters['Duration'] = "Long"
        self._build_video_filters()
        return self

    def standard_aspect(self):
        """Select video of standard aspect ratio."""
        self._video_filters['Aspect'] = "Standard"
        self._build_video_filters()
        return self

    def widescreen_aspect(self):
        """Select vidoes with widescreen aspect ratio."""
        self._video_filters['Aspect'] = "Wide"
        self._build_video_filters()
        return self

    def order_by_relevance(self):
        """Sort videos by relevance from the query (most to least relevant)"""
        self._filters['VideoSortBy'] = "Relevance"
        return self

    def order_by_date(self):
        """Sort videos by chronilogical order (older to newer)"""
        self._filters['VideoSortBy'] = "Date"



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
        sources = "%27"
        sources_list = []
        if web:
            sources_list.append("web")
        if image:
            sources_list.append("image")
        if video:
            sources_list.append("video")
        if news:
            sources_list.append("news")
        if spell:
            sources_list.append("spell")

        sources += "%2B".join(sources_list) + "%27"
        self._url = "https://api.datamarket.azure.com/Data.ashx/Bing/Search/v1/Composite?Sources="+sources
        self._first_query_char = '&'