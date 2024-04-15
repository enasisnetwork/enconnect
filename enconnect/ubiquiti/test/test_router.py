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
from ..params import RouterParams
from ..router import Router



def test_Router() -> None:
    """
    Perform various tests associated with relevant routines.
    """

    params = RouterParams(
        server='192.168.1.1',
        username='mocked',
        password='mocked')

    router = Router(params)


    attrs = list(router.__dict__)

    assert attrs == [
        '_Router__params',
        '_Router__session']


    assert inrepr(
        'router.Router object',
        router)

    assert hash(router) > 0

    assert instr(
        'router.Router object',
        router)


    assert router.params is params

    assert router.session is not None


    def _mocker_cookie() -> None:

        server = params.server

        location = (
            f'https://{server}'
            '/api/auth/login')

        mocker.post(location)


    def _mocker_users() -> None:

        server = params.server

        location = (
            f'https://{server}'
            '/proxy/network'
            '/api/s/default/rest/user')

        source = read_text(
            f'{SAMPLES}/source.json')

        mocker.register_uri(
            'get', location,
            [{'text': source,
              'status_code': 401},
             {'text': source}])


    with Mocker() as mocker:

        _mocker_cookie()
        _mocker_users()

        request = router.request_proxy

        response = request(
            'get', 'rest/user')


    response.raise_for_status()

    fetched = response.json()


    sample_path = (
        f'{SAMPLES}/dumped.json')

    sample = load_sample(
        sample_path, fetched,
        update=ENPYRWS)

    expect = prep_sample(fetched)

    assert sample == expect
