--  --- --- -- >> CODE HONOR << --
-- the folowing code was inspired by this project https://github.com/danielburkard/udacity_fullstack_project2

-- Drop the Database if exists
DROP DATABASE IF EXISTS tournament;

-- Create the tournaiment Database
CREATE DATABASE tournament;

\c tournament

-- Players Table
CREATE TABLE Players (
  id   SERIAL PRIMARY KEY,
  name VARCHAR(255)
);

-- Matches Table
CREATE TABLE Matches (
  id       SERIAL PRIMARY KEY,
  winner   INT REFERENCES Players (id),
  loser INT REFERENCES Players (id)
);

-- Wins View shows number of wins for each Player
CREATE VIEW Wins AS
  SELECT
    Players.id,
    COUNT(Matches.winner) AS n
  FROM Players
    LEFT JOIN Matches
      ON Players.id = Matches.winner
  GROUP BY Players.id, Matches.winner;

-- Count View shows number of matches for each Player
CREATE VIEW Count AS
  SELECT
    Players.id,
    Count(Matches.loser) AS n
  FROM Players
    LEFT JOIN Matches
      ON Players.id = Matches.winner
  GROUP BY Players.id;

-- Standings View shows number of wins and matches for each Player
CREATE VIEW Standings AS
 ( SELECT
    Players.id,
    Players.name,
    count(Matches.winner) as wins,
    (select count(Matches.id) from Matches where Players.id = Matches.winner OR Players.id = Matches.loser) AS matches
    FROM Players
    LEFT JOIN Matches
    on Players.id = Matches.winner
    GROUP BY Players.id
    ORDER BY wins);
