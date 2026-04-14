"""Exceptions beim Zugriffsschutz."""


class AuthorizationError(Exception):
    """Exception, falls der "Authorization"-String fehlt oder fehlerhaft ist."""
