from src.models import Person
from src.search import search_people


def test_search_by_last_name():
    people = [
        Person(
            gedcom_id="@I1@",
            first_name="Katarzyna",
            last_name="Zając",
            birth_year=1895,
        ),
        Person(
            gedcom_id="@I2@",
            first_name="Jan",
            last_name="Kowalski",
            birth_year=1901,
        ),
    ]

    results = search_people(
        people,
        last_name="Zaj",
    )

    assert len(results) == 1
    assert results[0].first_name == "Katarzyna"

def test_search_woman_by_maiden_and_married_name():
    person = Person(
        gedcom_id="@I1@",
        first_name="Katarzyna",
        last_name="Zając",
        married_name="Dzwonnik",
    )

    people = [person]

    maiden_results = search_people(
        people,
        last_name="Zając",
    )

    married_results = search_people(
        people,
        last_name="Dzwonnik",
    )

    assert len(maiden_results) == 1
    assert len(married_results) == 1