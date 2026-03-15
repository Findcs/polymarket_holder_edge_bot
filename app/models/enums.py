from enum import StrEnum


class TokenSide(StrEnum):
    YES = "YES"
    NO = "NO"


class SmartSide(StrEnum):
    YES = "YES"
    NO = "NO"
    NONE = "NONE"


class PositionStatus(StrEnum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"
    RESOLVED = "RESOLVED"
    UNKNOWN = "UNKNOWN"
