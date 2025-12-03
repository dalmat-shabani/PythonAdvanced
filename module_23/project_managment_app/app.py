import streamlit as st
import requests
import pandas as pd

st.title("Project Management App")

# -------------------------
# Add Developer
# -------------------------
st.header("Add a Developer")
dev_name = st.text_input("Developer Name")
dev_experience = st.number_input(
    "Developer Experience (Years)", min_value=0, max_value=50, value=0
)

if st.button("Create Developer"):
    dev_data = {"name": dev_name, "experience": dev_experience}
    response = requests.post("https://127.0.0.1:8000/developers/", json=dev_data)
    st.json(response.json())

# -------------------------
# Create Project
# -------------------------
st.header("Create Project")
proj_title = st.text_input("Project Title")
proj_description = st.text_area("Project Description")
proj_lang = st.text_input("Project Languages Used (comma-separated)")
lead_dev_name = st.text_input("Lead Developer Name")
lead_dev_exp = st.number_input(
    "Lead Developer Experience (Years)", min_value=0, max_value=50, value=0
)

if st.button("Create Project"):
    lead_dev_data = {"name": lead_dev_name, "experience": lead_dev_exp}

    proj_data = {
        "title": proj_title,
        "description": proj_description,
        "languages": [lang.strip() for lang in proj_lang.split(",") if lang.strip()],
        "lead_developer": lead_dev_data,
    }

    response = requests.post("https://127.0.0.1:8000/projects/", json=proj_data)
    st.json(response.json())

# -------------------------
# Display Projects Dashboard
# -------------------------
st.header("Project Dashboard")

if st.button("Get Projects"):
    response = requests.get("https://127.0.0.1:8000/projects/")
    project_data = response.json().get("projects", [])

    if project_data:
        projects_df = pd.DataFrame(project_data)

        st.subheader("Project Overview")
        st.dataframe(projects_df)

        st.subheader("Project Details")
        for proj in project_data:
            st.markdown(f"### {proj['title']}")
            st.markdown(f"**Description:** {proj['description']}")
            st.markdown(f"**Languages Used:** {', '.join(proj['languages'])}")

            lead_dev = proj["lead_developer"]
            st.markdown(
                f"**Lead Developer:** {lead_dev['name']} — "
                f"{lead_dev['experience']} years of experience"
            )

            st.markdown("---")

    else:
        st.warning("No Project Found")
