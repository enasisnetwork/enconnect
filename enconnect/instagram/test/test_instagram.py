"""
Functions and routines associated with Enasis Network Remote Connect.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from json import dumps
from json import loads
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
from ..instagram import Instagram
from ..params import InstagramParams



_REQGET = Request('get', SEMPTY)



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


    attrs = list(social.__dict__)

    assert attrs == [
        '_Instagram__params',
        '_Instagram__client']


    assert inrepr(
        'instagram.Instagram object',
        social)

    assert hash(social) > 0

    assert instr(
        'instagram.Instagram object',
        social)


    assert social.params is not None



def test_Instagram_block(
    social: Instagram,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param social: Class instance for connecting to service.
    """


    patched = patch(
        'httpx.Client.request')

    with patched as mocker:

        _latest = read_text(
            f'{SAMPLES}/source.json')

        _media = dumps(loads(
            _latest)['data'][0])

        mocker.side_effect = [
            Response(
                status_code=200,
                content=_latest,
                request=_REQGET),
            Response(
                status_code=200,
                content=_media,
                request=_REQGET)]

        latest = (
            social.latest_block())

        media = (
            social.media_block(
                'mocked'))


    sample_path = (
        f'{SAMPLES}/latest.json')

    sample = load_sample(
        sample_path,
        [x.model_dump()
         for x in latest],
        update=ENPYRWS)

    expect = prep_sample([
        x.model_dump()
        for x in latest])

    assert sample == expect


    sample_path = (
        f'{SAMPLES}/media.json')

    sample = load_sample(
        sample_path,
        media.model_dump(),
        update=ENPYRWS)

    expect = prep_sample(
        media.model_dump())

    assert sample == expect



@mark.asyncio
async def test_Instagram_async(
    social: Instagram,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param social: Class instance for connecting to service.
    """


    patched = patch(
        'httpx.AsyncClient.request',
        new_callable=AsyncMock)

    with patched as mocker:

        _latest = read_text(
            f'{SAMPLES}/source.json')

        _media = dumps(loads(
            _latest)['data'][0])

        mocker.side_effect = [
            Response(
                status_code=200,
                content=_latest,
                request=_REQGET),
            Response(
                status_code=200,
                content=_media,
                request=_REQGET)]

        latest = await (
            social.latest_async())

        media = await (
            social.media_async(
                'mocked'))


    sample_path = (
        f'{SAMPLES}/latest.json')

    sample = load_sample(
        sample_path,
        [x.model_dump()
         for x in latest],
        update=ENPYRWS)

    expect = prep_sample([
        x.model_dump()
        for x in latest])

    assert sample == expect


    sample_path = (
        f'{SAMPLES}/media.json')

    sample = load_sample(
        sample_path,
        media.model_dump(),
        update=ENPYRWS)

    expect = prep_sample(
        media.model_dump())

    assert sample == expect
