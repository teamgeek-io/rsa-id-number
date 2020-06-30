from rsaidnumber import (
    calculate_check_digit,
    generate_dummy_number,
    generate_random_dummy_number,
)


def test_calculate_check_digit_result():
    assert calculate_check_digit("12345abc") == 5
    assert calculate_check_digit("1728378274") == 0
    assert calculate_check_digit("872847gcsah2783471") == 1
    assert calculate_check_digit("93718237177284") == 3


def test_generate_dummy_id_number_result():
    assert generate_dummy_number() == "9310195896083"
    assert generate_dummy_number(sequence="940") == "9310195940089"


def test_generate_random_dummy_id_number():
    assert generate_random_dummy_number() is not None
