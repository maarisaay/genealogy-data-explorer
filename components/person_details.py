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

def select_related_person(person_id, source_id):
    st.session_state.selected_person_id = person_id
    st.session_state.related_source_id = source_id

def show_person_details(
    person,
    people,
    key_prefix,
    navigation_source_id,
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

        st.markdown("#### 💍 Marital status")

        if partners:
            for index, partner in enumerate(partners):
                partner_name = get_display_name(partner)

                col1, col2 = st.columns([1, 3])

                with col1:
                    if index == 0:
                        st.markdown("**Married to**")

                with col2:
                    st.button(
                        f"{partner_name} →",
                        key=(
                            f"{key_prefix}_partner_"
                            f"{person.gedcom_id}_"
                            f"{partner.gedcom_id}"
                        ),
                        type="tertiary",
                        on_click=select_related_person,
                        args=(
                            partner.gedcom_id,
                            navigation_source_id,
                        ),
                    )

        else:
            st.markdown("**No partner recorded**")