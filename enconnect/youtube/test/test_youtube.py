"""
Functions and routines associated with Enasis Network Remote Connect.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from encommon import ENPYRWS
from encommon.types import inrepr
from encommon.types import instr
from encommon.utils import load_sample
from encommon.utils import prep_sample
from encommon.utils import read_text

from httpx import Response

from pytest import fixture
from pytest import mark

from respx import MockRouter

from . import SAMPLES
from ..params import YouTubeParams
from ..youtube import YouTube



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

    assert social.client is not None



def test_YouTube_search_block(
    social: YouTube,
    respx_mock: MockRouter,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param social: Class instance for connecting to service.
    :param respx_mock: Object for mocking request operation.
    """


    _search = read_text(
        f'{SAMPLES}/search'
        '/source.json')

    location = (
        'https://www.googleapis.com'
        '/youtube/v3')


    (respx_mock
     .get(f'{location}/search')
     .mock(Response(
         status_code=200,
         content=_search)))


    search = (
        social.search_block(
            {'channelId': 'mocked'}))


    sample_path = (
        f'{SAMPLES}/search'
        '/dumped.json')

    sample = load_sample(
        sample_path,
        [x.model_dump()
         for x in search],
        update=ENPYRWS)

    expect = prep_sample([
        x.model_dump()
        for x in search])

    assert sample == expect



@mark.asyncio
async def test_YouTube_search_async(
    social: YouTube,
    respx_mock: MockRouter,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param social: Class instance for connecting to service.
    :param respx_mock: Object for mocking request operation.
    """


    _search = read_text(
        f'{SAMPLES}/search'
        '/source.json')

    location = (
        'https://www.googleapis.com'
        '/youtube/v3')


    (respx_mock
     .get(f'{location}/search')
     .mock(Response(
         status_code=200,
         content=_search)))


    search = await (
        social.search_async(
            {'channelId': 'mocked'}))


    sample_path = (
        f'{SAMPLES}/search'
        '/dumped.json')

    sample = load_sample(
        sample_path,
        [x.model_dump()
         for x in search],
        update=ENPYRWS)

    expect = prep_sample([
        x.model_dump()
        for x in search])

    assert sample == expect



def test_YouTube_videos_block(
    social: YouTube,
    respx_mock: MockRouter,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param social: Class instance for connecting to service.
    :param respx_mock: Object for mocking request operation.
    """


    _videos = read_text(
        f'{SAMPLES}/videos'
        '/source.json')

    location = (
        'https://www.googleapis.com'
        '/youtube/v3')


    (respx_mock
     .get(f'{location}/videos')
     .mock(Response(
         status_code=200,
         content=_videos)))

    (respx_mock
     .get(f'{location}/videos')
     .mock(Response(
         status_code=200,
         content=_videos)))


    videos = (
        social.videos_block(
            {'id': 'mocked'}))

    video = (
        social.video_block('mocked'))


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
    respx_mock: MockRouter,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param social: Class instance for connecting to service.
    :param respx_mock: Object for mocking request operation.
    """


    _videos = read_text(
        f'{SAMPLES}/videos'
        '/source.json')

    location = (
        'https://www.googleapis.com'
        '/youtube/v3')


    (respx_mock
     .get(f'{location}/videos')
     .mock(Response(
         status_code=200,
         content=_videos)))

    (respx_mock
     .get(f'{location}/videos')
     .mock(Response(
         status_code=200,
         content=_videos)))


    videos = await (
        social.videos_async(
            {'id': 'mocked'}))

    video = await (
        social.video_async('mocked'))


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
