import streamlit as st

from src.gedcom_parser import parse_gedcom
from src.search import search_people
from components.person_details import show_person_details


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

def close_related_person():
    st.session_state.selected_person_id = None


st.set_page_config(
    page_title="Genealogy Data Explorer",
    page_icon="🌳",
    layout="wide",
)

st.title("Genealogy Data Explorer")
st.write(
    "Upload a GEDCOM file to explore and search genealogy data."
)


uploaded_file = st.file_uploader(
    "Upload GEDCOM file",
    type=["ged"],
)


encoding_options = {
    "Auto detect": None,
    "UTF-8": "utf-8",
    "Windows-1250 (Central European)": "cp1250",
    "Windows-1252 (Western European)": "cp1252",
    "ISO-8859-2 (Central European)": "iso-8859-2",
    "UTF-16": "utf-16",
}


selected_encoding = st.selectbox(
    "File encoding",
    options=encoding_options.keys(),
)

if "selected_person_id" not in st.session_state:
    st.session_state.selected_person_id = None

if "related_source_id" not in st.session_state:
    st.session_state.related_source_id = None

if "related_section" not in st.session_state:
    st.session_state.related_section = None

if "expanded_children_keys" not in st.session_state:
    st.session_state.expanded_children_keys = set()

if uploaded_file is not None:
    try:
        people = parse_gedcom(
            uploaded_file,
            encoding=encoding_options[selected_encoding],
        )

        st.success(f"Loaded {len(people)} people.")

        st.divider()

        st.subheader("Search people")

        col1, col2 = st.columns(2)

        with col1:
            first_name = st.text_input(
                "First name",
                placeholder="e.g. Katarzyna",
            )

            birth_year_input = st.text_input(
                "Birth year",
                placeholder="e.g. 1895",
            )

        with col2:
            last_name = st.text_input(
                "Surname",
                placeholder="e.g. Zając or Dzwonnik",
            )

            birth_place = st.text_input(
                "Birth place",
                placeholder="e.g. Tarnowskie Góry",
            )

        birth_year = None
        birth_year_valid = True

        if birth_year_input.strip():
            try:
                birth_year = int(birth_year_input)

            except ValueError:
                birth_year_valid = False
                st.warning("Birth year must be a number.")

        if birth_year_valid:
            results = search_people(
                people,
                first_name=first_name,
                last_name=last_name,
                birth_year=birth_year,
                birth_place=birth_place,
            )

            st.divider()

            st.subheader("Results")
            st.write(f"Found {len(results)} people.")

            if not results:
                st.info("No matching people found.")

            else:
                for person in results[:50]:
                    full_name = get_display_name(person)

                    birth_year_display = (
                        person.birth_year
                        if person.birth_year
                        else "?"
                    )

                    death_year_display = (
                        person.death_year
                        if person.death_year
                        else "?"
                    )

                    label = (
                        f"{full_name} "
                        f"({birth_year_display} – {death_year_display})"
                    )

                    # Check whether this person's profile
                    # should contain the related-person card
                    is_navigation_source = (
                        st.session_state.related_source_id
                        == person.gedcom_id
                    )

                    with st.expander(
                        label,
                        expanded=is_navigation_source,
                    ):
                        show_person_details(
                            person,
                            people,
                            key_prefix=f"result_{person.gedcom_id}",
                            navigation_source_id=person.gedcom_id,
                        )


                if len(results) > 50:
                    st.info(
                        f"Showing the first 50 of "
                        f"{len(results)} results."
                    )

    except UnicodeDecodeError:
        st.error(
            "Unable to decode this GEDCOM file. "
            "Try selecting a different file encoding."
        )

    except ValueError as error:
        st.error(str(error))

    except Exception as error:
        st.error(
            "An unexpected error occurred while reading "
            "the GEDCOM file."
        )
        st.exception(error)