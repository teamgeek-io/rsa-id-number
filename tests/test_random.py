from datetime import date

from rsaidnumber import Citizenship, Gender, random, parse


def test_calculate_checksum_digit():
    assert random.calculate_checksum_digit("12345abc") == 5
    assert random.calculate_checksum_digit("1728378274") == 0
    assert random.calculate_checksum_digit("872847gcsah2783471") == 1
    assert random.calculate_checksum_digit("93718237177284") == 3


def test_generate_date_of_birth():
    date_of_birth = random.generate_date_of_birth()
    assert date_of_birth


def test_generate_gender_digits_female():
    digits = random.generate_gender_digits(Gender.FEMALE)
    assert len(digits) == 4
    assert int(digits[0]) < 5


def test_generate_gender_digits_male():
    digits = random.generate_gender_digits(Gender.MALE)
    assert len(digits) == 4
    assert int(digits[0]) >= 5


def test_make_id_number(mocker):
    generate_gender_digits_mock = mocker.patch(
        "rsaidnumber.random.generate_gender_digits", return_value="5312"
    )
    expected_id_number = "8012215312080"
    id_number = random.make_id_number(
        date(1980, 12, 21), Gender.MALE, Citizenship.SA_CITIZEN
    )
    generate_gender_digits_mock.assert_called_with(Gender.MALE)
    assert id_number == expected_id_number


def test_generate():
    id_number = random.generate()
    id_number = parse(id_number, False)
    assert id_number.valid


def test_generate_with_info(mocker):
    mocker.patch(
        "rsaidnumber.random.generate_gender_digits", return_value="5312"
    )
    expected_id_number = "8012215312080"
    id_number = random.generate(
        date(1980, 12, 21), Gender.MALE, Citizenship.SA_CITIZEN
    )
    assert id_number == expected_id_number
