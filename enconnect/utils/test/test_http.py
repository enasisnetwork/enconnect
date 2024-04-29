"""
Functions and routines associated with Enasis Network Remote Connect.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from unittest.mock import AsyncMock
from unittest.mock import patch

from encommon.types import inrepr
from encommon.types import instr

from httpx import Response

from pytest import fixture
from pytest import mark

from ..http import HTTPClient



@fixture
def httpx() -> HTTPClient:
    """
    Construct the instance for use in the downstream tests.

    :returns: Newly constructed instance of related class.
    """

    return HTTPClient()



def test_HTTPClient(
    httpx: HTTPClient,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param httpx: Class instance for connecting with server.
    """


    attrs = list(httpx.__dict__)

    assert attrs == [
        '_HTTPClient__timeout',
        '_HTTPClient__verify',
        '_HTTPClient__capem',
        '_HTTPClient__retry',
        '_HTTPClient__backoff',
        '_HTTPClient__states',
        '_HTTPClient__client_block',
        '_HTTPClient__client_async']


    assert inrepr(
        'http.HTTPClient object',
        httpx)

    assert hash(httpx) > 0

    assert instr(
        'http.HTTPClient object',
        httpx)


    assert httpx.timeout == 30

    assert httpx.verify is True

    assert httpx.capem is None

    assert httpx.retry == 3

    assert httpx.backoff == 3.0

    assert httpx.states == {429}

    assert httpx.client_block is not None

    assert httpx.client_async is not None



def test_HTTPClient_block(
    httpx: HTTPClient,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param httpx: Class instance for connecting with server.
    """

    patched = patch(
        'httpx.Client.request')

    request = httpx.request_block

    with patched as mocker:

        mocker.side_effect = [
            Response(429),
            Response(200)]

        response = request(
            'get', 'https://enasis.net')

        status = response.status_code

        assert status == 200

        assert mocker.call_count == 2



@mark.asyncio
async def test_HTTPClient_async(
    httpx: HTTPClient,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param httpx: Class instance for connecting with server.
    """

    patched = patch(
        'httpx.AsyncClient.request',
        new_callable=AsyncMock)

    request = httpx.request_async

    with patched as mocker:

        mocker.side_effect = [
            Response(429),
            Response(200)]

        response = await request(
            'get', 'https://enasis.net')

        status = response.status_code

        assert status == 200

        assert mocker.call_count == 2
