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
from ..instagram import Instagram
from ..params import InstagramParams



@fixture
def social() -> Instagram:
    """
    Construct the instance for use in the downstream tests.

    :returns: Newly constructed instance of related class.
    """

    params = InstagramParams(
        token='mocked')

    return Instagram(params)



def test_Instagram(
    social: Instagram,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param social: Class instance for connecting to service.
    """


    attrs = lattrs(social)

    assert attrs == [
        '_Instagram__params',
        '_Instagram__client']


    assert inrepr(
        'instagram.Instagram object',
        social)

    assert isinstance(
        hash(social), int)

    assert instr(
        'instagram.Instagram object',
        social)


    assert social.params

    assert social.client



def test_Instagram_block(
    social: Instagram,
    respx_mock: MockRouter,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param social: Class instance for connecting to service.
    :param respx_mock: Object for mocking request operation.
    """


    _latest = read_text(
        SAMPLES / 'source.json')

    _media = dumps(loads(
        _latest)['data'][0])

    location = (
        'https://graph.instagram.com')


    (respx_mock
     .get(f'{location}/me/media')
     .mock(Response(
         status_code=200,
         content=_latest)))

    (respx_mock
     .get(f'{location}/mocked')
     .mock(Response(
         status_code=200,
         content=_media)))


    latest = (
        social.latest_block())

    media = (
        social.media_block('mocked'))


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


    sample_path = (
        SAMPLES / 'media.json')

    sample = load_sample(
        sample_path,
        media.endumped,
        update=ENPYRWS)

    expect = prep_sample(
        media.endumped)

    assert expect == sample



@mark.asyncio
async def test_Instagram_async(
    social: Instagram,
    respx_mock: MockRouter,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param social: Class instance for connecting to service.
    :param respx_mock: Object for mocking request operation.
    """


    _latest = read_text(
        SAMPLES / 'source.json')

    _media = dumps(loads(
        _latest)['data'][0])

    location = (
        'https://graph.instagram.com')


    (respx_mock
     .get(f'{location}/me/media')
     .mock(Response(
         status_code=200,
         content=_latest)))

    (respx_mock
     .get(f'{location}/mocked')
     .mock(Response(
         status_code=200,
         content=_media)))


    latest = await (
        social.latest_async())

    media = await (
        social.media_async('mocked'))


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


    sample_path = (
        SAMPLES / 'media.json')

    sample = load_sample(
        sample_path,
        media.endumped,
        update=ENPYRWS)

    expect = prep_sample(
        media.endumped)

    assert expect == sample
