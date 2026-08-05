from src.models import Person


def search_people(
    people: list[Person],
    first_name: str = "",
    last_name: str = "",
    birth_year: int | None = None,
    birth_place: str = "",
) -> list[Person]:
    results = []

    for person in people:
        if first_name:
            if not person.first_name or first_name.lower() not in person.first_name.lower():
                continue

        if last_name:
            query = last_name.lower()

            maiden_match = (
                    person.last_name
                    and query in person.last_name.lower()
            )

            married_match = (
                    person.married_name
                    and query in person.married_name.lower()
            )

            if not maiden_match and not married_match:
                continue

        if birth_year is not None:
            if person.birth_year != birth_year:
                continue

        if birth_place:
            if not person.birth_place or birth_place.lower() not in person.birth_place.lower():
                continue

        results.append(person)

    return results