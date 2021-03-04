import logging
import re
from datetime import datetime

from .constants import (
    DATE_OF_BIRTH_FORMAT,
    GENDER_FEMALE_MAX,
    GENDER_FEMALE_MIN,
    PERMANENT_RESIDENT_DIGIT,
    RSA_ID_LENGTH,
    SA_CITIZEN_DIGIT,
    Citizenship,
    Gender,
)
from .random import generate

__version__ = "0.0.3"

__all__ = ["Gender", "Citizenship", "IdNumber", "parse", "generate"]

logger = logging.getLogger(__name__)


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
                f"{year}{month}{day}", DATE_OF_BIRTH_FORMAT
            )

            if self.date_of_birth > datetime.now():
                correct_year = self.date_of_birth.year - 100

                self.date_of_birth = self.date_of_birth.replace(
                    year=correct_year
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

        citizenship = value[10]
        if citizenship == SA_CITIZEN_DIGIT:
            self.citizenship = Citizenship.SA_CITIZEN
        elif citizenship == PERMANENT_RESIDENT_DIGIT:
            self.citizenship = Citizenship.PERMANENT_RESIDENT
        else:
            self.error = f"Invalid citizenship indicator: '{citizenship}'!"
            return

        digits = [int(d) for d in value]
        digits.reverse()
        sum = 0
        for index, digit in enumerate(digits):
            if (index + 1) % 2 == 0:
                digit = digit * 2
                if digit > 9:
                    digit = digit - 9
            sum = sum + digit

        if not sum % 10 == 0:
            self.error = f"'{value}' contains an invalid checksum digit!"
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
