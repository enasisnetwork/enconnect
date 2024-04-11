"""
Functions and routines associated with Enasis Network Remote Connect.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Any
from typing import Optional
from typing import TYPE_CHECKING

from pydantic import BaseModel

from requests import Response
from requests import request

if TYPE_CHECKING:
    from .params import InstagramParams



MEDIA_FIELDS = [
    'caption',
    'id',
    'is_shared_to_feed',
    'media_type',
    'media_url',
    'permalink',
    'thumbnail_url',
    'timestamp',
    'username']

MEDIA_RENAME = {
    'is_shared_to_feed': 'shared',
    'media_type': 'type',
    'media_url': 'location',
    'thumbnail_url': 'thumbnail'}



class InstagramMedia(BaseModel, extra='allow'):
    """
    Contains information returned from the upstream response.

    :param data: Keyword arguments passed to Pydantic model.
        Parameter is picked up by autodoc, please ignore.
    """

    caption: Optional[str] = None
    id: str
    shared: Optional[bool] = None
    type: str
    location: str
    permalink: Optional[str] = None
    thumbnail: Optional[str] = None
    timestamp: str
    username: str


    def __init__(
        self,
        **data: Any,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        items = MEDIA_RENAME.items()

        for old, new in items:

            if old not in data:
                continue

            data[new] = data[old]

            del data[old]

        super().__init__(**data)



class Instagram:
    """
    Interact with the cloud service API with various methods.

    :param params: Parameters for instantiating the instance.
    """

    __params: 'InstagramParams'


    def __init__(
        self,
        params: 'InstagramParams',
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        self.__params = params


    @property
    def params(
        self,
    ) -> 'InstagramParams':
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


        params['access_token'] = (
            self.params.token)

        location = (
            f'https://{server}/{path}')


        return request(
            method=method,
            url=location,
            timeout=self.params.timeout,
            params=params,
            verify=capem or verify)


    def get_media(
        self,
    ) -> list[InstagramMedia]:
        """
        Return the posts from the account associated with user.

        :returns: Posts from the account associated with user.
        """

        fields = ','.join(MEDIA_FIELDS)


        response = self.request(
            'get', 'me/media',
            {'fields': fields})

        response.raise_for_status()

        fetched = response.json()

        assert isinstance(fetched, dict)


        return [
            InstagramMedia(**x)
            for x in fetched['data']]
