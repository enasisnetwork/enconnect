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
from ..params import RedditParams
from ..reddit import Reddit



def test_Reddit() -> None:
    """
    Perform various tests associated with relevant routines.
    """

    params = RedditParams()

    social = Reddit(params)


    attrs = list(social.__dict__)

    assert attrs == [
        '_Reddit__params']


    assert 1 <= repr(social).find(
        'reddit.Reddit object')

    assert hash(social) > 0

    assert 1 <= str(social).find(
        'reddit.Reddit object')


    assert social.params is params


    def _mocker_new() -> None:

        server = params.server

        location = (
            f'https://{server}/'
            'r/mocked/new.json')

        source = read_text(
            f'{SAMPLES}/source.json')

        mocker.get(
            url=location,
            text=source)


    with Mocker() as mocker:

        _mocker_new()

        listing = social.get_new('mocked')


    sample_path = (
        f'{SAMPLES}/dumped.json')

    sample = load_sample(
        sample_path,
        [x.model_dump()
         for x in listing],
        update=ENPYRWS)

    expect = prep_sample([
        x.model_dump()
        for x in listing])

    assert sample == expect
