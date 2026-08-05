from src.models import Person


def get_children_with_partner(
    person: Person,
    partner: Person,
    people_by_id: dict[str, Person],
) -> list[Person]:
    shared_children_ids = (
        set(person.children_ids)
        & set(partner.children_ids)
    )

    return [
        people_by_id[child_id]
        for child_id in shared_children_ids
        if child_id in people_by_id
    ]