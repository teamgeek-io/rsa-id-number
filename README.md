
# rsa-id-number

Utilities for working with South African ID numbers.

## RSA ID Number Format

```
+-------------------------+
|8|8|0|1|2|3|5|1|1|1|0|8|8|
+-------------------------+
|Y|Y|M|M|D|D|S|S|S|S|C|A|Z|
+-------------------------+
```

- **YYMMDD**: The first 6 digits represent the date of birth (*23 January 1988*)
- **SSSS**: The next 4 digits are used to define the individual's gender (*Male*)
  - *Female*: 0000 - 4999
  - *Male*: 5000 - 9999
- **C**: The next digit is used to classify citizenship (*SA citizen*)
  - *SA citizen*: 0
  - *Permanent resident*: 1
- **A**: The next digit was used until 1980s to classify race
- **Z**: The last digit is used as a checksum digit to verify the number (*Valid*)

# Installation

```
$ pip install rsa-id-number
```

# Usage

```
>>> import rsaidnumber
>>> id_number = rsaidnumber.parse('8801235111088')
>>> id_number.valid
True
>>> id_number.date_of_birth
datetime.datetime(1988, 1, 23, 0, 0)
>>> id_number.gender
<Gender.MALE: 2>
>>> id_number.citizenship
<Citizenship.SA_CITIZEN: 1>
>>> id_number = rsaidnumber.parse('8801235111080')
Traceback (most recent call last):
  ...
ValueError: '8801235111080' contains an invalid checksum digit!
>>> id_number = rsaidnumber.parse('8801235111080', False)
>>> id_number.valid
False
```

# Contributing

Setup your development environment by running:

```
$ make
```

this will create a new Python *virtualenv*, install all necessary dependencies and run the tests.
