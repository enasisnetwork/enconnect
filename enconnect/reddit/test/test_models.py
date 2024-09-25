"""
Functions and routines associated with Enasis Network Remote Connect.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from json import loads

from encommon.types import inrepr
from encommon.types import instr
from encommon.types import lattrs
from encommon.utils import read_text

from pytest import raises

from . import SAMPLES
from ..models import RedditListing



def test_RedditListing() -> None:
    """
    Perform various tests associated with relevant routines.
    """

    content = read_text(
        SAMPLES / 'source.json')

    loaded = loads(content)

    assert isinstance(
        loaded, dict)

    source = (
        loaded['data']
        ['children']
        [0]['data'])


    item = (
        RedditListing(**source))


    attrs = lattrs(item)

    assert attrs == [
        'name',
        'id',
        'created',
        'title',
        'selftext',
        'author',
        'url',
        'permalink',
        'thumbnail',
        'url_dest',
        'domain',
        'medias',
        'pinned',
        'edited',
        'stickied',
        'archived',
        'vote_downs',
        'vote_ups',
        'score']


    assert inrepr(
        'RedditListing(name',
        item)

    with raises(TypeError):
        hash(item)

    assert instr(
        "name='t3_1c2wc19'",
        item)


    assert item.name == 't3_1c2wc19'

    assert item.id == '1c2wc19'

    assert item.created == 1712993526

    assert item.title[:7] == 'Welcome'

    assert item.selftext
    assert item.selftext[:5] == 'Hello'

    assert item.author == 'enasisnetwork'

    assert item.url[:5] == 'https'

    assert item.permalink[:16] == '/r/enasisnetwork'

    assert item.thumbnail == 'self'

    assert item.url_dest is None

    assert item.domain == 'self.enasisnetwork'

    assert item.medias is None

    assert item.pinned is False

    assert item.edited is False

    assert item.stickied is False

    assert item.archived is False

    assert item.vote_downs == 0

    assert item.vote_ups == 1

    assert item.score == 1
