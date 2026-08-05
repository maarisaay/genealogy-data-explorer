from io import BytesIO

from src.gedcom_parser import parse_gedcom


def test_parse_person():
    gedcom = b"""
0 @I1@ INDI
1 NAME Katarzyna /Zajac/
1 SEX F
1 BIRT
2 DATE 10 FEB 1895
2 PLAC Tarnowskie Gory
"""

    file = BytesIO(gedcom)

    people = parse_gedcom(file)

    assert len(people) == 1

    person = people[0]

    assert person.gedcom_id == "@I1@"
    assert person.first_name == "Katarzyna"
    assert person.last_name == "Zajac"
    assert person.sex == "F"
    assert person.birth_date == "10 FEB 1895"
    assert person.birth_year == 1895
    assert person.birth_place == "Tarnowskie Gory"

def test_parse_cp1250_person():
    gedcom = """
0 @I1@ INDI
1 NAME Łukasz /Żółć/
1 SEX M
1 BIRT
2 DATE 12 MAY 1895
2 PLAC Łódź
""".encode("cp1250")

    file = BytesIO(gedcom)

    people = parse_gedcom(file, encoding="cp1250")

    assert len(people) == 1
    assert people[0].first_name == "Łukasz"
    assert people[0].last_name == "Żółć"
    assert people[0].birth_place == "Łódź"