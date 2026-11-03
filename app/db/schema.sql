------------------------------------------------------------------
-- Setup the projects table
------------------------------------------------------------------

DROP TABLE IF EXISTS projects;

CREATE TABLE projects (
    id     INTEGER PRIMARY KEY AUTOINCREMENT,
    name   TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'Active' CHECK (status IN ('Active', 'On hold', 'Done'))
);

------------------------------------------------------------------
-- Setup the tasks table
------------------------------------------------------------------

DROP TABLE IF EXISTS tasks;

CREATE TABLE tasks (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    title      TEXT    NOT NULL,
    is_done    INTEGER NOT NULL DEFAULT 0,  -- 0 = to do, 1 = done

    FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE
);

