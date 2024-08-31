"""
Functions and routines associated with Enasis Network Remote Connect.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Annotated
from typing import Any
from typing import Literal
from typing import Optional

from encommon.types import BaseModel

from pydantic import Field



RESULT_KINDS = Literal[
    'channel',
    'playlist',
    'video']

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

VIDEO_VALUE = {
    'channelId': 'channel',
    'channelTitle': 'channel_title',
    'description': 'about',
    'publishedAt': 'published',
    'thumbnails': 'thumbnail',
    'title': 'title'}



class YouTubeResult(BaseModel, extra='ignore'):
    """
    Contains information returned from the upstream response.
    """

    kind: Annotated[
        RESULT_KINDS,
        Field(...,
              description='Value from the server response')]

    channel: Annotated[
        Optional[str],
        Field(None,
              description='Value from the server response')]

    playlist: Annotated[
        Optional[str],
        Field(None,
              description='Value from the server response')]

    video: Annotated[
        Optional[str],
        Field(None,
              description='Value from the server response')]

    title: Annotated[
        str,
        Field(...,
              description='Value from the server response')]

    about: Annotated[
        Optional[str],
        Field(None,
              description='Value from the server response')]

    channel_title: Annotated[
        Optional[str],
        Field(None,
              description='Value from the server response')]

    thumbnail: Annotated[
        str,
        Field(...,
              description='Value from the server response')]

    published: Annotated[
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



class YouTubeVideo(BaseModel, extra='ignore'):
    """
    Contains information returned from the upstream response.
    """

    kind: Annotated[
        RESULT_KINDS,
        Field(...,
              description='Value from the server response')]

    channel: Annotated[
        str,
        Field(...,
              description='Value from the server response')]

    video: Annotated[
        str,
        Field(...,
              description='Value from the server response')]

    title: Annotated[
        str,
        Field(...,
              description='Value from the server response')]

    about: Annotated[
        Optional[str],
        Field(None,
              description='Value from the server response')]

    thumbnail: Annotated[
        str,
        Field(...,
              description='Value from the server response')]

    published: Annotated[
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


        data['video'] = data['id']


        video = data['snippet']

        items = VIDEO_VALUE.items()

        for old, new in items:

            value = video.get(old)

            if value is None:
                continue  # NOCVR

            data[new] = value


        if 'thumbnail' in data:
            data['thumbnail'] = (
                data['thumbnail']
                ['high']['url'])


        data['kind'] = data['kind'][8:]


        super().__init__(**data)
