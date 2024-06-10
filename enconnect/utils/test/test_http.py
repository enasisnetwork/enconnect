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
def client() -> HTTPClient:
    """
    Construct the instance for use in the downstream tests.

    :returns: Newly constructed instance of related class.
    """

    return HTTPClient()



def test_HTTPClient(
    client: HTTPClient,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param client: Class instance for connecting with server.
    """


    attrs = list(client.__dict__)

    assert attrs == [
        '_HTTPClient__timeout',
        '_HTTPClient__headers',
        '_HTTPClient__verify',
        '_HTTPClient__capem',
        '_HTTPClient__httpauth',
        '_HTTPClient__retry',
        '_HTTPClient__backoff',
        '_HTTPClient__states',
        '_HTTPClient__client_block',
        '_HTTPClient__client_async']


    assert inrepr(
        'http.HTTPClient object',
        client)

    assert hash(client) > 0

    assert instr(
        'http.HTTPClient object',
        client)


    assert client.timeout == 30

    assert client.headers is None

    assert client.verify is True

    assert client.capem is None

    assert client.httpauth is None

    assert client.retry == 3

    assert client.backoff == 3.0

    assert client.states == {429}

    assert client.client_block is not None

    assert client.client_async is not None



def test_HTTPClient_block(
    client: HTTPClient,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param client: Class instance for connecting with server.
    """

    patched = patch(
        'httpx.Client.request')

    request = client.request_block

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
    client: HTTPClient,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param client: Class instance for connecting with server.
    """

    patched = patch(
        'httpx.AsyncClient.request',
        new_callable=AsyncMock)

    request = client.request_async

    with patched as mocker:

        mocker.side_effect = [
            Response(429),
            Response(200)]

        response = await request(
            'get', 'https://enasis.net')

        status = response.status_code

        assert status == 200

        assert mocker.call_count == 2
