"""Page 1: the list of projects. Select a row to open that project."""

import streamlit as st

from utils import seed_database, execute, fetch_all

STATUSES = ["Active", "On hold", "Done"]

st.title("Projects")
st.caption("Select a project to see its tasks.")

projects = fetch_all("""
    SELECT projects.id,
           projects.name                    AS Project,
           projects.status                  AS Status,
           COUNT(tasks.id)                  AS Tasks,
           COALESCE(SUM(tasks.is_done), 0)  AS Done
    FROM projects
    LEFT JOIN tasks ON tasks.project_id = projects.id
    GROUP BY projects.id
    ORDER BY projects.name
""")

# on_select="rerun" means selecting a row runs this script again, and tells us which row
event = st.dataframe(
    [dict(project) for project in projects],
    hide_index=True,
    column_order=["Project", "Status", "Tasks", "Done"],
    on_select="rerun",
    selection_mode="single-row",
)

if event.selection.rows:
    # We're told the row's POSITION in the list, so look up that project to get its ID
    chosen = projects[event.selection.rows[0]]
    st.switch_page("views/project.py", query_params={"id": chosen["id"]})


# A form only sends its values when the submit button is clicked
with st.form("add_project", clear_on_submit=True):
    st.subheader("Add a project")
    name = st.text_input("Project name")
    status = st.selectbox("Status", STATUSES)

    if st.form_submit_button("Add project"):
        if name.strip():
            execute("INSERT INTO projects (name, status) VALUES (?, ?)", name.strip(), status)
            st.rerun()   # run the script again so the table shows the new project
        else:
            st.error("Please type a project name.")


with st.popover("Reset demo data"):
    st.write("This deletes everything and puts the demo data back.")
    if st.button("Yes, reset", type="primary"):
        seed_database()
        st.rerun()
