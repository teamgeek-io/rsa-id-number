from enum import Enum, auto

RSA_ID_LENGTH = 13
DATE_OF_BIRTH_FORMAT = "%y%m%d"
GENDER_FEMALE_MIN = 0
GENDER_FEMALE_MAX = 4999
GENDER_MALE_MIN = 5000
GENDER_MALE_MAX = 9999
SA_CITIZEN_DIGIT = "0"
PERMANENT_RESIDENT_DIGIT = "1"
RACE_DIGIT = "8"  # used until 1980s


class Gender(Enum):
    FEMALE = auto()
    MALE = auto()


class Citizenship(Enum):
    SA_CITIZEN = auto()
    PERMANENT_RESIDENT = auto()
