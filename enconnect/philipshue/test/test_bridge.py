"""
Functions and routines associated with Enasis Network Remote Connect.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



import asyncio
from json import dumps
from json import loads
from typing import Any
from typing import AsyncIterator
from typing import Iterator

from encommon import ENPYRWS
from encommon.types import inrepr
from encommon.types import instr
from encommon.types.strings import SEMPTY
from encommon.utils import load_sample
from encommon.utils import prep_sample
from encommon.utils import read_text

from httpx import AsyncByteStream
from httpx import Request
from httpx import Response
from httpx import SyncByteStream

from pytest import fixture
from pytest import mark

from respx import MockRouter

from . import SAMPLES
from ..bridge import Bridge
from ..params import BridgeParams



_REQGET = Request('get', SEMPTY)



@fixture
def bridge() -> Bridge:
    """
    Construct the instance for use in the downstream tests.

    :returns: Newly constructed instance of related class.
    """

    params = BridgeParams(
        server='192.168.1.10',
        token='mocked')

    return Bridge(params)



def test_Bridge(
    bridge: Bridge,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param social: Class instance for connecting to service.
    """


    attrs = list(bridge.__dict__)

    assert attrs == [
        '_Bridge__params',
        '_Bridge__client']


    assert inrepr(
        'bridge.Bridge object',
        bridge)

    assert hash(bridge) > 0

    assert instr(
        'bridge.Bridge object',
        bridge)


    assert bridge.params is not None

    assert bridge.client is not None



def test_Bridge_request(
    bridge: Bridge,
    respx_mock: MockRouter,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param social: Class instance for connecting to service.
    :param respx_mock: Object for mocking request operation.
    """


    _source = read_text(
        f'{SAMPLES}/source'
        '/resource.json')

    location = (
        'https://192.168.1.10')


    (respx_mock
     .get(f'{location}/clip/v2/resource')
     .mock(Response(
         status_code=200,
         content=_source,
         request=_REQGET)))


    response = (
        bridge.request(
            'get', 'resource'))

    response.raise_for_status()


    fetched = response.json()

    sample_path = (
        f'{SAMPLES}/dumped'
        '/resource.json')

    sample = load_sample(
        sample_path, fetched,
        update=ENPYRWS)

    expect = prep_sample(fetched)

    assert sample == expect



def test_Bridge_events_block(
    bridge: Bridge,
    respx_mock: MockRouter,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param social: Class instance for connecting to service.
    :param respx_mock: Object for mocking request operation.
    """


    _events = loads(read_text(
        f'{SAMPLES}/source'
        '/events.json'))

    location = (
        'https://192.168.1.10'
        '/eventstream/clip/v2')


    class ByteStream(SyncByteStream):

        def __iter__(
            self,
        ) -> Iterator[bytes]:

            chunks = [
                (f'data: {dumps(x)}\n'
                 .encode('utf-8'))
                for x in _events]

            chunks.insert(0, b': hi\n')

            yield from chunks


    streamer = ByteStream()

    (respx_mock
     .get(location)
     .mock(Response(
         status_code=200,
         stream=streamer)))


    events = list(
        bridge.events_block())

    chunks: list[dict[str, Any]] = []

    for chunk in events:
        chunks.extend(chunk)


    sample_path = (
        f'{SAMPLES}/dumped'
        '/events.json')

    sample = load_sample(
        sample_path, chunks,
        update=ENPYRWS)

    expect = prep_sample(chunks)

    assert sample == expect



@mark.asyncio
async def test_Bridge_events_async(
    bridge: Bridge,
    respx_mock: MockRouter,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param social: Class instance for connecting to service.
    :param respx_mock: Object for mocking request operation.
    """


    _events = loads(read_text(
        f'{SAMPLES}/source'
        '/events.json'))

    location = (
        'https://192.168.1.10'
        '/eventstream/clip/v2')


    class ByteStream(AsyncByteStream):

        async def __aiter__(
            self,
        ) -> AsyncIterator[bytes]:

            chunks = [
                (f'data: {dumps(x)}\n'
                 .encode('utf-8'))
                for x in _events]

            chunks.insert(0, b': hi\n')

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


    events = (
        bridge.events_async())

    chunks: list[dict[str, Any]] = []

    async for chunk in events:
        chunks.extend(chunk)


    sample_path = (
        f'{SAMPLES}/dumped'
        '/events.json')

    sample = load_sample(
        sample_path, chunks,
        update=ENPYRWS)

    expect = prep_sample(chunks)

    assert sample == expect
