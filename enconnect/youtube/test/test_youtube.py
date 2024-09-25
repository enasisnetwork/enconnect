"""
Functions and routines associated with Enasis Network Remote Connect.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from encommon.types import inrepr
from encommon.types import instr
from encommon.types import lattrs
from encommon.utils import load_sample
from encommon.utils import prep_sample
from encommon.utils import read_text
from encommon.utils.sample import ENPYRWS

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


    attrs = lattrs(social)

    assert attrs == [
        '_YouTube__params',
        '_YouTube__client']


    assert inrepr(
        'youtube.YouTube object',
        social)

    assert isinstance(
        hash(social), int)

    assert instr(
        'youtube.YouTube object',
        social)


    assert social.params

    assert social.client



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
        [x.endumped
         for x in search],
        update=ENPYRWS)

    expect = prep_sample([
        x.endumped
        for x in search])

    assert expect == sample



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
        [x.endumped
         for x in search],
        update=ENPYRWS)

    expect = prep_sample([
        x.endumped
        for x in search])

    assert expect == sample



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
        [x.endumped
         for x in videos],
        update=ENPYRWS)

    expect = prep_sample([
        x.endumped
        for x in videos])

    assert expect == sample


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
        [x.endumped
         for x in videos],
        update=ENPYRWS)

    expect = prep_sample([
        x.endumped
        for x in videos])

    assert expect == sample


    assert video == videos[0]
