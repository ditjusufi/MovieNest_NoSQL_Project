-- insterting the synthetic data  
BULK INSERT USERS
FROM 'C:\Users\Dita\OneDrive\Desktop\MovieNest_NoSQL_Project\data\users.csv'
WITH
(
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    TABLOCK
);

SELECT COUNT(*) AS TotalUsers
FROM USERS;

SELECT TOP 10 *
FROM USERS;

BULK INSERT ACTORS
FROM 'C:\Users\Dita\OneDrive\Desktop\MovieNest_NoSQL_Project\data\actors.csv'
WITH
(
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    TABLOCK
);

SELECT COUNT(*) AS TotalActors
FROM ACTORS;

BULK INSERT MOVIES
FROM 'C:\Users\Dita\OneDrive\Desktop\MovieNest_NoSQL_Project\data\movies.csv'
WITH
(
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    TABLOCK
);

SELECT COUNT(*) AS TotalMovies
FROM MOVIES;

BULK INSERT ACTORS_MOVIES
FROM 'C:\Users\Dita\OneDrive\Desktop\MovieNest_NoSQL_Project\data\actors_movies.csv'
WITH
(
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    TABLOCK
);

SELECT COUNT(*) AS TotalActorMovieLinks
FROM ACTORS_MOVIES;

BULK INSERT RENTALS
FROM 'C:\Users\Dita\OneDrive\Desktop\MovieNest_NoSQL_Project\data\rentals.csv'
WITH
(
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    TABLOCK
);

SELECT COUNT(*) AS TotalRentals
FROM RENTALS;

BULK INSERT REVIEWS
FROM 'C:\Users\Dita\OneDrive\Desktop\MovieNest_NoSQL_Project\data\reviews.csv'
WITH
(
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    TABLOCK
);

SELECT COUNT(*) AS TotalReviews
FROM REVIEWS;

-- checking if everything is insterted 
SELECT
    (SELECT COUNT(*) FROM USERS) AS UsersCount,
    (SELECT COUNT(*) FROM ACTORS) AS ActorsCount,
    (SELECT COUNT(*) FROM MOVIES) AS MoviesCount,
    (SELECT COUNT(*) FROM ACTORS_MOVIES) AS ActorMovieCount,
    (SELECT COUNT(*) FROM RENTALS) AS RentalsCount,
    (SELECT COUNT(*) FROM REVIEWS) AS ReviewsCount;


-- queries to validate the database
SELECT RentalStatus,
       COUNT(*) AS TotalRentals
FROM RENTALS
GROUP BY RentalStatus;

SELECT TOP 10
       m.Title,
       COUNT(*) AS RentalCount
FROM RENTALS r
JOIN MOVIES m
    ON r.MovieID = m.MovieID
GROUP BY m.Title
ORDER BY RentalCount DESC;

SELECT
    m.Genre,
    ROUND(AVG(CAST(rv.Rating AS FLOAT)),2) AS AverageRating
FROM REVIEWS rv
JOIN MOVIES m
    ON rv.MovieID = m.MovieID
GROUP BY m.Genre
ORDER BY AverageRating DESC;

SELECT COUNT(*)
FROM REVIEWS;