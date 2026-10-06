import pyodbc
from pymongo import MongoClient

# -----------------------------
# HELPER FUNCTION
# -----------------------------

def print_section(title):
    print("\n" + "=" * 40)
    print(title)
    print("=" * 40)


# -----------------------------
# SQL SERVER CONNECTION
# -----------------------------

print_section("SQL SERVER CONNECTION")

sql_conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=DESKTOP-PHJ079G\\MSSQLSERVER01;"
    "DATABASE=MovieNest;"
    "Trusted_Connection=yes;"
)

cursor = sql_conn.cursor()


# -----------------------------
# MONGODB CONNECTION
# -----------------------------

print_section("MONGODB CONNECTION")

client = MongoClient("mongodb://localhost:27017")

db = client["MovieNestMongo"]

users_collection = db["users"]
movies_collection = db["movies"]

# Make migration idempotent
users_collection.delete_many({})
movies_collection.delete_many({})


# -----------------------------
# MIGRATE USERS
# -----------------------------

print_section("MIGRATING USERS")

users_query = """
SELECT
    u.UserID,
    u.FullName,
    u.Email,
    u.DateOfRegistration,
    u.UserType,
    COUNT(DISTINCT r.RentalID) AS TotalRentals,
    COUNT(DISTINCT rv.ReviewID) AS TotalReviews
FROM USERS u
LEFT JOIN RENTALS r
    ON u.UserID = r.UserID
LEFT JOIN REVIEWS rv
    ON u.UserID = rv.UserID
GROUP BY
    u.UserID,
    u.FullName,
    u.Email,
    u.DateOfRegistration,
    u.UserType
ORDER BY u.UserID;
"""

cursor.execute(users_query)

users = []

for row in cursor.fetchall():
    users.append({
        "userId": row.UserID,
        "fullName": row.FullName,
        "email": row.Email,
        "dateOfRegistration": str(row.DateOfRegistration),
        "userType": row.UserType,
        "totalRentals": row.TotalRentals,
        "totalReviews": row.TotalReviews
    })

users_collection.insert_many(users)

print("Users migrated successfully!")
print(f"Total users migrated: {len(users)}")


# -----------------------------
# MIGRATE MOVIES
# -----------------------------

print_section("MIGRATING MOVIES")

movies_query = """
SELECT
    m.MovieID,
    m.Title,
    m.ReleaseYear,
    m.Duration,
    m.Genre,
    m.Description,
    COUNT(DISTINCT r.RentalID) AS RentalCount,
    COUNT(DISTINCT rv.ReviewID) AS ReviewCount,
    ROUND(AVG(CAST(rv.Rating AS FLOAT)), 2) AS AverageRating
FROM MOVIES m
LEFT JOIN RENTALS r
    ON m.MovieID = r.MovieID
LEFT JOIN REVIEWS rv
    ON m.MovieID = rv.MovieID
GROUP BY
    m.MovieID,
    m.Title,
    m.ReleaseYear,
    m.Duration,
    m.Genre,
    m.Description
ORDER BY m.MovieID;
"""

cursor.execute(movies_query)

movies = []

for row in cursor.fetchall():

    # Get actors for this movie
    actors_query = """
    SELECT
        a.ActorID,
        a.FullName,
        am.ActorRole
    FROM ACTORS_MOVIES am
    JOIN ACTORS a
        ON am.ActorID = a.ActorID
    WHERE am.MovieID = ?
    ORDER BY a.ActorID;
    """

    cursor.execute(actors_query, row.MovieID)

    actors = []

    for actor_row in cursor.fetchall():
        actors.append({
            "actorId": actor_row.ActorID,
            "fullName": actor_row.FullName,
            "role": actor_row.ActorRole
        })

    average_rating = row.AverageRating

    if average_rating is None:
        average_rating = 0

    movies.append({
        "movieId": row.MovieID,
        "title": row.Title,
        "releaseYear": row.ReleaseYear,
        "duration": row.Duration,
        "genre": row.Genre,
        "description": row.Description,
        "actors": actors,
        "rentalCount": row.RentalCount,
        "reviewCount": row.ReviewCount,
        "averageRating": float(average_rating)
    })

movies_collection.insert_many(movies)

print("Movies migrated successfully!")
print(f"Total movies migrated: {len(movies)}")


# -----------------------------
# CLOSE CONNECTIONS
# -----------------------------

print_section("CLOSING CONNECTIONS")

sql_conn.close()
client.close()

print("Migration completed successfully!")