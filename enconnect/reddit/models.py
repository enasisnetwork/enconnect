"""
Functions and routines associated with Enasis Network Remote Connect.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Annotated
from typing import Any
from typing import Optional

from encommon.types import BaseModel
from encommon.types import getate
from encommon.types import sort_dict

from pydantic import Field



LISTING_VALUE = {
    'created_utc': 'created',
    'ups': 'vote_ups',
    'downs': 'vote_downs',
    'url_overridden_by_dest': 'url_dest',
    'media_metadata': 'medias'}



class RedditListing(BaseModel, extra='ignore'):
    """
    Contains information returned from the upstream response.
    """

    name: Annotated[
        str,
        Field(...,
              description='Value from the server response')]

    id: Annotated[
        str,
        Field(...,
              description='Value from the server response')]

    created: Annotated[
        int,
        Field(...,
              description='Value from the server response')]

    title: Annotated[
        str,
        Field(...,
              description='Value from the server response')]

    selftext: Annotated[
        Optional[str],
        Field(None,
              description='Value from the server response')]

    author: Annotated[
        str,
        Field(...,
              description='Value from the server response')]

    url: Annotated[
        str,
        Field(...,
              description='Value from the server response')]

    permalink: Annotated[
        str,
        Field(...,
              description='Value from the server response')]

    thumbnail: Annotated[
        str,
        Field(...,
              description='Value from the server response')]

    url_dest: Annotated[
        Optional[str],
        Field(None,
              description='Value from the server response')]

    domain: Annotated[
        str,
        Field(...,
              description='Value from the server response')]

    medias: Annotated[
        Optional[list[str]],
        Field(None,
              description='Value from the server response')]

    pinned: Annotated[
        bool,
        Field(...,
              description='Value from the server response')]

    edited: Annotated[
        bool | float,
        Field(...,
              description='Value from the server response')]

    stickied: Annotated[
        bool,
        Field(...,
              description='Value from the server response')]

    archived: Annotated[
        bool,
        Field(...,
              description='Value from the server response')]

    vote_downs: Annotated[
        int,
        Field(...,
              description='Value from the server response')]

    vote_ups: Annotated[
        int,
        Field(...,
              description='Value from the server response')]

    score: Annotated[
        int,
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

            medias = data['medias']


            gitems = getate(
                data,
                'gallery_data/items')


            if gitems is not None:

                for item in gitems:

                    _unique = item['id']
                    _media = item['media_id']

                    if _media not in medias:
                        continue  # NOCVR

                    media = medias[_media]

                    medias[_unique] = media

                    del medias[_media]


            mitems = (
                sort_dict(medias)
                .items())


            for _, media in mitems:

                assert isinstance(
                    media, dict)

                image = getate(
                    media, 's/u')

                assert isinstance(
                    image, str)

                images.append(image)


            data['medias'] = images




        super().__init__(**data)
