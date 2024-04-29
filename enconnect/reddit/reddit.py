"""
Functions and routines associated with Enasis Network Remote Connect.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Any
from typing import Literal
from typing import Optional
from typing import TYPE_CHECKING

from encommon.types import getate

from httpx import Response

from pydantic import BaseModel

from ..utils import HTTPClient

if TYPE_CHECKING:
    from .params import RedditParams



LISTING_VALUE = {
    'created_utc': 'created',
    'ups': 'vote_ups',
    'downs': 'vote_downs',
    'url_overridden_by_dest': 'url_dest',
    'media_metadata': 'medias'}



class RedditListing(BaseModel, extra='ignore'):
    """
    Contains information returned from the upstream response.

    .. note::
       Fields are not completely documented for this model.

    :param data: Keyword arguments passed to Pydantic model.
        Parameter is picked up by autodoc, please ignore.
    """

    name: str
    id: str
    created: int
    title: str
    selftext: Optional[str] = None
    author: str

    url: str
    permalink: str
    thumbnail: str
    url_dest: Optional[str] = None
    domain: str

    medias: Optional[list[str]] = None

    pinned: bool
    edited: bool | float
    stickied: bool
    archived: bool

    vote_downs: int
    vote_ups: int

    score: int


    def __init__(
        self,
        **data: Any,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        items = LISTING_VALUE.items()

        for old, new in items:

            value = data.get(old)

            if value is None:
                continue

            data[new] = value


        data = {
            k: v for k, v in
            data.items()
            if v not in ['', None]}


        if data.get('medias'):

            images: list[str] = []

            items = data['medias'].items()

            for _, media in items:

                assert isinstance(media, dict)

                image = getate(media, 's/u')

                assert isinstance(image, str)

                images.append(image)

            data['medias'] = images


        super().__init__(**data)



class Reddit:
    """
    Interact with the cloud service API with various methods.

    :param params: Parameters for instantiating the instance.
    """

    __params: 'RedditParams'
    __client: HTTPClient


    def __init__(
        self,
        params: 'RedditParams',
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
    ) -> 'RedditParams':
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
        client = self.client

        location = (
            f'https://{server}/{path}')

        request = client.request_block

        return request(
            method=method,
            location=location,
            params=params)


    async def request_async(
        self,
        method: Literal['get'],
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
        client = self.client

        location = (
            f'https://{server}/{path}')

        request = client.request_async

        return await request(
            method=method,
            location=location,
            params=params)


    def latest(
        # NOCVR
        self,
        subred: str,
        params: Optional[dict[str, Any]] = None,
    ) -> list[RedditListing]:
        """
        Return the new items within the provided subreddit path.

        :param subred: Path to subreddit containing the content.
        :param params: Optional parameters included in request.
        :returns: New items within the provided subreddit path.
        """

        return self.latest_block(subred, params)


    def latest_block(
        self,
        subred: str,
        params: Optional[dict[str, Any]] = None,
    ) -> list[RedditListing]:
        """
        Return the new items within the provided subreddit path.

        :param subred: Path to subreddit containing the content.
        :param params: Optional parameters included in request.
        :returns: New items within the provided subreddit path.
        """

        params = dict(params or {})


        request = self.request_block

        response = request(
            'get', f'r/{subred}/new.json')

        response.raise_for_status()

        fetched = response.json()

        assert isinstance(fetched, dict)


        source = fetched['data']
        children = source['children']

        return [
            RedditListing(**x['data'])
            for x in children]


    async def latest_async(
        self,
        subred: str,
        params: Optional[dict[str, Any]] = None,
    ) -> list[RedditListing]:
        """
        Return the new items within the provided subreddit path.

        :param subred: Path to subreddit containing the content.
        :param params: Optional parameters included in request.
        :returns: New items within the provided subreddit path.
        """

        params = dict(params or {})


        request = self.request_async

        response = await request(
            'get', f'r/{subred}/new.json')

        response.raise_for_status()

        fetched = response.json()

        assert isinstance(fetched, dict)


        source = fetched['data']
        children = source['children']

        return [
            RedditListing(**x['data'])
            for x in children]
