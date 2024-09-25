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
from ..models import InstagramMedia



def test_InstagramMedia() -> None:
    """
    Perform various tests associated with relevant routines.
    """

    content = read_text(
        SAMPLES / 'source.json')

    loaded = loads(content)

    assert isinstance(
        loaded, dict)

    source = loaded['data'][0]


    item = (
        InstagramMedia(**source))


    attrs = lattrs(item)

    assert attrs == [
        'caption',
        'id',
        'shared',
        'type',
        'location',
        'permalink',
        'thumbnail',
        'timestamp',
        'username']


    assert inrepr(
        'InstagramMedia(caption',
        item)

    with raises(TypeError):
        hash(item)

    assert instr(
        'caption=None',
        item)


    assert item.caption is None

    assert item.id == '18004631711419688'

    assert item.shared is None

    assert item.type == 'IMAGE'

    assert item.location[:5] == 'https'

    assert item.permalink
    assert item.permalink[:5] == 'https'

    assert item.thumbnail is None

    assert item.timestamp[:4] == '2024'

    assert item.username == 'enasisnetwork'
