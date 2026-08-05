from src.family_relationships import get_children_with_partner
from src.models import Person


def test_get_children_with_partner():
    child_1 = Person(
        gedcom_id="@I3@",
        first_name="Anna",
    )

    child_2 = Person(
        gedcom_id="@I4@",
        first_name="Jan",
    )

    person = Person(
        gedcom_id="@I1@",
        children_ids=["@I3@", "@I4@"],
    )

    partner = Person(
        gedcom_id="@I2@",
        children_ids=["@I3@"],
    )

    people_by_id = {
        child_1.gedcom_id: child_1,
        child_2.gedcom_id: child_2,
    }

    children = get_children_with_partner(
        person,
        partner,
        people_by_id,
    )

    assert len(children) == 1
    assert children[0].gedcom_id == "@I3@"