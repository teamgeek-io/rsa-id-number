import re
from datetime import date, timedelta
from random import choice, randrange

from .constants import (
    DATE_OF_BIRTH_FORMAT,
    GENDER_FEMALE_MIN,
    GENDER_FEMALE_MAX,
    GENDER_MALE_MIN,
    GENDER_MALE_MAX,
    SA_CITIZEN_DIGIT,
    PERMANENT_RESIDENT_DIGIT,
    RACE_DIGIT,
    Gender,
    Citizenship,
)


def calculate_checksum_digit(numbers: str) -> int:
    """Calculate the checksum digit for the given number sequence.

    Use the Luhn algorithm to calculate a checksum digit, which can be used
    for basic error detection in the number sequence.

    Args:
        numbers: Number sequence to calculate the checksum for.

    Returns:
        The checksum digit.

    """
    digits = [int(d) for d in re.sub(r"\D", "", numbers)]
    digits.reverse()
    sum = 0
    for index, digit in enumerate(digits):
        if index % 2 == 0:
            digit = digit * 2
            if digit > 9:
                digit = digit - 9
        sum = sum + digit
    return sum * 9 % 10


def generate_date_of_birth(start=date(1920, 1, 1), end=None):
    """Return a random date in a given period.

    Args:
        start: Start date.
        end: End date.

    Returns:
        Random date in the given range.

    """
    if not end:
        end = date.today()
    difference = end - start
    days = randrange(difference.days)
    return start + timedelta(days=days)


def generate_gender_digits(gender: Gender) -> str:
    """Return a random sequence of digits representing the given gender.

    Female: 0000 - 4999
    Male: 5000 - 9999

    Args:
        gender: Gender to generate digits for.

    Returns:
        Sequence of digits for the given gender.

    """
    if gender == Gender.FEMALE:
        number = randrange(GENDER_FEMALE_MIN, GENDER_FEMALE_MAX + 1)
    else:
        number = randrange(GENDER_MALE_MIN, GENDER_MALE_MAX + 1)
    return f"{number:03d}"


def make_id_number(
    date_of_birth: date, gender: Gender, citizenship: Citizenship
) -> str:
    """Construct a valid RSA ID number from the given information.

    Args:
        date_of_birth: The date of birth.
        gender: The gender indicator.
        citizenship: The citizenship indicator.

    Returns:
        A new valid RSA ID number.

    """
    date_of_birth_digits = date_of_birth.strftime(DATE_OF_BIRTH_FORMAT)
    gender_digits = generate_gender_digits(gender)
    if citizenship == Citizenship.SA_CITIZEN:
        citizenship_digit = SA_CITIZEN_DIGIT
    else:
        citizenship_digit = PERMANENT_RESIDENT_DIGIT
    digits = "".join(
        [date_of_birth_digits, gender_digits, citizenship_digit, RACE_DIGIT]
    )
    checksum_digit = calculate_checksum_digit(digits)
    return f"{digits}{checksum_digit}"


def generate(
    date_of_birth: date = None,
    gender: Gender = None,
    citizenship: Citizenship = None,
) -> str:
    """Generate a valid RSA ID number.

    Generate random values for any of the missing information.

    Args:
        date_of_birth: The date of birth.
        gender: The gender indicator.
        citizenship: The citizenship indicator.

    Returns:
        A new valid RSA ID number.

    Examples:
        >>> import rsaidnumber
        >>> rsaidnumber.generate()
        8012215312080

    """
    if not date_of_birth:
        date_of_birth = generate_date_of_birth()
    if not gender:
        gender = choice([Gender.MALE, Gender.FEMALE])
    if not citizenship:
        citizenship = choice(
            [Citizenship.SA_CITIZEN, Citizenship.PERMANENT_RESIDENT]
        )
    return make_id_number(
        date_of_birth, gender=gender, citizenship=citizenship
    )
