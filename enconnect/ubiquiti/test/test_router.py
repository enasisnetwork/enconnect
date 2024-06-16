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

from httpx import Response

from pytest import fixture

from respx import MockRouter

from . import SAMPLES
from ..params import RouterParams
from ..router import Router



@fixture
def router() -> Router:
    """
    Construct the instance for use in the downstream tests.

    :returns: Newly constructed instance of related class.
    """

    params = RouterParams(
        server='192.168.1.1',
        username='mocked',
        password='mocked')

    return Router(params)



def test_Router(
    router: Router,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param router: Class instance for connecting to service.
    """


    attrs = list(router.__dict__)

    assert attrs == [
        '_Router__params',
        '_Router__client']


    assert inrepr(
        'router.Router object',
        router)

    assert hash(router) > 0

    assert instr(
        'router.Router object',
        router)


    assert router.params is not None

    assert router.client is not None



def test_Router_request(
    router: Router,
    respx_mock: MockRouter,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param router: Class instance for connecting to service.
    :param respx_mock: Object for mocking request operation.
    """


    _source = read_text(
        f'{SAMPLES}/source.json')

    location = (
        'https://192.168.1.1')


    (respx_mock
     .get(
         f'{location}/proxy/network'
         '/api/s/default/rest/user')
     .mock(side_effect=[
         Response(
             status_code=401),
         Response(
             status_code=200,
             content=_source)]))

    (respx_mock
     .post(f'{location}/api/auth/login')
     .mock(Response(
         status_code=200,
         content=_source)))


    response = (
        router.request_proxy(
            'get', 'rest/user'))

    response.raise_for_status()


    fetched = response.json()

    sample_path = (
        f'{SAMPLES}/dumped.json')

    sample = load_sample(
        sample_path, fetched,
        update=ENPYRWS)

    expect = prep_sample(fetched)

    assert sample == expect
