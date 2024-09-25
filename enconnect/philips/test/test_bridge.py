"""
Functions and routines associated with Enasis Network Remote Connect.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from encommon.types import DictStrAny
from encommon.types import inrepr
from encommon.types import instr
from encommon.types import lattrs
from encommon.utils import load_sample
from encommon.utils import prep_sample
from encommon.utils import read_sample
from encommon.utils import read_text
from encommon.utils.sample import ENPYRWS

from httpx import Response

from pytest import fixture
from pytest import mark

from respx import MockRouter

from . import ByteStreamAsync
from . import ByteStreamBlock
from . import SAMPLES
from ..bridge import Bridge
from ..params import BridgeParams



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

    :param bridge: Class instance for connecting to service.
    """


    attrs = lattrs(bridge)

    assert attrs == [
        '_Bridge__params',
        '_Bridge__client']


    assert inrepr(
        'bridge.Bridge object',
        bridge)

    assert isinstance(
        hash(bridge), int)

    assert instr(
        'bridge.Bridge object',
        bridge)


    assert bridge.params

    assert bridge.client



def test_Bridge_request(
    bridge: Bridge,
    respx_mock: MockRouter,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param bridge: Class instance for connecting to service.
    :param respx_mock: Object for mocking request operation.
    """


    source = read_text(
        f'{SAMPLES}/source'
        '/resource.json')

    source = read_sample(
        sample=source)


    (respx_mock
     .get(
         'https://192.168.1.10'
         '/clip/v2/resource')
     .mock(Response(
         status_code=200,
         content=source)))


    request = bridge.request

    response = request(
        method='get',
        path='resource')

    response.raise_for_status()

    fetched = response.json()


    sample_path = (
        f'{SAMPLES}/dumped'
        '/resource.json')

    sample = load_sample(
        path=sample_path,
        update=ENPYRWS,
        content=fetched)

    expect = prep_sample(
        content=fetched)

    assert expect == sample



def test_Bridge_events_block(
    bridge: Bridge,
    respx_mock: MockRouter,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param bridge: Class instance for connecting to service.
    :param respx_mock: Object for mocking request operation.
    """


    source = read_text(
        f'{SAMPLES}/source'
        '/events.json')

    source = read_sample(
        sample=source)

    streamer = (
        ByteStreamBlock(source))

    (respx_mock
     .get(
         'https://192.168.1.10'
         '/eventstream/clip/v2')
     .mock(Response(
         status_code=200,
         stream=streamer)))


    request = bridge.events_block

    events = list(request())


    sample_path = (
        f'{SAMPLES}/dumped'
        '/events.json')

    sample = load_sample(
        path=sample_path,
        update=ENPYRWS,
        content=events)

    expect = prep_sample(
        content=events)

    assert expect == sample



@mark.asyncio
async def test_Bridge_events_async(
    bridge: Bridge,
    respx_mock: MockRouter,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param bridge: Class instance for connecting to service.
    :param respx_mock: Object for mocking request operation.
    """


    source = read_text(
        f'{SAMPLES}/source'
        '/events.json')

    source = read_sample(
        sample=source)

    streamer = (
        ByteStreamAsync(source))

    (respx_mock
     .get(
         'https://192.168.1.10'
         '/eventstream/clip/v2')
     .mock(Response(
         status_code=200,
         stream=streamer)))


    request = bridge.events_async

    _events = request()

    events: list[DictStrAny] = []

    async for event in _events:
        events.append(event)


    sample_path = (
        f'{SAMPLES}/dumped'
        '/events.json')

    sample = load_sample(
        path=sample_path,
        update=ENPYRWS,
        content=events)

    expect = prep_sample(
        content=events)

    assert expect == sample
