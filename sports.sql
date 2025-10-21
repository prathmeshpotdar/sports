CREATE DATABASE sports;
USE sports;

SELECT COUNT(*) FROM competitions;
SELECT * FROM competitor_rankings ORDER BY rank_position LIMIT 10;

SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS Competitor_Rankings;
DROP TABLE IF EXISTS Competitors;
DROP TABLE IF EXISTS Venues;
DROP TABLE IF EXISTS Complexes;
DROP TABLE IF EXISTS Competitions;
DROP TABLE IF EXISTS Categories;

SET FOREIGN_KEY_CHECKS = 1;


DROP TABLE IF EXISTS Categories;

CREATE TABLE Categories (
    category_id VARCHAR(50) PRIMARY KEY,
    category_name VARCHAR(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE Competitions (
    competition_id VARCHAR(50) PRIMARY KEY,
    competition_name VARCHAR(255) NOT NULL,
    category_id VARCHAR(50),
    type VARCHAR(50),
    gender VARCHAR(20),
    FOREIGN KEY (category_id) REFERENCES Categories(category_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE Complexes (
    complex_id VARCHAR(50) PRIMARY KEY,
    complex_name VARCHAR(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE Venues (
    venue_id VARCHAR(50) PRIMARY KEY,
    venue_name VARCHAR(255) NOT NULL,
    city_name VARCHAR(100),
    country_name VARCHAR(100),
    timezone VARCHAR(50),
    complex_id VARCHAR(50),
    FOREIGN KEY (complex_id) REFERENCES Complexes(complex_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE Competitors (
    competitor_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    country VARCHAR(100),
    country_code VARCHAR(10)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE Competitor_Rankings (
    rank_id INT AUTO_INCREMENT PRIMARY KEY,
    competitor_id VARCHAR(50),
    rank_position INT,
    movement VARCHAR(50),
    points INT,
    FOREIGN KEY (competitor_id) REFERENCES Competitors(competitor_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DESCRIBE Competitions;

DESCRIBE Categories;

-- a) List all competitions with their category names
SELECT c.competition_id,
       c.name AS competition_name,
       cat.name AS category_name,
       c.type,
       c.gender
FROM Competitions c
JOIN Categories cat ON c.category_id = cat.category_id
LIMIT 0, 1000;
-- Shows all competitions and their categories

-- b) Count the number of competitions in each category
SELECT cat.name AS category_name, COUNT(c.competition_id) AS competition_count
FROM Categories cat
LEFT JOIN Competitions c ON cat.category_id = c.category_id
GROUP BY cat.name;
-- Counts competitions per category

-- c) Find competitions of type 'doubles'
SELECT competition_id, name AS competition_name, type, gender
FROM Competitions
WHERE type = 'doubles';
-- Filters competitions of type 'doubles'

-- d) Get competitions in a specific category (e.g., 'ITF Men')
SELECT c.competition_id, c.name AS competition_name
FROM Competitions c
JOIN Categories cat ON c.category_id = cat.category_id
WHERE cat.name = 'ITF Men';
-- Filters competitions by category

-- e) Analyze distribution of competition types by category
SELECT cat.name AS category_name, c.type, COUNT(c.competition_id) AS type_count
FROM Competitions c
JOIN Categories cat ON c.category_id = cat.category_id
GROUP BY cat.name, c.type
ORDER BY cat.name;
-- Counts how many competitions of each type exist per category

-- f) List all top-level competitions (all competitions in current schema)
SELECT competition_id, name AS competition_name
FROM Competitions;
-- Since there is no hierarchy, all competitions are considered top-level


DESCRIBE Venues;


-- a) List all venues with their complex names
SELECT v.venue_id, 
       v.name AS venue_name, 
       v.capacity, 
       v.surface, 
       c.name AS complex_name
FROM Venues v
JOIN Complexes c ON v.complex_id = c.complex_id
LIMIT 0, 1000;
-- Shows venues with capacity, surface, and the complex they belong to

-- b) Count the number of venues in each complex
SELECT c.name AS complex_name, COUNT(v.venue_id) AS venue_count
FROM Complexes c
LEFT JOIN Venues v ON c.complex_id = v.complex_id
GROUP BY c.name;
-- Counts venues per complex

-- c) Get venues with a specific surface (e.g., 'Hard')
SELECT venue_id, name AS venue_name, capacity, surface
FROM Venues
WHERE surface = 'Hard';
-- Filters venues by surface type

-- d) Identify all venues and their capacities
SELECT name AS venue_name, capacity, surface, complex_id
FROM Venues;
-- Lists all venues with capacity and surface

-- e) Find complexes with more than one venue
SELECT c.name AS complex_name, COUNT(v.venue_id) AS num_venues
FROM Complexes c
JOIN Venues v ON c.complex_id = v.complex_id
GROUP BY c.name
HAVING num_venues > 1;
-- Identifies complexes with multiple venues

-- f) List venues grouped by surface type
SELECT surface, GROUP_CONCAT(name ORDER BY name SEPARATOR ', ') AS venues
FROM Venues
GROUP BY surface;
-- Shows venues grouped by surface type

-- g) Find all venues for a specific complex
SELECT name AS venue_name, capacity, surface
FROM Venues
WHERE complex_id = 'complex1';
-- Filters venues belonging to a specific complex




-- Get all competitors with their rank and points
SELECT comp.name AS competitor_name, cr.rank_position, cr.points
FROM Competitor_Rankings cr
JOIN Competitors comp ON cr.competitor_id = comp.competitor_id
ORDER BY cr.rank_position;

-- Find competitors ranked in the top 5
SELECT comp.name AS competitor_name, cr.rank_position, cr.points
FROM Competitor_Rankings cr
JOIN Competitors comp ON cr.competitor_id = comp.competitor_id
WHERE cr.rank_position <= 5
ORDER BY cr.rank_position;

-- Count competitors
SELECT COUNT(competitor_id) AS num_competitors
FROM Competitors;

-- Find competitors with the highest points
SELECT comp.name AS competitor_name, cr.points
FROM Competitor_Rankings cr
JOIN Competitors comp ON cr.competitor_id = comp.competitor_id
WHERE cr.points = (SELECT MAX(points) FROM Competitor_Rankings);
