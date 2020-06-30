import re
import logging
from datetime import datetime
from enum import Enum, auto

__version__ = "0.0.1"

logger = logging.getLogger(__name__)

RSA_ID_LENGTH = 13
GENDER_FEMALE_MIN = 0
GENDER_FEMALE_MAX = 4999
GENDER_MALE_MIN = 5000
GENDER_MALE_MAX = 9999
CITIZENSHIP_SA_CITIZEN = 0
CITIZENSHIP_PERMANENT_RESIDENT = 1


class Gender(Enum):
    FEMALE = auto()
    MALE = auto()


class Citizenship(Enum):
    SA_CITIZEN = auto()
    PERMANENT_RESIDENT = auto()


class IdNumber:
    def __init__(self, value: str):
        self.value = value
        self.error = None
        self.date_of_birth = None
        self.gender = None
        self.citizenship = None
        self.parse()

    def clean(self):
        """Return the value without any whitespace."""
        return re.sub(r"\s", "", self.value or "")

    def parse(self):
        """Parse the value and validate against the RSA ID number format."""
        self.error = None
        self.date_of_birth = None
        self.gender = None
        self.citizenship = None

        value = self.clean()
        if not value:
            self.error = f"'{value}' is not a valid RSA ID number!"
            return

        if not value.isdigit():
            self.error = f"'{value}' contains non-digit characters!"
            return

        if len(value) != RSA_ID_LENGTH:
            self.error = f"'{value}' is not {RSA_ID_LENGTH} digits!"
            return

        year = value[0:2]
        month = value[2:4]
        day = value[4:6]
        try:
            self.date_of_birth = datetime.strptime(
                f"{year}{month}{day}", "%y%m%d"
            )
        except ValueError:
            self.error = f"'{value}' contains an invalid date of birth!"
            logger.debug(self.error, exc_info=True)
            return

        gender = int(value[6:10])
        if gender >= GENDER_FEMALE_MIN and gender <= GENDER_FEMALE_MAX:
            self.gender = Gender.FEMALE
        else:
            self.gender = Gender.MALE

        citizenship = int(value[10])
        if citizenship == CITIZENSHIP_SA_CITIZEN:
            self.citizenship = Citizenship.SA_CITIZEN
        elif citizenship == CITIZENSHIP_PERMANENT_RESIDENT:
            self.citizenship = Citizenship.PERMANENT_RESIDENT
        else:
            self.error = f"Invalid citizenship indicator: '{citizenship}'!"
            return

    @property
    def valid(self) -> bool:
        """Return True if there is not error, False otherwise."""
        return not self.error

    def __repr__(self):
        return self.clean()


def parse(value: str, raise_exc: bool = True) -> IdNumber:
    """Parse `value` and validate against the RSA ID number format.

    Args:
        value: ID number string to parse and validate.

    Returns:
        A new `IdNumber` instance.

    Raises:
        ValueError: If the ID number is invalid and `raise_exc` is True.

    Examples:
        >>> import rsaidnumber
        >>> value = '1234567890123'
        >>> id_number = rsaidnumber.parse(value)

    """
    id_number = IdNumber(value)
    id_number.parse()
    if not id_number.valid and raise_exc:
        raise ValueError(id_number.error)
    return id_number
