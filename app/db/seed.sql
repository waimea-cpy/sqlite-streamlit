------------------------------------------------------------------
-- Seed the projects table with some test projects
------------------------------------------------------------------

INSERT INTO projects (name, status) VALUES
    ('Dungeon Crawler',    'Active'),   -- project 1
    ('Pixel Art Editor',   'Active'),   -- project 2
    ('Boss Rush Mode',     'On hold'),  -- project 3
    ('Retro Arcade Menu',  'Done');     -- project 4

------------------------------------------------------------------
-- Seed the tasks table with some test tasks linking to projects
------------------------------------------------------------------

INSERT INTO tasks (project_id, title, is_done) VALUES
    (1, 'Design the map generator',            1),
    (1, 'Add treasure chests',                 1),
    (1, 'Make the boss slightly less invincible', 0),
    (1, 'Playtest with a very patient friend', 0),

    (2, 'Build the colour palette picker',     1),
    (2, 'Add an undo button',                  0),
    (2, 'Export to PNG',                       0),

    (3, 'Sketch ten bosses',                   1),
    (3, 'Balance the health bars',             0),

    (4, 'Build the title screen',              1),
    (4, 'Add the high score table',            1),
    (4, 'Add a secret cheat code',             1);

