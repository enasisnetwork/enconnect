"""
Functions and routines associated with Enasis Network Remote Connect.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from json import dumps
from json import loads

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
from ..params import RedditParams
from ..reddit import Reddit



@fixture
def social() -> Reddit:
    """
    Construct the instance for use in the downstream tests.

    :returns: Newly constructed instance of related class.
    """

    params = RedditParams(
        username='mocked',
        password='mocked',
        client='mocked',
        secret='mocked',
        useragent='mocked')

    return Reddit(params)



def test_Reddit(
    social: Reddit,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param social: Class instance for connecting to service.
    """


    attrs = lattrs(social)

    assert attrs == [
        '_Reddit__params',
        '_Reddit__client',
        '_Reddit__token']


    assert inrepr(
        'reddit.Reddit object',
        social)

    assert isinstance(
        hash(social), int)

    assert instr(
        'reddit.Reddit object',
        social)


    assert social.params

    assert social.client

    assert not social.token



def test_Reddit_latest_block(
    social: Reddit,
    respx_mock: MockRouter,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param social: Class instance for connecting to service.
    :param respx_mock: Object for mocking request operation.
    """


    _latest = read_text(
        SAMPLES / 'source.json')

    _token = read_text(
        SAMPLES / 'token.json')

    location = [
        'https://oauth.reddit.com',
        'https://www.reddit.com']


    (respx_mock
     .post(
         f'{location[1]}/api'
         '/v1/access_token')
     .mock(Response(
         status_code=200,
         content=_token)))

    (respx_mock
     .post(
         f'{location[0]}/api'
         '/v1/access_token')
     .mock(Response(
         status_code=200,
         content=_token)))

    (respx_mock
     .get(
         f'{location[0]}/r'
         '/mocked/new.json')
     .mock(side_effect=[
         Response(
             status_code=401),
         Response(
             status_code=200,
             content=_latest)]))


    latest = (
        social.latest_block('mocked'))


    sample_path = (
        SAMPLES / 'latest.json')

    sample = load_sample(
        sample_path,
        [x.endumped
         for x in latest],
        update=ENPYRWS)

    expect = prep_sample([
        x.endumped
        for x in latest])

    assert expect == sample


    social.request_token_block()



@mark.asyncio
async def test_Reddit_latest_async(
    social: Reddit,
    respx_mock: MockRouter,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param social: Class instance for connecting to service.
    :param respx_mock: Object for mocking request operation.
    """


    _latest = read_text(
        SAMPLES / 'source.json')

    _token = read_text(
        SAMPLES / 'token.json')

    location = [
        'https://oauth.reddit.com',
        'https://www.reddit.com']


    (respx_mock
     .post(
         f'{location[1]}/api'
         '/v1/access_token')
     .mock(Response(
         status_code=200,
         content=_token)))

    (respx_mock
     .post(
         f'{location[0]}/api'
         '/v1/access_token')
     .mock(Response(
         status_code=200,
         content=_token)))

    (respx_mock
     .get(
         f'{location[0]}/r'
         '/mocked/new.json')
     .mock(side_effect=[
         Response(
             status_code=401),
         Response(
             status_code=200,
             content=_latest)]))


    latest = await (
        social.latest_async('mocked'))


    sample_path = (
        SAMPLES / 'latest.json')

    sample = load_sample(
        sample_path,
        [x.endumped
         for x in latest],
        update=ENPYRWS)

    expect = prep_sample([
        x.endumped
        for x in latest])

    assert expect == sample


    await social.request_token_async()



def test_Reddit_listing_block(
    social: Reddit,
    respx_mock: MockRouter,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param social: Class instance for connecting to service.
    :param respx_mock: Object for mocking request operation.
    """


    _latest = read_text(
        SAMPLES / 'source.json')

    _token = read_text(
        SAMPLES / 'token.json')

    _listing = dumps([
        loads(_latest)])

    location = [
        'https://oauth.reddit.com',
        'https://www.reddit.com']


    (respx_mock
     .post(
         f'{location[1]}/api'
         '/v1/access_token')
     .mock(Response(
         status_code=200,
         content=_token)))

    (respx_mock
     .post(
         f'{location[0]}/api'
         '/v1/access_token')
     .mock(Response(
         status_code=200,
         content=_token)))

    (respx_mock
     .get(
         f'{location[0]}'
         '/comments/mocked.json')
     .mock(side_effect=[
         Response(
             status_code=401),
         Response(
             status_code=200,
             content=_listing)]))


    listing = (
        social.listing_block('mocked'))


    sample_path = (
        SAMPLES / 'listing.json')

    sample = load_sample(
        sample_path,
        listing.endumped,
        update=ENPYRWS)

    expect = prep_sample(
        listing.endumped)

    assert expect == sample



@mark.asyncio
async def test_Reddit_listing_async(
    social: Reddit,
    respx_mock: MockRouter,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param social: Class instance for connecting to service.
    :param respx_mock: Object for mocking request operation.
    """


    _latest = read_text(
        SAMPLES / 'source.json')

    _token = read_text(
        SAMPLES / 'token.json')

    _listing = dumps([
        loads(_latest)])

    location = [
        'https://oauth.reddit.com',
        'https://www.reddit.com']


    (respx_mock
     .post(
         f'{location[1]}/api'
         '/v1/access_token')
     .mock(Response(
         status_code=200,
         content=_token)))

    (respx_mock
     .post(
         f'{location[0]}/api'
         '/v1/access_token')
     .mock(Response(
         status_code=200,
         content=_token)))

    (respx_mock
     .get(
         f'{location[0]}'
         '/comments/mocked.json')
     .mock(side_effect=[
         Response(
             status_code=401),
         Response(
             status_code=200,
             content=_listing)]))


    listing = await (
        social.listing_async('mocked'))


    sample_path = (
        SAMPLES / 'listing.json')

    sample = load_sample(
        sample_path,
        listing.endumped,
        update=ENPYRWS)

    expect = prep_sample(
        listing.endumped)

    assert expect == sample
