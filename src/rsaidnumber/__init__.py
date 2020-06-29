import re
import logging
from datetime import datetime
from enum import Enum

__version__ = "0.0.1"

logger = logging.getLogger(__name__)

RSA_ID_LENGTH = 13


class Gender(Enum):
    FEMALE = "4"
    MALE = "5"


class Citizenship(Enum):
    CITIZEN = "0"
    RESIDENT = "1"


def validate(id_number: str):
    """Validate `id_number` against the RSA ID number format.

    Args:
        id_number: ID number to validate.

    Raises:
        ValueError: If the ID number is invalid.

    Examples:
        >>> import rsaidnumber
        >>> rsaidnumber.validate('1234567890123')

    """
    if not id_number:
        raise ValueError(f"'{id_number}' is not a valid RSA ID number!")

    id_number = re.sub(r"\s", "", id_number)

    if not id_number.isdigit():
        raise ValueError(f"'{id_number}' contains non-digit characters!")

    if len(id_number) != RSA_ID_LENGTH:
        raise ValueError(f"'{id_number}' is not {RSA_ID_LENGTH} digits!")

    year = id_number[0:2]
    month = id_number[2:4]
    day = id_number[4:6]
    try:
        datetime.strptime(f"{month}{year}{day}", "%y%m%d")
    except ValueError:
        msg = f"'{id_number}' contains an invalid date of birth!"
        logger.exception(msg, id_number)
        raise ValueError(msg)
