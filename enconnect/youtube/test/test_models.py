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
from ..models import YouTubeResult
from ..models import YouTubeVideo



def test_YouTubeResult() -> None:
    """
    Perform various tests associated with relevant routines.
    """

    content = read_text(
        f'{SAMPLES}/search'
        '/source.json')

    loaded = loads(content)

    assert isinstance(
        loaded, dict)

    source = loaded['items'][0]


    item = (
        YouTubeResult(**source))


    attrs = lattrs(item)

    assert attrs == [
        'kind',
        'channel',
        'playlist',
        'video',
        'title',
        'about',
        'channel_title',
        'thumbnail',
        'published']


    assert inrepr(
        'YouTubeResult(kind',
        item)

    with raises(TypeError):
        hash(item)

    assert instr(
        "kind='video'",
        item)

    assert item.kind == 'video'

    assert item.channel == 'UCPNB7Hrq5oHl81EzG6x3BwA'

    assert item.playlist is None

    assert item.video == 'FIEkHYHDjzk'

    assert item.title == 'Validating encommon code'

    assert item.about
    assert item.about[:12] == 'Demonstrates'

    assert item.channel_title == 'Enasis Network'

    assert item.thumbnail[:5] == 'https'

    assert item.published[:4] == '2024'




def test_YouTubeVideo() -> None:
    """
    Perform various tests associated with relevant routines.
    """

    content = read_text(
        f'{SAMPLES}/videos'
        '/source.json')

    loaded = loads(content)

    assert isinstance(
        loaded, dict)

    source = loaded['items'][0]


    item = (
        YouTubeVideo(**source))


    attrs = lattrs(item)

    assert attrs == [
        'kind',
        'channel',
        'video',
        'title',
        'about',
        'thumbnail',
        'published']


    assert inrepr(
        'YouTubeVideo(kind',
        item)

    with raises(TypeError):
        hash(item)

    assert instr(
        "kind='video'",
        item)


    assert item.kind == 'video'

    assert item.channel == 'UCPNB7Hrq5oHl81EzG6x3BwA'

    assert item.video == '9h-vcAjRCz8'

    assert item.title == 'Validating encommon code'

    assert item.about
    assert item.about[:12] == 'Demonstrates'

    assert item.thumbnail[:5] == 'https'

    assert item.published[:4] == '2024'
