from datetime import datetime

import pytest

import rsaidnumber


def test_id_number_clean():
    id_number = rsaidnumber.IdNumber(" t  es t")
    assert id_number.clean() == "test"


def test_id_number_str():
    id_number = rsaidnumber.IdNumber(" test ")
    assert str(id_number) == id_number.clean()


def test_id_number_none():
    id_number = rsaidnumber.IdNumber(None)
    assert not id_number.valid
    assert id_number.error == "'' is not a valid RSA ID number!"


def test_id_number_empty():
    id_number = rsaidnumber.IdNumber("")
    assert not id_number.valid
    assert id_number.error == "'' is not a valid RSA ID number!"


def test_id_number_non_digits():
    id_number = rsaidnumber.IdNumber(" a ")
    assert not id_number.valid
    assert id_number.error == "'a' contains non-digit characters!"


def test_id_number_incorrect_length():
    id_number = rsaidnumber.IdNumber("123")
    assert not id_number.valid
    assert id_number.error == "'123' is not 13 digits!"


def test_id_number_invalid_date_of_birth():
    id_number = rsaidnumber.IdNumber("0000001234567")
    assert not id_number.valid
    assert (
        id_number.error == "'0000001234567' contains an invalid date of birth!"
    )


def test_id_number_old_date_of_birth():
    id_number = rsaidnumber.IdNumber("5903198389082")
    assert id_number.valid
    assert id_number.date_of_birth < datetime.now()


def test_id_number_valid():
    id_number = rsaidnumber.IdNumber("8012215312080")
    expected_date_of_birth = datetime(year=1980, month=12, day=21)
    expected_gender = rsaidnumber.Gender.MALE
    expected_citizenship = rsaidnumber.Citizenship.SA_CITIZEN
    assert id_number.valid
    assert not id_number.error
    assert id_number.date_of_birth == expected_date_of_birth
    assert id_number.gender == expected_gender
    assert id_number.citizenship == expected_citizenship


def test_parse_valid():
    id_number = rsaidnumber.parse("8012215312080")
    assert id_number.valid


def test_parse_invalid():
    with pytest.raises(ValueError):
        rsaidnumber.parse("invalid_id_number")


def test_parse_invalid_no_exception():
    id_number = rsaidnumber.parse("invalid_id_number", raise_exc=False)
    assert not id_number.valid
