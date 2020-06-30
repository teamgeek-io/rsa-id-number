import re
import logging
from datetime import datetime
from random import randrange, choice
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


def calculate_check_digit(digits):
    digits_arr = list(re.sub(r"\D", "", digits))
    num_digits = list(map(lambda d: int(d), digits_arr))

    num_digits.reverse()
    check_sum = 0
    for idx, d in enumerate(num_digits):
        if idx % 2 == 0:
            d = d * 2
            if d > 9:
                d = d - 9
        check_sum = check_sum + d

    return check_sum * 9 % 10


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
        datetime.strptime(f"{year}{month}{day}", "%y%m%d")
    except ValueError:
        msg = f"'{id_number}' contains an invalid date of birth!"
        logger.debug(msg, id_number)
        raise ValueError(msg)

    check_digit = id_number[-1:]
    number_without_check_digit = id_number[:-1]

    if int(check_digit) != calculate_check_digit(number_without_check_digit):
        raise ValueError(f"'{id_number}' check sum does not match!")


def generate_dummy_number(
    year="93",
    month="10",
    day="19",
    gender=Gender.MALE,
    citizenship=Citizenship.CITIZEN,
    sequence="896",
):
    values = [year, month, day, gender.value, sequence, citizenship.value, "8"]

    no_check_digit = "".join(values)
    id_number = no_check_digit + str(calculate_check_digit(no_check_digit))

    return id_number


def generate_random_dummy_number(
    year=None,
    month=None,
    day=None,
    gender=None,
    citizenship=None,
    sequence=None,
):
    if year is None:
        year = str(randrange(20, 99))
    if month is None:
        month_num = randrange(1, 12)
        month = f"{month_num:02d}"
    if day is None:
        day_num = randrange(1, 31)
        day = f"{day_num:02d}"
    if gender is None:
        gender = choice([Gender.MALE, Gender.FEMALE])
    if citizenship is None:
        citizenship = choice([Citizenship.CITIZEN, Citizenship.RESIDENT])
    if sequence is None:
        sequence_num = randrange(0, 999)
        sequence = f"{sequence_num:03d}"

    return generate_dummy_number(
        year=year,
        month=month,
        day=day,
        gender=gender,
        citizenship=citizenship,
        sequence=sequence,
    )
