from io import BytesIO

from src.gedcom_parser import parse_gedcom, decode_gedcom


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

def test_mixed_encoding_preserves_utf8_polish_characters():
    gedcom = (
        b"\xef\xbb\xbf"
        + """
0 @I1@ INDI
1 NAME Katarzyna /Zając/
1 BIRT
2 DATE 10 FEB 1895
2 PLAC Czeladź
""".encode("utf-8")
    )

    file = BytesIO(gedcom)

    people = parse_gedcom(file)

    assert len(people) == 1
    assert people[0].first_name == "Katarzyna"
    assert people[0].last_name == "Zając"
    assert people[0].birth_place == "Czeladź"

def test_mixed_utf8_and_cp1250_encoding():
    utf8_part = """
0 @I1@ INDI
1 NAME Katarzyna /Zając/
1 BIRT
2 PLAC Czeladź
""".encode("utf-8")

    cp1250_part = """
1 NOTE Łódź
""".encode("cp1250")

    raw_data = b"\xef\xbb\xbf" + utf8_part + cp1250_part

    text = decode_gedcom(raw_data)

    assert "Katarzyna" in text
    assert "Zając" in text
    assert "Czeladź" in text
    assert "Łódź" in text