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


    patched = patch(
        'httpx.Client.request')

    with patched as mocker:

        source = read_text(
            f'{SAMPLES}/source.json')

        request = Request('get', SEMPTY)

        mocker.side_effect = [
            Response(
                status_code=200,
                content=source,
                request=request)]

        media = social.latest_block()


    sample_path = (
        f'{SAMPLES}/dumped.json')

    sample = load_sample(
        sample_path,
        [x.model_dump()
         for x in media],
        update=ENPYRWS)

    expect = prep_sample([
        x.model_dump()
        for x in media])

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

        source = read_text(
            f'{SAMPLES}/source.json')

        request = Request('get', SEMPTY)

        mocker.side_effect = [
            Response(
                status_code=200,
                content=source,
                request=request)]

        waited = social.latest_async()

        media = await waited


    sample_path = (
        f'{SAMPLES}/dumped.json')

    sample = load_sample(
        sample_path,
        [x.model_dump()
         for x in media],
        update=ENPYRWS)

    expect = prep_sample([
        x.model_dump()
        for x in media])

    assert sample == expect
