"""
Functions and routines associated with Enasis Network Remote Connect.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



import asyncio
from typing import AsyncIterator
from typing import Iterator
from unittest.mock import AsyncMock
from unittest.mock import patch

from encommon.types import inrepr
from encommon.types import instr
from encommon.types import lattrs

from httpx import AsyncByteStream
from httpx import Response
from httpx import SyncByteStream

from pytest import fixture
from pytest import mark

from respx import MockRouter

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


    attrs = lattrs(client)

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

    assert isinstance(
        hash(client), int)

    assert instr(
        'http.HTTPClient object',
        client)


    assert client.timeout == 30

    assert not client.headers

    assert client.verify

    assert not client.capem

    assert not client.httpauth

    assert client.retry == 3

    assert client.backoff == 3.0

    assert client.states == {429}

    assert client.client_block

    assert client.client_async



def test_HTTPClient_request_block(
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
async def test_HTTPClient_request_async(
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



def test_HTTPClient_stream_block(
    client: HTTPClient,
    respx_mock: MockRouter,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param client: Class instance for connecting with server.
    :param respx_mock: Object for mocking request operation.
    """


    location = (
        'https://192.168.1.10'
        '/eventstream/clip/v2')


    class ByteStream(SyncByteStream):

        def __iter__(
            self,
        ) -> Iterator[bytes]:

            chunks = [
                b'stream content\n',
                b'stream content\n']

            yield from chunks


    streamer = ByteStream()

    (respx_mock
     .get(location)
     .mock(Response(
         status_code=200,
         stream=streamer)))


    request = client.stream_block

    stream = request(
        'get', location)


    chunks: list[str] = []

    for chunk in stream:
        chunks.append(chunk)

    assert chunks == [
        'stream content',
        'stream content']



@mark.asyncio
async def test_HTTPClient_stream_async(
    client: HTTPClient,
    respx_mock: MockRouter,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param client: Class instance for connecting with server.
    :param respx_mock: Object for mocking request operation.
    """


    location = (
        'https://192.168.1.10'
        '/eventstream/clip/v2')


    class ByteStream(AsyncByteStream):

        async def __aiter__(
            self,
        ) -> AsyncIterator[bytes]:

            chunks = [
                b'stream content\n',
                b'stream content\n']

            await asyncio.sleep(0)

            for chunk in chunks:

                yield chunk

                await asyncio.sleep(0)

            await asyncio.sleep(0)


    streamer = ByteStream()

    (respx_mock
     .get(location)
     .mock(Response(
         status_code=200,
         stream=streamer)))


    request = client.stream_async

    stream = request(
        'get', location)


    chunks: list[str] = []

    async for chunk in stream:
        chunks.append(chunk)

    assert chunks == [
        'stream content',
        'stream content']


    await asyncio.sleep(0)
