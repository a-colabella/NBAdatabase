USE nba;

DELIMITER //
CREATE PROCEDURE all_player()
SELECT player_name, pos, age, Tm, G as Games, TRUNCATE(FG/FGA, 2) as 'FG%', TRUNCATE(3P/3PA, 2) as '3P%', TRUNCATE(FT/FTA, 2) as 'FT%', TRUNCATE((ORB+DRB)/G, 2) as Rebounds,
TRUNCATE(AST/G, 2) as Assists, TRUNCATE(STL/G, 2) as Steals, TRUNCATE(BLK/G, 2) as Blocks, TRUNCATE(TOV/G, 2) as Turnovers, TRUNCATE(PTS/G, 2) as 'PPG' 
FROM players
//

DELIMITER //
CREATE PROCEDURE all_coach()
SELECT coach_name, team_name
FROM coaches
//

DELIMITER //
SELECT *
FROM games;
//

DELIMITER //
SELECT *
FROM teams;
//

DELIMITER //
SELECT *
FROM players
//
