import pytest
import rsaidnumber


def test_validate_none():
    id_number = None
    with pytest.raises(
        ValueError, match="'None' is not a valid RSA ID number!"
    ):
        rsaidnumber.validate(id_number)


def test_validate_empty():
    id_number = ""
    with pytest.raises(ValueError, match="'' is not a valid RSA ID number!"):
        rsaidnumber.validate(id_number)


def test_validate_non_digits():
    id_number = " a "
    with pytest.raises(ValueError, match="'a' contains non-digit characters!"):
        rsaidnumber.validate(id_number)


def test_validate_incorrect_length():
    id_number = "123"
    with pytest.raises(ValueError, match="'123' is not 13 digits!"):
        rsaidnumber.validate(id_number)


def test_validate_invalid_date_of_birth():
    id_number = "0000001234567"
    with pytest.raises(
        ValueError, match="'0000001234567' contains an invalid date of birth!"
    ):
        rsaidnumber.validate(id_number)


def test_validate_valid_check_digit():
    id_number = "8804085800081"
    rsaidnumber.validate(id_number)


def test_validate_invalid_check_digit():
    id_number = "8804085800124"
    with pytest.raises(
        ValueError, match="'8804085800124' check sum does not match!"
    ):
        rsaidnumber.validate(id_number)
