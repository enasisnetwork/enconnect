"""
Functions and routines associated with Enasis Network Remote Connect.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from unittest.mock import AsyncMock
from unittest.mock import patch

from encommon import ENPYRWS
from encommon.types import inrepr
from encommon.types import instr
from encommon.types.strings import SEMPTY
from encommon.utils import load_sample
from encommon.utils import prep_sample
from encommon.utils import read_text

from httpx import Request
from httpx import Response

from pytest import fixture
from pytest import mark

from . import SAMPLES
from ..params import YouTubeParams
from ..youtube import YouTube



_REQGET = Request('get', SEMPTY)



@fixture
def social() -> YouTube:
    """
    Construct the instance for use in the downstream tests.

    :returns: Newly constructed instance of related class.
    """

    params = YouTubeParams(
        token='mocked')

    return YouTube(params)



def test_YouTube(
    social: YouTube,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param social: Class instance for connecting to service.
    """


    attrs = list(social.__dict__)

    assert attrs == [
        '_YouTube__params',
        '_YouTube__client']


    assert inrepr(
        'youtube.YouTube object',
        social)

    assert hash(social) > 0

    assert instr(
        'youtube.YouTube object',
        social)


    assert social.params is not None



def test_YouTube_search_block(
    social: YouTube,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param social: Class instance for connecting to service.
    """


    patched = patch(
        'httpx.Client.request')

    with patched as mocker:

        source = read_text(
            f'{SAMPLES}/search/source.json')

        mocker.side_effect = [
            Response(
                status_code=200,
                content=source,
                request=_REQGET)]

        payload = {'channelId': 'mocked'}

        results = (
            social
            .search_block(payload))


    sample_path = (
        f'{SAMPLES}/search/dumped.json')

    sample = load_sample(
        sample_path,
        [x.model_dump()
         for x in results],
        update=ENPYRWS)

    expect = prep_sample([
        x.model_dump()
        for x in results])

    assert sample == expect



@mark.asyncio
async def test_YouTube_search_async(
    social: YouTube,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param social: Class instance for connecting to service.
    """


    patched = patch(
        'httpx.AsyncClient.request',
        new_callable=AsyncMock)

    with patched as mocker:

        source = read_text(
            f'{SAMPLES}/search/source.json')

        mocker.side_effect = [
            Response(
                status_code=200,
                content=source,
                request=_REQGET)]

        payload = {'channelId': 'mocked'}

        waited = (
            social
            .search_async(payload))

        results = await waited


    sample_path = (
        f'{SAMPLES}/search/dumped.json')

    sample = load_sample(
        sample_path,
        [x.model_dump()
         for x in results],
        update=ENPYRWS)

    expect = prep_sample([
        x.model_dump()
        for x in results])

    assert sample == expect



def test_YouTube_videos_block(
    social: YouTube,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param social: Class instance for connecting to service.
    """


    patched = patch(
        'httpx.Client.request')

    with patched as mocker:

        source = read_text(
            f'{SAMPLES}/videos'
            '/source.json')

        mocker.side_effect = [
            Response(
                status_code=200,
                content=source,
                request=_REQGET),
            Response(
                status_code=200,
                content=source,
                request=_REQGET)]

        payload = {'id': 'mocked'}

        videos = (
            social.videos_block(
                payload))

        video = (
            social.video_block(
                'mocked'))


    sample_path = (
        f'{SAMPLES}/videos'
        '/dumped.json')

    sample = load_sample(
        sample_path,
        [x.model_dump()
         for x in videos],
        update=ENPYRWS)

    expect = prep_sample([
        x.model_dump()
        for x in videos])

    assert sample == expect


    assert video == videos[0]



@mark.asyncio
async def test_YouTube_videos_async(
    social: YouTube,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param social: Class instance for connecting to service.
    """


    patched = patch(
        'httpx.AsyncClient.request',
        new_callable=AsyncMock)

    with patched as mocker:

        source = read_text(
            f'{SAMPLES}/videos'
            '/source.json')

        mocker.side_effect = [
            Response(
                status_code=200,
                content=source,
                request=_REQGET),
            Response(
                status_code=200,
                content=source,
                request=_REQGET)]

        payload = {'id': 'mocked'}

        videos = await (
            social.videos_async(
                payload))

        video = await (
            social.video_async(
                'mocked'))


    sample_path = (
        f'{SAMPLES}/videos'
        '/dumped.json')

    sample = load_sample(
        sample_path,
        [x.model_dump()
         for x in videos],
        update=ENPYRWS)

    expect = prep_sample([
        x.model_dump()
        for x in videos])

    assert sample == expect


    assert video == videos[0]
