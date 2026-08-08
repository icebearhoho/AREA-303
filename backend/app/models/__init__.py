"""ORM models live here. Add one file per aggregate (user.py, idea.py, ...)."""

from app.models.channel_link import ChannelConnection
from app.models.idea import Idea

__all__ = ["ChannelConnection", "Idea"]
