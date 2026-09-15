class LinkError(Exception):
    """A Link failed to send, receive, create, or locate."""


class LinkTimeout(LinkError):
    """A send, receive, or link creation waited too long."""
