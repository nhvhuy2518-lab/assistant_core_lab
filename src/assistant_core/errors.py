"""Named exceptions used at service boundaries."""


class AssistantError(Exception):
    """Base class for errors raised by the assistant."""


class ConfigError(AssistantError):
    """Configuration is missing or invalid."""


class DataError(AssistantError):
    """A knowledge file is missing or malformed."""


class InvalidRequest(AssistantError):
    """The request cannot be processed as given."""


class ProviderError(AssistantError):
    """A response provider failed or returned an unusable result."""
