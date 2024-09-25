"""
Functions and routines associated with Enasis Network Remote Connect.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



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

from respx import MockRouter

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
        server='192.168.1.11',
        appid=69,
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
        SAMPLES / 'source.json')

    source = read_sample(
        sample=source)


    (respx_mock
     .get(
         'https://192.168.1.11'
         '/apps/api/69'
         '/devices/all')
     .mock(Response(
         status_code=200,
         content=source)))


    request = bridge.request

    response = request(
        method='get',
        path='devices/all')

    response.raise_for_status()

    fetched = response.json()


    sample_path = (
        SAMPLES / 'dumped.json')

    sample = load_sample(
        path=sample_path,
        update=ENPYRWS,
        content=fetched)

    expect = prep_sample(
        content=fetched)

    assert expect == sample
