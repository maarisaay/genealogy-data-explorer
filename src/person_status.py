from datetime import datetime

from src.models import Person


def get_living_status(person: Person) -> str:
    if person.death_confirmed:
        return "Deceased"

    if person.birth_year is None:
        return "Unknown"

    current_year = datetime.now().year
    estimated_age = current_year - person.birth_year

    if estimated_age < 0:
        return "Unknown"

    if estimated_age <= 110:
        return "Likely living"

    return "Unknown"