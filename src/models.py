from dataclasses import dataclass, field


@dataclass
class Person:
    gedcom_id: str
    first_name: str | None = None
    last_name: str | None = None
    married_name: str | None = None
    sex: str | None = None

    birth_date: str | None = None
    birth_year: int | None = None
    birth_place: str | None = None

    death_date: str | None = None
    death_year: int | None = None
    death_place: str | None = None
    death_confirmed: bool = False

    father_id: str | None = None
    mother_id: str | None = None

    spouse_ids: list[str] = field(default_factory=list)
    children_ids: list[str] = field(default_factory=list)

@dataclass
class Family:
    gedcom_id: str
    husband_id: str | None = None
    wife_id: str | None = None
    children_ids: list[str] = field(default_factory=list)