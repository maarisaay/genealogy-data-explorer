import streamlit as st


def show_person_details(person):
    sex_labels = {
        "F": "Female",
        "M": "Male",
    }

    sex = sex_labels.get(person.sex, "Unknown")

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

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(
                f"**Sex**  \n"
                f"{sex}"
            )

        with col2:
            st.markdown(
                f"**GEDCOM ID**  \n"
                f"`{person.gedcom_id}`"
            )