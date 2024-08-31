"""
Functions and routines associated with Enasis Network Remote Connect.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Annotated
from typing import Any
from typing import Optional

from encommon.types import BaseModel

from pydantic import Field



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
    """

    caption: Annotated[
        Optional[str],
        Field(None,
              description='Value from the server response')]

    id: Annotated[
        str,
        Field(...,
              description='Value from the server response')]

    shared: Annotated[
        Optional[bool],
        Field(None,
              description='Value from the server response')]

    type: Annotated[
        str,
        Field(...,
              description='Value from the server response')]

    location: Annotated[
        str,
        Field(...,
              description='Value from the server response')]

    permalink: Annotated[
        Optional[str],
        Field(None,
              description='Value from the server response')]

    thumbnail: Annotated[
        Optional[str],
        Field(None,
              description='Value from the server response')]

    timestamp: Annotated[
        str,
        Field(...,
              description='Value from the server response')]

    username: Annotated[
        str,
        Field(...,
              description='Value from the server response')]


    def __init__(
        self,
        /,
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
