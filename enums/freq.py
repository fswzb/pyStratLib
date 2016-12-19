

from enum import Enum
from enum import unique

class StrEnum(str, Enum):
    pass

@unique
class Freq(StrEnum):
    MONTH = 'month'
    YEAR = 'year'
    WEEK = 'week'
