-- MovieNest NoSQL Migration Project
USE master;
GO

DROP DATABASE IF EXISTS MovieNest;
GO

CREATE DATABASE MovieNest;
GO

USE MovieNest;
GO

-- 1. USERS table
CREATE TABLE USERS
(
    UserID INT PRIMARY KEY,
    FullName VARCHAR(100) NOT NULL,
    Email VARCHAR(100) NOT NULL UNIQUE,
    DateOfRegistration DATE NOT NULL,
    UserType VARCHAR(20) NOT NULL,

    CONSTRAINT chk_user_type
        CHECK (UserType IN ('Regular', 'Premium', 'Admin'))
);
GO

-- 2. ACTORS table
CREATE TABLE ACTORS
(
    ActorID INT PRIMARY KEY,
    FullName VARCHAR(100) NOT NULL,
    DateOfBirth DATE NULL
);
GO

-- 3. MOVIES table
CREATE TABLE MOVIES
(
    MovieID INT PRIMARY KEY,
    Title VARCHAR(200) NOT NULL,
    ReleaseYear INT NOT NULL,
    Duration INT NOT NULL, -- duration in minutes
    Genre VARCHAR(50) NOT NULL,
    Description VARCHAR(MAX) NULL,

    CONSTRAINT chk_release_year
        CHECK (ReleaseYear BETWEEN 1900 AND 2026),

    CONSTRAINT chk_duration
        CHECK (Duration > 0)
);
GO

-- 4. ACTORS_MOVIES table
-- This is the junction table between ACTORS and MOVIES
CREATE TABLE ACTORS_MOVIES
(
    ActorID INT NOT NULL,
    MovieID INT NOT NULL,
    ActorRole VARCHAR(100) NULL,

    CONSTRAINT pk_actors_movies
        PRIMARY KEY (ActorID, MovieID),

    CONSTRAINT fk_actors_movies_actor
        FOREIGN KEY (ActorID) REFERENCES ACTORS(ActorID),

    CONSTRAINT fk_actors_movies_movie
        FOREIGN KEY (MovieID) REFERENCES MOVIES(MovieID)
);
GO

-- 5. RENTALS table
CREATE TABLE RENTALS
(
    RentalID INT PRIMARY KEY,
    UserID INT NOT NULL,
    MovieID INT NOT NULL,
    RentalDate DATE NOT NULL,
    ReturnDate DATE NULL,
    RentalStatus VARCHAR(20) NOT NULL,

    CONSTRAINT fk_rentals_user
        FOREIGN KEY (UserID) REFERENCES USERS(UserID),

    CONSTRAINT fk_rentals_movie
        FOREIGN KEY (MovieID) REFERENCES MOVIES(MovieID),

    CONSTRAINT chk_rental_status
        CHECK (RentalStatus IN ('Active', 'Returned', 'Late')),

    CONSTRAINT chk_return_date
        CHECK (ReturnDate IS NULL OR ReturnDate >= RentalDate)
);
GO

-- 6. REVIEWS table
CREATE TABLE REVIEWS
(
    ReviewID INT PRIMARY KEY,
    UserID INT NOT NULL,
    MovieID INT NOT NULL,
    Rating INT NOT NULL,
    Comment VARCHAR(MAX) NULL,
    ReviewDate DATE NOT NULL,

    CONSTRAINT fk_reviews_user
        FOREIGN KEY (UserID) REFERENCES USERS(UserID),

    CONSTRAINT fk_reviews_movie
        FOREIGN KEY (MovieID) REFERENCES MOVIES(MovieID),

    CONSTRAINT chk_rating
        CHECK (Rating BETWEEN 1 AND 5),

    CONSTRAINT unique_user_movie_review
        UNIQUE (UserID, MovieID)
);
GO