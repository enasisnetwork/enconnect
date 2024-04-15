"""
Functions and routines associated with Enasis Network Remote Connect.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from encommon import ENPYRWS
from encommon.types import inrepr
from encommon.types import instr
from encommon.utils import load_sample
from encommon.utils import prep_sample
from encommon.utils import read_text

from requests_mock import Mocker

from . import SAMPLES
from ..bridge import Bridge
from ..params import BridgeParams



def test_Bridge() -> None:
    """
    Perform various tests associated with relevant routines.
    """

    params = BridgeParams(
        server='192.168.1.10',
        token='mocked')

    bridge = Bridge(params)


    attrs = list(bridge.__dict__)

    assert attrs == [
        '_Bridge__params']


    assert inrepr(
        'bridge.Bridge object',
        bridge)

    assert hash(bridge) > 0

    assert instr(
        'bridge.Bridge object',
        bridge)


    assert bridge.params is params


    def _mocker_resource() -> None:

        server = params.server

        location = (
            f'https://{server}'
            '/clip/v2/resource')

        source = read_text(
            f'{SAMPLES}/source.json')

        mocker.get(
            url=location,
            text=source)


    with Mocker() as mocker:

        _mocker_resource()

        request = bridge.request

        response = request(
            'get', 'resource')


    response.raise_for_status()

    fetched = response.json()


    sample_path = (
        f'{SAMPLES}/dumped.json')

    sample = load_sample(
        sample_path, fetched,
        update=ENPYRWS)

    expect = prep_sample(fetched)

    assert sample == expect
