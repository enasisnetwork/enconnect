"""
Functions and routines associated with Enasis Network Remote Connect.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



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

        mocker.side_effect = [
            Response(
                status_code=200,
                content=source,
                request=_REQGET)]

        response = (
            bridge.request(
                'get', 'resource'))

        response.raise_for_status()


    fetched = response.json()

    sample_path = (
        f'{SAMPLES}/dumped.json')

    sample = load_sample(
        sample_path, fetched,
        update=ENPYRWS)

    expect = prep_sample(fetched)

    assert sample == expect
