create schema icebreakers;

CREATE TABLE icebreakers.User (
    id INT PRIMARY KEY,
    email VARCHAR(30) unique,
    name VARCHAR(50) not null,
    dob DATE not null,
    created_date TIMESTAMP,
    password VARCHAR(200) not null,
    points INT
);

