from src.models import Person


def get_relationship_status(person: Person) -> str:
    if person.spouse_ids:
        return "Partnered"

    return "No partner recorded"