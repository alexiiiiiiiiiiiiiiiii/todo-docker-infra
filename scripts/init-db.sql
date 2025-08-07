CREATE TABLE IF NOT EXISTS tasks (
  id SERIAL PRIMARY KEY,
  title TEXT NOT NULL
);

INSERT INTO tasks (title) VALUES
('Apprendre Docker'),
('Créer une API Flask'),
('Booster ma note !');
