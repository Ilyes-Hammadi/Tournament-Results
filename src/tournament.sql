--  --- --- -- >> CODE HONOR << --
-- the folowing code was inspired by this project https://github.com/danielburkard/udacity_fullstack_project2


-- Drop all the tables and views if they exists
DROP VIEW IF EXISTS Standings;
DROP VIEW IF EXISTS Count;
DROP VIEW IF EXISTS Wins;
DROP TABLE IF EXISTS Matches;
DROP TABLE IF EXISTS Players;

-- Players Table
CREATE TABLE Players (
  id   SERIAL PRIMARY KEY,
  name VARCHAR(255)
);

-- Matches Table
CREATE TABLE Matches (
  id       SERIAL PRIMARY KEY,
  winner   INT REFERENCES Players (id),
  loser INT REFERENCES Players (id),
  result   INT
);

-- Wins View shows number of wins for each Player
CREATE VIEW Wins AS
  SELECT
    Players.id,
    COUNT(Matches.loser) AS n
  FROM Players
    LEFT JOIN (SELECT *
               FROM Matches
               WHERE result > 0) AS Matches
      ON Players.id = Matches.winner
  GROUP BY Players.id;

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
  SELECT
    Players.id,
    Players.name,
    Wins.n  AS wins,
    Count.n AS matches
  FROM Players, Count, Wins
  WHERE Players.id = Wins.id AND Wins.id = Count.id;
