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


    attrs = lattrs(router)

    assert attrs == [
        '_Router__params',
        '_Router__client']


    assert inrepr(
        'router.Router object',
        router)

    assert isinstance(
        hash(router), int)

    assert instr(
        'router.Router object',
        router)


    assert router.params

    assert router.client



def test_Router_request(
    router: Router,
    respx_mock: MockRouter,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param router: Class instance for connecting to service.
    :param respx_mock: Object for mocking request operation.
    """


    source = read_text(
        SAMPLES / 'source.json')

    source = read_sample(
        sample=source)


    (respx_mock
     .get(
         'https://192.168.1.1'
         '/proxy/network/api/s'
         '/default/rest/user')
     .mock(side_effect=[
         Response(401),
         Response(
             status_code=200,
             content=source)]))

    (respx_mock
     .post(
         'https://192.168.1.1'
         '/api/auth/login')
     .mock(Response(200)))


    request = router.reqroxy

    response = request(
        method='get',
        path='rest/user')

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
