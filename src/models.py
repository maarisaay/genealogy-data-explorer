from dataclasses import dataclass, field


@dataclass
class Person:
    gedcom_id: str
    first_name: str | None = None
    last_name: str | None = None
    sex: str | None = None

    birth_date: str | None = None
    birth_year: int | None = None
    birth_place: str | None = None

    death_date: str | None = None
    death_year: int | None = None
    death_place: str | None = None

    father_id: str | None = None
    mother_id: str | None = None

    spouse_ids: list[str] = field(default_factory=list)
    children_ids: list[str] = field(default_factory=list)