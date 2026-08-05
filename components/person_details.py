import streamlit as st

from src.person_status import get_living_status


def get_display_name(person) -> str:
    if person.married_name and person.last_name:
        return (
            f"{person.first_name} "
            f"{person.married_name} "
            f"(née {person.last_name})"
        )

    return " ".join(
        part
        for part in [person.first_name, person.last_name]
        if part
    )

def select_related_person(
    person_id: str,
    source_id: str,
    section: str,
) -> None:
    st.session_state.selected_person_id = person_id
    st.session_state.related_source_id = source_id
    st.session_state.related_section = section

def replace_related_person(person_id: str) -> None:
    st.session_state.selected_person_id = person_id

def close_related_person() -> None:
    st.session_state.selected_person_id = None
    st.session_state.related_section = None

def show_related_person(
    source_person,
    people,
    key_prefix: str,
    navigation_source_id: str,
    section: str,
) -> None:
    is_selected_section = (
        st.session_state.related_source_id == source_person.gedcom_id
        and st.session_state.related_section == section
        and st.session_state.selected_person_id is not None
    )

    if not is_selected_section:
        return

    selected_person = next(
        (
            person
            for person in people
            if person.gedcom_id
            == st.session_state.selected_person_id
        ),
        None,
    )

    if selected_person is None:
        return

    st.divider()

    header_col, close_col = st.columns([5, 1])

    with header_col:
        st.markdown(
            f"##### {get_display_name(selected_person)}"
        )

    with close_col:
        st.button(
            "✕ Close",
            key=f"{key_prefix}_close_{section}",
            on_click=close_related_person,
        )

    show_person_details(
        selected_person,
        people,
        key_prefix=(
            f"{key_prefix}_{section}_related_"
            f"{selected_person.gedcom_id}"
        ),
        navigation_source_id=navigation_source_id,
        is_related_view=True,
    )

def show_related_person_button(
    target_person,
    label: str,
    key: str,
    navigation_source_id: str,
    section: str,
    is_related_view: bool,
) -> None:
    if is_related_view:
        st.button(
            label,
            key=key,
            type="tertiary",
            on_click=replace_related_person,
            args=(target_person.gedcom_id,),
        )

    else:
        st.button(
            label,
            key=key,
            type="tertiary",
            on_click=select_related_person,
            args=(
                target_person.gedcom_id,
                navigation_source_id,
                section,
            ),
        )

def show_person_details(
    person,
    people,
    key_prefix: str,
    navigation_source_id: str,
    is_related_view: bool = False,
):
    status = get_living_status(person)

    sex_labels = {
        "F": "Female",
        "M": "Male",
    }

    sex = sex_labels.get(person.sex, "Unknown")

    people_by_id = {
        p.gedcom_id: p
        for p in people
    }

    father = (
        people_by_id.get(person.father_id)
        if person.father_id
        else None
    )

    mother = (
        people_by_id.get(person.mother_id)
        if person.mother_id
        else None
    )

    partners = [
        people_by_id[spouse_id]
        for spouse_id in person.spouse_ids
        if spouse_id in people_by_id
    ]

    with st.container(border=True):
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### 🌱 Birth")

            st.markdown(
                f"**Date**  \n"
                f"{person.birth_date or 'Unknown'}"
            )

            st.markdown(
                f"**Place**  \n"
                f"{person.birth_place or 'Unknown'}"
            )

        with col2:
            st.markdown("#### 🕯️ Death")

            st.markdown(
                f"**Date**  \n"
                f"{person.death_date or 'Unknown'}"
            )

            st.markdown(
                f"**Place**  \n"
                f"{person.death_place or 'Unknown'}"
            )

        st.divider()

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(
                f"**Sex**  \n"
                f"{sex}"
            )

        with col2:
            st.markdown(
                f"**Status**  \n"
                f"{status}"
            )

        with col3:
            st.markdown(
                f"**GEDCOM ID**  \n"
                f"`{person.gedcom_id}`"
            )

        st.divider()

        st.markdown("#### 👪 Parents")

        father_col, mother_col = st.columns(2)

        with father_col:
            st.markdown("**Father**")

            if father:
                father_name = get_display_name(father)

                show_related_person_button(
                    target_person=father,
                    label=f"{father_name} →",
                    key=(
                        f"{key_prefix}_father_"
                        f"{person.gedcom_id}_"
                        f"{father.gedcom_id}"
                    ),
                    navigation_source_id=navigation_source_id,
                    section="parents",
                    is_related_view=is_related_view,
                )
            else:
                st.caption("Not recorded")

        with mother_col:
            st.markdown("**Mother**")

            if mother:
                mother_name = get_display_name(mother)

                show_related_person_button(
                    target_person=mother,
                    label=f"{mother_name} →",
                    key=(
                        f"{key_prefix}_mother_"
                        f"{person.gedcom_id}_"
                        f"{mother.gedcom_id}"
                    ),
                    navigation_source_id=navigation_source_id,
                    section="parents",
                    is_related_view=is_related_view,
                )
            else:
                st.caption("Not recorded")

        show_related_person(
            source_person=person,
            people=people,
            key_prefix=key_prefix,
            navigation_source_id=navigation_source_id,
            section="parents",
        )

        st.divider()

        st.markdown("#### 💍 Marital status")

        if partners:
            for index, partner in enumerate(partners):
                partner_name = get_display_name(partner)

                col1, col2 = st.columns([1, 3])

                with col1:
                    if index == 0:
                        st.markdown("**Married to**")

                with col2:
                    show_related_person_button(
                        target_person=partner,
                        label=f"{partner_name} →",
                        key=(
                            f"{key_prefix}_partner_"
                            f"{person.gedcom_id}_"
                            f"{partner.gedcom_id}"
                        ),
                        navigation_source_id=navigation_source_id,
                        section="partner",
                        is_related_view=is_related_view,
                    )
        else:
            st.markdown("**No partner recorded**")



