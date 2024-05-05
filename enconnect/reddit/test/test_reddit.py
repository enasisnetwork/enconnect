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
from ..params import RedditParams
from ..reddit import Reddit



_REQGET = Request('get', SEMPTY)
_REQPOST = Request('post', SEMPTY)



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


    attrs = list(social.__dict__)

    assert attrs == [
        '_Reddit__params',
        '_Reddit__client',
        '_Reddit__token']


    assert inrepr(
        'reddit.Reddit object',
        social)

    assert hash(social) > 0

    assert instr(
        'reddit.Reddit object',
        social)


    assert social.params is not None

    assert social.token is None



def test_Reddit_block(
    social: Reddit,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param social: Class instance for connecting to service.
    """


    patched = patch(
        'httpx.Client.request')

    with patched as mocker:

        source = read_text(
            f'{SAMPLES}/source.json')

        token = read_text(
            f'{SAMPLES}/token.json')

        mocker.side_effect = [
            Response(
                status_code=200,
                content=token,
                request=_REQPOST),
            Response(
                status_code=401,
                content=source,
                request=_REQGET),
            Response(
                status_code=200,
                content=token,
                request=_REQPOST),
            Response(
                status_code=200,
                content=source,
                request=_REQGET)]

        listing = (
            social
            .latest_block('mocked'))


    sample_path = (
        f'{SAMPLES}/dumped.json')

    sample = load_sample(
        sample_path,
        [x.model_dump()
         for x in listing],
        update=ENPYRWS)

    expect = prep_sample([
        x.model_dump()
        for x in listing])

    assert sample == expect


    social.request_token_block()



@mark.asyncio
async def test_Reddit_async(
    social: Reddit,
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
            f'{SAMPLES}/source.json')

        token = read_text(
            f'{SAMPLES}/token.json')

        mocker.side_effect = [
            Response(
                status_code=200,
                content=token,
                request=_REQPOST),
            Response(
                status_code=401,
                content=source,
                request=_REQGET),
            Response(
                status_code=200,
                content=token,
                request=_REQPOST),
            Response(
                status_code=200,
                content=source,
                request=_REQGET)]

        waited = (
            social
            .latest_async('mocked'))

        listing = await waited


    sample_path = (
        f'{SAMPLES}/dumped.json')

    sample = load_sample(
        sample_path,
        [x.model_dump()
         for x in listing],
        update=ENPYRWS)

    expect = prep_sample([
        x.model_dump()
        for x in listing])

    assert sample == expect


    await social.request_token_async()
