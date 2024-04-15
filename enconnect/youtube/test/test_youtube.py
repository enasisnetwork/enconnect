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
from ..params import YouTubeParams
from ..youtube import YouTube



def test_YouTube() -> None:
    """
    Perform various tests associated with relevant routines.
    """

    params = YouTubeParams(
        token='mocked')

    social = YouTube(params)


    attrs = list(social.__dict__)

    assert attrs == [
        '_YouTube__params']


    assert inrepr(
        'youtube.YouTube object',
        social)

    assert hash(social) > 0

    assert instr(
        'youtube.YouTube object',
        social)


    assert social.params is params


    def _mocker_search() -> None:

        server = params.server
        token = params.token

        location = (
            f'https://{server}/'
            'youtube/v3/search'
            '?channelId=mocked'
            '&maxResults=50'
            '&order=date'
            '&part=snippet,id'
            f'&key={token}')

        source = read_text(
            f'{SAMPLES}/source.json')

        mocker.get(
            url=location,
            text=source)


    with Mocker() as mocker:

        _mocker_search()

        results = social.get_search(
            {'channelId': 'mocked'})


    sample_path = (
        f'{SAMPLES}/dumped.json')

    sample = load_sample(
        sample_path,
        [x.model_dump()
         for x in results],
        update=ENPYRWS)

    expect = prep_sample([
        x.model_dump()
        for x in results])

    assert sample == expect
