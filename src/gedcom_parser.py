from src.models import Person, Family


def decode_gedcom(
    raw_data: bytes,
    encoding: str | None = None
) -> str:

    # Encoding explicitly selected by the user
    if encoding:
        return raw_data.decode(encoding)

    # UTF-16 BOM
    if raw_data.startswith((b"\xff\xfe", b"\xfe\xff")):
        return raw_data.decode("utf-16")

    # Try normal UTF-8 first
    try:
        return raw_data.decode("utf-8-sig")
    except UnicodeDecodeError:
        pass

    # File appears to contain mostly UTF-8 with legacy bytes
    return decode_mixed_utf8_cp1250(raw_data)

def decode_mixed_utf8_cp1250(raw_data: bytes) -> str:
    """
    Decode a primarily UTF-8 file while recovering individual
    legacy Windows-1250 bytes.
    """

    if raw_data.startswith(b"\xef\xbb\xbf"):
        raw_data = raw_data[3:]

    text = raw_data.decode("utf-8", errors="surrogateescape")

    result = []
    legacy_bytes = bytearray()

    def flush_legacy_bytes():
        if legacy_bytes:
            result.append(
                legacy_bytes.decode("cp1250", errors="replace")
            )
            legacy_bytes.clear()

    for char in text:
        code = ord(char)

        if 0xDC80 <= code <= 0xDCFF:
            legacy_bytes.append(code - 0xDC00)
        else:
            flush_legacy_bytes()
            result.append(char)

    flush_legacy_bytes()

    return "".join(result)

def parse_gedcom(
    file,
    encoding: str | None = None,
) -> list[Person]:
    raw_data = file.getvalue()
    text = decode_gedcom(raw_data, encoding)
    lines = text.splitlines()

    people = parse_people(lines)
    families = parse_families(lines)

    link_family_relationships(
        people,
        families,
    )

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

def parse_people(lines: list[str]) -> list[Person]:
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

        # Start of a new individual
        if level == "0" and value == "INDI":
            if current_person is not None:
                people.append(current_person)

            current_person = Person(
                gedcom_id=tag
            )

            current_event = None
            continue

        # End of individual section
        if level == "0":
            if current_person is not None:
                people.append(current_person)
                current_person = None

            current_event = None
            continue

        # Ignore everything outside an INDI record
        if current_person is None:
            continue

        # Person-level data
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
                current_person.death_confirmed = True

        # Additional person/event data
        elif level == "2":
            if tag == "_MARNM":
                current_person.married_name = value.strip()

            elif current_event:
                if tag == "DATE":
                    set_event_date(
                        current_person,
                        current_event,
                        value,
                    )

                elif tag == "PLAC":
                    set_event_place(
                        current_person,
                        current_event,
                        value,
                    )

    # File may end directly after an INDI record
    if current_person is not None:
        people.append(current_person)

    return people

def parse_families(lines: list[str]) -> list[Family]:
    families = []
    current_family = None

    for line in lines:
        parts = line.strip().split(" ", 2)

        if len(parts) < 2:
            continue

        level = parts[0]
        tag = parts[1]
        value = parts[2] if len(parts) > 2 else ""

        if level == "0" and value == "FAM":
            if current_family is not None:
                families.append(current_family)

            current_family = Family(
                gedcom_id=tag
            )

            continue

        if current_family is None:
            continue

        if level == "1":
            if tag == "HUSB":
                current_family.husband_id = value

            elif tag == "WIFE":
                current_family.wife_id = value

            elif tag == "CHIL":
                current_family.children_ids.append(value)

    if current_family is not None:
        families.append(current_family)

    return families

def link_family_relationships(
    people: list[Person],
    families: list[Family],
) -> None:
    people_by_id = {
        person.gedcom_id: person
        for person in people
    }

    for family in families:
        husband = people_by_id.get(family.husband_id)
        wife = people_by_id.get(family.wife_id)

        # Link spouses
        if husband and wife:
            if wife.gedcom_id not in husband.spouse_ids:
                husband.spouse_ids.append(wife.gedcom_id)

            if husband.gedcom_id not in wife.spouse_ids:
                wife.spouse_ids.append(husband.gedcom_id)

        # Link parents and children
        for child_id in family.children_ids:
            child = people_by_id.get(child_id)

            if child is None:
                continue

            if husband:
                child.father_id = husband.gedcom_id

                if child.gedcom_id not in husband.children_ids:
                    husband.children_ids.append(child.gedcom_id)

            if wife:
                child.mother_id = wife.gedcom_id

                if child.gedcom_id not in wife.children_ids:
                    wife.children_ids.append(child.gedcom_id)