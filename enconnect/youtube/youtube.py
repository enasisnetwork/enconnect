"""
Functions and routines associated with Enasis Network Remote Connect.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Literal
from typing import Optional
from typing import TYPE_CHECKING
from typing import get_args

from httpx import Response

from .models import RESULT_KINDS
from .models import YouTubeResult
from .models import YouTubeVideo
from ..utils import HTTPClient
from ..utils.http import _PAYLOAD

if TYPE_CHECKING:
    from .params import YouTubeParams



_RESULT_KINDS = [
    f'youtube#{x}' for x in
    get_args(RESULT_KINDS)]



class YouTube:
    """
    Interact with the cloud service API with various methods.

    :param params: Parameters used to instantiate the class.
    """

    __params: 'YouTubeParams'
    __client: HTTPClient


    def __init__(
        self,
        params: 'YouTubeParams',
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        self.__params = params

        client = HTTPClient(
            timeout=params.timeout,
            verify=params.ssl_verify,
            capem=params.ssl_capem)

        self.__client = client


    @property
    def params(
        self,
    ) -> 'YouTubeParams':
        """
        Return the Pydantic model containing the configuration.

        :returns: Pydantic model containing the configuration.
        """

        return self.__params


    @property
    def client(
        self,
    ) -> HTTPClient:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.__client


    def request_block(
        self,
        method: Literal['get'],
        path: str,
        params: Optional[_PAYLOAD] = None,
    ) -> Response:
        """
        Return the response for upstream request to the server.

        :param method: Method for operation with the API server.
        :param path: Path for the location to upstream endpoint.
        :param params: Optional parameters included in request.
        :returns: Response from upstream request to the server.
        """

        params = dict(params or {})

        server = 'www.googleapis.com'
        client = self.__client

        params['key'] = (
            self.__params.token)

        location = (
            f'https://{server}/'
            f'youtube/v3/{path}')

        request = client.request_block

        return request(
            method=method,
            location=location,
            params=params)


    async def request_async(
        self,
        method: Literal['get'],
        path: str,
        params: Optional[_PAYLOAD] = None,
    ) -> Response:
        """
        Return the response for upstream request to the server.

        :param method: Method for operation with the API server.
        :param path: Path for the location to upstream endpoint.
        :param params: Optional parameters included in request.
        :returns: Response from upstream request to the server.
        """

        params = dict(params or {})

        server = 'www.googleapis.com'
        client = self.__client

        params['key'] = (
            self.__params.token)

        location = (
            f'https://{server}/'
            f'youtube/v3/{path}')

        request = client.request_async

        return await request(
            method=method,
            location=location,
            params=params)


    def search(
        # NOCVR
        self,
        params: Optional[_PAYLOAD] = None,
    ) -> list[YouTubeResult]:
        """
        Return the results from the provided search parameters.

        :param params: Optional parameters included in request.
        :returns: Results from the provided search parameters.
        """

        return self.search_block(params)


    def search_block(
        self,
        params: Optional[_PAYLOAD] = None,
    ) -> list[YouTubeResult]:
        """
        Return the results from the provided search parameters.

        :param params: Optional parameters included in request.
        :returns: Results from the provided search parameters.
        """

        params = dict(params or {})


        if 'maxResults' not in params:
            params['maxResults'] = 50

        if 'order' not in params:
            params['order'] = 'date'

        if 'part' not in params:
            params['part'] = 'snippet,id'


        request = self.request_block

        response = request(
            'get', 'search', params)

        response.raise_for_status()

        fetched = response.json()

        assert isinstance(fetched, dict)


        return [
            YouTubeResult(**x)
            for x in fetched['items']
            if x['id']['kind']
            in _RESULT_KINDS]


    async def search_async(
        self,
        params: Optional[_PAYLOAD] = None,
    ) -> list[YouTubeResult]:
        """
        Return the results from the provided search parameters.

        :param params: Optional parameters included in request.
        :returns: Results from the provided search parameters.
        """

        params = dict(params or {})


        if 'maxResults' not in params:
            params['maxResults'] = 50

        if 'order' not in params:
            params['order'] = 'date'

        if 'part' not in params:
            params['part'] = 'snippet,id'


        request = self.request_async

        response = await request(
            'get', 'search', params)

        response.raise_for_status()

        fetched = response.json()

        assert isinstance(fetched, dict)


        return [
            YouTubeResult(**x)
            for x in fetched['items']
            if x['id']['kind']
            in _RESULT_KINDS]


    def videos(
        # NOCVR
        self,
        params: Optional[_PAYLOAD] = None,
    ) -> list[YouTubeVideo]:
        """
        Return the videos from the provided search parameters.

        :param params: Optional parameters included in request.
        :returns: Results from the provided search parameters.
        """

        return self.videos_block(params)


    def videos_block(
        self,
        params: Optional[_PAYLOAD] = None,
    ) -> list[YouTubeVideo]:
        """
        Return the videos from the provided search parameters.

        :param params: Optional parameters included in request.
        :returns: Results from the provided search parameters.
        """

        params = dict(params or {})


        if 'maxResults' not in params:
            params['maxResults'] = 50

        if 'order' not in params:
            params['order'] = 'date'

        if 'part' not in params:
            params['part'] = 'snippet,id'


        request = self.request_block

        response = request(
            'get', 'videos', params)

        response.raise_for_status()

        fetched = response.json()

        assert isinstance(fetched, dict)


        return [
            YouTubeVideo(**x)
            for x in fetched['items']]


    async def videos_async(
        self,
        params: Optional[_PAYLOAD] = None,
    ) -> list[YouTubeVideo]:
        """
        Return the videos from the provided search parameters.

        :param params: Optional parameters included in request.
        :returns: Results from the provided search parameters.
        """

        params = dict(params or {})


        if 'maxResults' not in params:
            params['maxResults'] = 50

        if 'order' not in params:
            params['order'] = 'date'

        if 'part' not in params:
            params['part'] = 'snippet,id'


        request = self.request_async

        response = await request(
            'get', 'videos', params)

        response.raise_for_status()

        fetched = response.json()

        assert isinstance(fetched, dict)


        return [
            YouTubeVideo(**x)
            for x in fetched['items']]


    def video_block(
        self,
        unique: str,
    ) -> YouTubeVideo:
        """
        Return the specific content within the social platform.

        :param unique: Unique identifier within social platform.
        :returns: Specific content within the social platform.
        """

        videos = self.videos_block(
            {'id': unique})

        return videos[0]


    async def video_async(
        self,
        unique: str,
    ) -> YouTubeVideo:
        """
        Return the specific content within the social platform.

        :param unique: Unique identifier within social platform.
        :returns: Specific content within the social platform.
        """

        videos = await (
            self.videos_async({
                'id': unique}))

        return videos[0]
