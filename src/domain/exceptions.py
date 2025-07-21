"""Application exceptions"""


class MissingConfiguration(BaseException):
    """Raised when the configuration file is missing"""


class IncompleteConfiguration(BaseException):
    """Raised when mandatory information from the configuration is missing"""
