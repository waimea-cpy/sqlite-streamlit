"""Page 2: one project and its tasks. The URL says which project, e.g. /project?id=3"""

import streamlit as st

from utils import execute, fetch_one, fetch_all

STATUSES = ["Active", "On hold", "Done"]

if st.button("< Back to projects"):
    st.switch_page("views/projects.py")

project_id = st.query_params.get("id")
project = fetch_one("SELECT * FROM projects WHERE id = ?", project_id)

if project is None:
    st.error("Project not found.")
    st.stop()   # don't run the rest of this page

st.title(project["name"])

# The key includes the project ID, so each project gets its own status box
new_status = st.selectbox("Status", STATUSES, index=STATUSES.index(project["status"]), key=f"status_{project_id}")
if new_status != project["status"]:
    execute("UPDATE projects SET status = ? WHERE id = ?", new_status, project_id)
    st.rerun()


# --- Tasks ---

tasks = fetch_all("SELECT * FROM tasks WHERE project_id = ? ORDER BY is_done, id", project_id)

st.subheader("Tasks")
done_count = sum(task["is_done"] for task in tasks)
st.caption(f"{done_count} of {len(tasks)} tasks done")

if not tasks:
    st.info("No tasks yet. Add one below!")

for task in tasks:
    # Every widget made in a loop needs its own unique key
    tick_column, delete_column = st.columns([6, 1])

    is_done = tick_column.checkbox(task["title"], value=bool(task["is_done"]), key=f"done_{task['id']}")
    if is_done != bool(task["is_done"]):
        execute("UPDATE tasks SET is_done = ? WHERE id = ?", int(is_done), task["id"])
        st.rerun()

    # A popover is a button that opens a little box - here it holds the "are you sure?" button
    with delete_column.popover("Delete", key=f"delete_{task['id']}"):
        st.write("This deletes this task permanently.")
        if st.button("Yes, delete", key=f"confirm_delete_{task['id']}"):
            execute("DELETE FROM tasks WHERE id = ?", task["id"])
            st.rerun()

with st.form("add_task", clear_on_submit=True):
    title = st.text_input("New task")
    if st.form_submit_button("Add task") and title.strip():
        execute("INSERT INTO tasks (project_id, title) VALUES (?, ?)", project_id, title.strip())
        st.rerun()


st.divider()

with st.popover("Delete this project", type="primary"):
    st.write("This deletes the project and all its tasks.")
    if st.button("Yes, delete", type="primary"):
        # The tasks go too, because the schema says ON DELETE CASCADE
        execute("DELETE FROM projects WHERE id = ?", project_id)
        st.switch_page("views/projects.py")
