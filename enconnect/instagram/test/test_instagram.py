"""
Functions and routines associated with Enasis Network Remote Connect.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from encommon import ENPYRWS
from encommon.utils import load_sample
from encommon.utils import prep_sample
from encommon.utils import read_text

from requests_mock import Mocker

from . import SAMPLES
from ..instagram import Instagram
from ..instagram import MEDIA_FIELDS
from ..params import InstagramParams



def test_Instagram() -> None:
    """
    Perform various tests associated with relevant routines.
    """

    params = InstagramParams(
        token='mocked')

    social = Instagram(params)


    attrs = list(social.__dict__)

    assert attrs == [
        '_Instagram__params']


    assert 1 <= repr(social).find(
        'instagram.Instagram object')

    assert hash(social) > 0

    assert 1 <= str(social).find(
        'instagram.Instagram object')


    assert social.params is params


    def _mocker_media() -> None:

        server = params.server
        token = params.token

        fields = ','.join(MEDIA_FIELDS)

        location = (
            f'https://{server}/'
            'me/media'
            f'?fields={fields}'
            f'&access_token={token}')

        source = read_text(
            f'{SAMPLES}/source.json')

        mocker.get(
            url=location,
            text=source)


    with Mocker() as mocker:

        _mocker_media()

        media = social.get_media()


    sample_path = (
        f'{SAMPLES}/dumped.json')

    sample = load_sample(
        sample_path,
        [x.model_dump()
         for x in media],
        update=ENPYRWS)

    expect = prep_sample([
        x.model_dump()
        for x in media])

    assert sample == expect
