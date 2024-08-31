"""
Functions and routines associated with Enasis Network Remote Connect.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from .discord.test import DSCClientSocket
from .discord.test import client_dscsock
from .irc.test import IRCClientSocket
from .irc.test import client_ircsock



__all__ = [
    'IRCClientSocket',
    'client_ircsock',
    'DSCClientSocket',
    'client_dscsock']
