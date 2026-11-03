"""Projects and tasks: a Streamlit app on SQLite, with two related tables.

Install first:  pip install streamlit
Run with:       streamlit run streamlit_app.py   (it opens in your browser)

How Streamlit works: every time you click or type anything, the WHOLE page
script runs again from top to bottom. So there are no callbacks - just "if the
button was clicked, do the SQL", then the page redraws with fresh data.

This file just lists the pages. Each page is its own script in views/.
"""

import streamlit as st

from utils import DATABASE_PATH, seed_database

if not DATABASE_PATH.exists():
    seed_database()

pages = st.navigation(
    [
        st.Page("views/projects.py", title="Projects", default=True),
        # Hidden from the menu: you get here by clicking a project, e.g. /project?id=3
        st.Page("views/project.py", title="Project", url_path="project", visibility="hidden"),
    ],
    position="hidden",
)
pages.run()
