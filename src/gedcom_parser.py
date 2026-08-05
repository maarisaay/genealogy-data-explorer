from charset_normalizer import from_bytes

from src.models import Person

def decode_gedcom(
    raw_data: bytes,
    encoding: str | None = None
) -> str:

    # Encoding explicitly selected by the user
    if encoding:
        return raw_data.decode(encoding)

    # UTF-8 BOM
    if raw_data.startswith(b"\xef\xbb\xbf"):
        try:
            return raw_data.decode("utf-8-sig")
        except UnicodeDecodeError:
            pass

    # UTF-16 BOM
    if raw_data.startswith((b"\xff\xfe", b"\xfe\xff")):
        try:
            return raw_data.decode("utf-16")
        except UnicodeDecodeError:
            pass

    # Standard UTF-8
    try:
        return raw_data.decode("utf-8")
    except UnicodeDecodeError:
        pass

    # Automatic detection for legacy files
    detected = from_bytes(raw_data).best()

    if detected is None:
        raise ValueError("Unable to determine GEDCOM file encoding.")

    return str(detected)

def parse_gedcom(
    file,
    encoding: str | None = None
) -> list[Person]:
    """
    Parse a GEDCOM file and return a list of Person objects.
    """
    raw_data = file.read()
    text = decode_gedcom(raw_data, encoding)
    lines = text.splitlines()

    people = []
    current_person = None
    current_event = None

    for line in lines:
        parts = line.strip().split(" ", 2)

        if len(parts) < 2:
            continue

        level = parts[0]
        tag = parts[1]
        value = parts[2] if len(parts) > 2 else ""

        # Start of a new individual record
        if level == "0" and value == "INDI":
            if current_person is not None:
                people.append(current_person)

            current_person = Person(
                gedcom_id=tag
            )

            current_event = None
            continue

        if current_person is None:
            continue

        # Main person fields
        if level == "1":
            current_event = None

            if tag == "NAME":
                parse_name(current_person, value)

            elif tag == "SEX":
                current_person.sex = value

            elif tag == "BIRT":
                current_event = "birth"

            elif tag == "DEAT":
                current_event = "death"

        # Event details
        elif level == "2" and current_event:
            if tag == "DATE":
                set_event_date(current_person, current_event, value)

            elif tag == "PLAC":
                set_event_place(current_person, current_event, value)

    if current_person is not None:
        people.append(current_person)

    return people

def parse_name(person: Person, value: str) -> None:
    """
    Parse GEDCOM name format:
    John /Smith/
    """

    if "/" in value:
        parts = value.split("/")

        person.first_name = parts[0].strip()
        person.last_name = parts[1].strip()
    else:
        person.first_name = value.strip()


def set_event_date(person: Person, event: str, value: str) -> None:
    year = extract_year(value)

    if event == "birth":
        person.birth_date = value
        person.birth_year = year

    elif event == "death":
        person.death_date = value
        person.death_year = year

def set_event_place(person: Person, event: str, value: str) -> None:
    if event == "birth":
        person.birth_place = value

    elif event == "death":
        person.death_place = value

def extract_year(date: str) -> int | None:
    for part in date.split():
        if part.isdigit() and len(part) == 4:
            return int(part)

    return None