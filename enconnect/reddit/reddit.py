"""
Functions and routines associated with Enasis Network Remote Connect.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



import asyncio
from typing import Literal
from typing import Optional
from typing import TYPE_CHECKING

from httpx import Response

from .models import RedditListing
from ..utils import HTTPClient
from ..utils.http import _HTTPAUTH
from ..utils.http import _PAYLOAD

if TYPE_CHECKING:
    from .params import RedditParams



class Reddit:
    """
    Interact with the cloud service API with various methods.

    :param params: Parameters used to instantiate the class.
    """

    __params: 'RedditParams'
    __client: HTTPClient

    __token: Optional[str]


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

        self.__token = None


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


    @property
    def token(
        self,
    ) -> Optional[str]:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.__token


    def request_token_block(
        self,
    ) -> str:
        """
        Establish new session obtaining token for authorization.

        :returns: Access token used with authenticated requests.
        """

        if self.__token is not None:
            return self.__token

        _params = self.__params
        username = _params.username
        password = _params.password
        client = _params.client
        secret = _params.secret

        request = self.request_block

        payload = {
            'grant_type': 'password',
            'username': username,
            'password': password}

        response = request(
            method='post',
            path='api/v1/access_token',
            data=payload,
            httpauth=(client, secret))

        response.raise_for_status()

        fetched = response.json()

        assert isinstance(fetched, dict)

        self.__token = (
            fetched['access_token'])

        return self.__token


    async def request_token_async(
        self,
    ) -> str:
        """
        Establish new session obtaining token for authorization.

        :returns: Access token used with authenticated requests.
        """

        if self.__token is not None:
            await asyncio.sleep(0)
            return self.__token

        _params = self.__params
        username = _params.username
        password = _params.password
        client = _params.client
        secret = _params.secret

        request = self.request_async

        payload = {
            'grant_type': 'password',
            'username': username,
            'password': password}

        response = await request(
            method='post',
            path='api/v1/access_token',
            data=payload,
            httpauth=(client, secret))

        response.raise_for_status()

        fetched = response.json()

        assert isinstance(fetched, dict)

        self.__token = (
            fetched['access_token'])

        return self.__token


    def request_block(
        self,
        method: Literal['get', 'post'],
        path: str,
        params: Optional[_PAYLOAD] = None,
        data: Optional[_PAYLOAD] = None,
        *,
        httpauth: Optional[_HTTPAUTH] = None,
    ) -> Response:
        """
        Return the response for upstream request to the server.

        :param method: Method for operation with the API server.
        :param path: Path for the location to upstream endpoint.
        :param params: Optional parameters included in request.
        :param data: Optional dict payload included in request.
        :param httpauth: Optional information for authentication.
        :returns: Response from upstream request to the server.
        """

        server = 'www.reddit.com'
        client = self.__client

        request = client.request_block


        token = self.__token
        tokey = 'Authorization'

        _params = self.__params
        agent = _params.useragent

        headers = {
            'User-Agent': agent}

        if token is not None:
            headers[tokey] = token
            server = 'oauth.reddit.com'


        location = (
            f'https://{server}/{path}')

        return request(
            method=method,
            location=location,
            params=params,
            data=data,
            headers=headers,
            httpauth=httpauth)


    async def request_async(
        self,
        method: Literal['get', 'post'],
        path: str,
        params: Optional[_PAYLOAD] = None,
        data: Optional[_PAYLOAD] = None,
        *,
        httpauth: Optional[_HTTPAUTH] = None,
    ) -> Response:
        """
        Return the response for upstream request to the server.

        :param method: Method for operation with the API server.
        :param path: Path for the location to upstream endpoint.
        :param params: Optional parameters included in request.
        :param data: Optional dict payload included in request.
        :param httpauth: Optional information for authentication.
        :returns: Response from upstream request to the server.
        """

        server = 'www.reddit.com'
        client = self.__client

        request = client.request_async


        token = self.__token
        tokey = 'Authorization'

        _params = self.__params
        agent = _params.useragent

        headers = {
            'User-Agent': agent}

        if token is not None:
            headers[tokey] = token
            server = 'oauth.reddit.com'


        location = (
            f'https://{server}/{path}')

        return await request(
            method=method,
            location=location,
            params=params,
            data=data,
            headers=headers,
            httpauth=httpauth)


    def listing_block(
        self,
        unique: str,
    ) -> RedditListing:
        """
        Return the specific content within the social platform.

        :param unique: Unique identifier within social platform.
        :returns: Specific content within the social platform.
        """

        request = self.request_block

        if self.__token is None:
            self.request_token_block()


        def _request() -> Response:

            return request(
                method='get',
                path=f'comments/{unique}.json')


        response = _request()

        if response.status_code == 401:

            self.__token = None

            self.request_token_block()

            response = _request()

        response.raise_for_status()

        fetched = response.json()

        assert isinstance(fetched, list)


        source = fetched[0]['data']
        children = source['children']

        return RedditListing(
            **children[0]['data'])


    async def listing_async(
        self,
        unique: str,
    ) -> RedditListing:
        """
        Return the specific content within the social platform.

        :param unique: Unique identifier within social platform.
        :returns: Specific content within the social platform.
        """

        request = self.request_async

        if self.__token is None:
            await self.request_token_async()


        async def _request() -> Response:

            return await request(
                method='get',
                path=f'comments/{unique}.json')


        response = await _request()

        if response.status_code == 401:

            self.__token = None

            await self.request_token_async()

            response = await _request()

        response.raise_for_status()

        fetched = response.json()

        assert isinstance(fetched, list)


        source = fetched[0]['data']
        children = source['children']

        return RedditListing(
            **children[0]['data'])


    def latest(
        # NOCVR
        self,
        subred: str,
        params: Optional[_PAYLOAD] = None,
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
        params: Optional[_PAYLOAD] = None,
    ) -> list[RedditListing]:
        """
        Return the new items within the provided subreddit path.

        :param subred: Path to subreddit containing the content.
        :param params: Optional parameters included in request.
        :returns: New items within the provided subreddit path.
        """

        params = dict(params or {})

        request = self.request_block

        if self.__token is None:
            self.request_token_block()


        def _request() -> Response:

            return request(
                method='get',
                path=f'r/{subred}/new.json')


        response = _request()

        if response.status_code == 401:

            self.__token = None

            self.request_token_block()

            response = _request()

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
        params: Optional[_PAYLOAD] = None,
    ) -> list[RedditListing]:
        """
        Return the new items within the provided subreddit path.

        :param subred: Path to subreddit containing the content.
        :param params: Optional parameters included in request.
        :returns: New items within the provided subreddit path.
        """

        params = dict(params or {})

        request = self.request_async

        if self.__token is None:
            await self.request_token_async()


        async def _request() -> Response:

            return await request(
                method='get',
                path=f'r/{subred}/new.json')


        response = await _request()

        if response.status_code == 401:

            self.__token = None

            await self.request_token_async()

            response = await _request()

        response.raise_for_status()

        fetched = response.json()

        assert isinstance(fetched, dict)


        source = fetched['data']
        children = source['children']

        return [
            RedditListing(**x['data'])
            for x in children]
