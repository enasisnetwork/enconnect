"""
Functions and routines associated with Enasis Network Remote Connect.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Any
from typing import Literal
from typing import Optional
from typing import TYPE_CHECKING
from typing import get_args

from pydantic import BaseModel

from requests import Response
from requests import request

if TYPE_CHECKING:
    from .params import YouTubeParams



RESULT_KINDS = Literal[
    'channel',
    'playlist',
    'video']

_RESULT_KINDS = [
    f'youtube#{x}' for x in
    get_args(RESULT_KINDS)]



RESULT_VALUE = {
    'channelId': 'channel',
    'channelTitle': 'channel_title',
    'description': 'about',
    'publishedAt': 'published',
    'thumbnails': 'thumbnail',
    'title': 'title'}

RESULT_BASIC = {
    'channelId': 'channel',
    'kind': 'kind',
    'playlistId': 'playlist',
    'videoId': 'video'}



class YouTubeResult(BaseModel, extra='ignore'):
    """
    Contains information returned from the upstream response.

    :param data: Keyword arguments passed to Pydantic model.
        Parameter is picked up by autodoc, please ignore.
    """

    kind: RESULT_KINDS

    channel: Optional[str] = None
    playlist: Optional[str] = None
    video: Optional[str] = None

    title: str
    about: Optional[str] = None
    channel_title: Optional[str] = None
    thumbnail: str
    published: str


    def __init__(
        self,
        **data: Any,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """


        basic = data.get('id', {})

        items = RESULT_BASIC.items()

        for old, new in items:

            value = basic.get(old)

            if value is None:
                continue

            data[new] = value


        match = data.get('snippet', {})

        items = RESULT_VALUE.items()

        for old, new in items:

            value = match.get(old)

            if value is None:
                continue  # NOCVR

            data[new] = value


        if 'thumbnail' in data:
            data['thumbnail'] = (
                data['thumbnail']
                ['high']['url'])


        data['kind'] = data['kind'][8:]


        super().__init__(**data)



class YouTube:
    """
    Interact with the cloud service API with various methods.

    :param params: Parameters for instantiating the instance.
    """

    __params: 'YouTubeParams'


    def __init__(
        self,
        params: 'YouTubeParams',
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        self.__params = params


    @property
    def params(
        self,
    ) -> 'YouTubeParams':
        """
        Return the Pydantic model containing the configuration.

        :returns: Pydantic model containing the configuration.
        """

        return self.__params


    def request(
        self,
        method: str,
        path: str,
        params: Optional[dict[str, Any]] = None,
    ) -> Response:
        """
        Return the response for upstream request to the server.

        :param method: Method for operation with the API server.
        :param path: Path for the location to upstream endpoint.
        :param params: Optional parameters included in request.
        :returns: Response for upstream request to the server.
        """

        params = dict(params or {})

        server = self.params.server
        verify = self.params.ssl_verify
        capem = self.params.ssl_capem


        params['key'] = (
            self.params.token)

        location = (
            f'https://{server}/'
            f'youtube/v3/{path}')


        return request(
            method=method,
            url=location,
            timeout=self.params.timeout,
            params=params,
            verify=capem or verify)


    def get_search(
        self,
        params: Optional[dict[str, Any]] = None,
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


        response = self.request(
            'get', 'search', params)

        response.raise_for_status()

        fetched = response.json()

        assert isinstance(fetched, dict)


        return [
            YouTubeResult(**x)
            for x in fetched['items']
            if x['id']['kind']
            in _RESULT_KINDS]
