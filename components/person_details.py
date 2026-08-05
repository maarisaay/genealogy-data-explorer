import streamlit as st

from src.person_status import get_living_status
from src.family_relationships import get_children_with_partner

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

def toggle_children(children_key: str) -> None:
    expanded_keys = st.session_state.expanded_children_keys

    if children_key in expanded_keys:
        expanded_keys.remove(children_key)
    else:
        expanded_keys.add(children_key)

    st.session_state.expanded_children_keys = expanded_keys

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
        # Inside an already opened related-person panel:
        # replace its contents.
        st.button(
            label,
            key=key,
            type="tertiary",
            on_click=replace_related_person,
            args=(target_person.gedcom_id,),
        )

    else:
        # Inside the main profile:
        # open a related-person panel in the selected section.
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
) -> None:
    status = get_living_status(person)

    sex_labels = {
        "F": "Female",
        "M": "Male",
    }
    sex = sex_labels.get(person.sex, "Unknown")

    people_by_id = {
        current_person.gedcom_id: current_person
        for current_person in people
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
        # Birth and death
        birth_col, death_col = st.columns(2)

        with birth_col:
            st.markdown("#### 🌱 Birth")

            st.markdown(
                f"**Date**  \n"
                f"{person.birth_date or 'Unknown'}"
            )

            st.markdown(
                f"**Place**  \n"
                f"{person.birth_place or 'Unknown'}"
            )

        with death_col:
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

        # General information
        sex_col, status_col, id_col = st.columns(3)

        with sex_col:
            st.markdown(
                f"**Sex**  \n"
                f"{sex}"
            )

        with status_col:
            st.markdown(
                f"**Status**  \n"
                f"{status}"
            )

        with id_col:
            st.markdown(
                f"**GEDCOM ID**  \n"
                f"`{person.gedcom_id}`"
            )

        st.divider()

        # Parents
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

        # Tylko główny profil może otworzyć podokno rodzica.
        # W już otwartym podoknie kliknięcie rodzica podmienia osobę.
        if not is_related_view:
            show_related_person(
                source_person=person,
                people=people,
                key_prefix=f"{key_prefix}_parents",
                navigation_source_id=navigation_source_id,
                section="parents",
            )

        st.divider()

        # Partners and children
        st.markdown("#### 💍 Marital status")

        if partners:
            for index, partner in enumerate(partners):
                partner_name = get_display_name(partner)

                children = get_children_with_partner(
                    person,
                    partner,
                    people_by_id,
                )

                partner_section = (
                    f"partner_{partner.gedcom_id}"
                )

                children_section = (
                    f"children_{partner.gedcom_id}"
                )

                children_key = (
                    f"{key_prefix}_children_"
                    f"{person.gedcom_id}_"
                    f"{partner.gedcom_id}"
                )

                partner_col, children_col = st.columns([3, 1])

                with partner_col:
                    st.markdown("**Married to**")

                    show_related_person_button(
                        target_person=partner,
                        label=f"{partner_name} →",
                        key=(
                            f"{key_prefix}_partner_"
                            f"{person.gedcom_id}_"
                            f"{partner.gedcom_id}"
                        ),
                        navigation_source_id=navigation_source_id,
                        section=partner_section,
                        is_related_view=is_related_view,
                    )

                with children_col:
                    st.markdown("**Children**")

                    child_count = len(children)

                    if child_count == 1:
                        children_label = "1 child"
                    else:
                        children_label = (
                            f"{child_count} children"
                        )

                    st.button(
                        children_label,
                        key=children_key,
                        disabled=child_count == 0,
                        on_click=toggle_children,
                        args=(children_key,),
                        use_container_width=True,
                    )

                # Profil partnera może zostać otwarty jako podokno
                # wyłącznie z głównego profilu.
                if not is_related_view:
                    show_related_person(
                        source_person=person,
                        people=people,
                        key_prefix=(
                            f"{key_prefix}_{partner_section}"
                        ),
                        navigation_source_id=navigation_source_id,
                        section=partner_section,
                    )

                children_are_expanded = (
                    children_key
                    in st.session_state.expanded_children_keys
                )

                if children_are_expanded and children:
                    with st.container(border=True):
                        header_col, close_col = st.columns([5, 1])

                        with header_col:
                            st.markdown(
                                f"**Children with "
                                f"{partner_name}**"
                            )

                        with close_col:
                            st.button(
                                "✕ Close",
                                key=f"{children_key}_close",
                                on_click=toggle_children,
                                args=(children_key,),
                            )

                        for child in children:
                            child_name = get_display_name(child)

                            birth_year = (
                                child.birth_year
                                if child.birth_year
                                else "?"
                            )

                            death_year = (
                                child.death_year
                                if child.death_year
                                else "?"
                            )

                            show_related_person_button(
                                target_person=child,
                                label=(
                                    f"{child_name} "
                                    f"({birth_year} – "
                                    f"{death_year}) →"
                                ),
                                key=(
                                    f"{key_prefix}_child_"
                                    f"{person.gedcom_id}_"
                                    f"{partner.gedcom_id}_"
                                    f"{child.gedcom_id}"
                                ),
                                navigation_source_id=(
                                    navigation_source_id
                                ),
                                section=children_section,
                                is_related_view=is_related_view,
                            )

                        # Profil dziecka otwiera się pod listą dzieci
                        # tylko wtedy, gdy lista należy do głównego profilu.
                        #
                        # Jeśli lista znajduje się już w podoknie,
                        # kliknięcie dziecka podmieni osobę dzięki
                        # replace_related_person().
                        if not is_related_view:
                            show_related_person(
                                source_person=person,
                                people=people,
                                key_prefix=(
                                    f"{key_prefix}_"
                                    f"{children_section}"
                                ),
                                navigation_source_id=(
                                    navigation_source_id
                                ),
                                section=children_section,
                            )

                if index < len(partners) - 1:
                    st.divider()

        else:
            st.markdown("**No partner recorded**")
