import pyodbc
from pymongo import MongoClient

# SQL Server connection
sql_conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=DESKTOP-PHJ079G\\MSSQLSERVER01;"
    "DATABASE=MovieNest;"
    "Trusted_Connection=yes;"
)

cursor = sql_conn.cursor()

# MongoDB connection
client = MongoClient("mongodb://localhost:27017")
db = client["MovieNestMongo"]

users_collection = db["users"]
movies_collection = db["movies"]

print("MOVIENEST MIGRATION VALIDATION REPORT")
print("------------------------------------")

# 1. Validate users count
cursor.execute("SELECT COUNT(*) FROM USERS")
sql_users_count = cursor.fetchone()[0]

mongo_users_count = users_collection.count_documents({})

if sql_users_count == mongo_users_count:
    print(f"PASS - Users count matches: {sql_users_count}")
else:
    print(f"FAIL - Users count mismatch: SQL={sql_users_count}, MongoDB={mongo_users_count}")

# 2. Validate movies count
cursor.execute("SELECT COUNT(*) FROM MOVIES")
sql_movies_count = cursor.fetchone()[0]

mongo_movies_count = movies_collection.count_documents({})

if sql_movies_count == mongo_movies_count:
    print(f"PASS - Movies count matches: {sql_movies_count}")
else:
    print(f"FAIL - Movies count mismatch: SQL={sql_movies_count}, MongoDB={mongo_movies_count}")

# 3. Validate total rentals
cursor.execute("SELECT COUNT(*) FROM RENTALS")
sql_rentals_count = cursor.fetchone()[0]

mongo_rentals_count = sum(movie.get("rentalCount", 0) for movie in movies_collection.find({}))

if sql_rentals_count == mongo_rentals_count:
    print(f"PASS - Total rentals match: {sql_rentals_count}")
else:
    print(f"FAIL - Rental count mismatch: SQL={sql_rentals_count}, MongoDB={mongo_rentals_count}")

# 4. Validate total reviews
cursor.execute("SELECT COUNT(*) FROM REVIEWS")
sql_reviews_count = cursor.fetchone()[0]

mongo_reviews_count = sum(movie.get("reviewCount", 0) for movie in movies_collection.find({}))

if sql_reviews_count == mongo_reviews_count:
    print(f"PASS - Total reviews match: {sql_reviews_count}")
else:
    print(f"FAIL - Review count mismatch: SQL={sql_reviews_count}, MongoDB={mongo_reviews_count}")

# 5. Spot-check: top rented movie in SQL vs MongoDB
cursor.execute("""
SELECT TOP 1
    m.MovieID,
    m.Title,
    COUNT(*) AS RentalCount
FROM RENTALS r
JOIN MOVIES m ON r.MovieID = m.MovieID
GROUP BY m.MovieID, m.Title
ORDER BY RentalCount DESC;
""")

sql_top_movie = cursor.fetchone()

mongo_top_movie = movies_collection.find_one(
    sort=[("rentalCount", -1)]
)

if sql_top_movie.MovieID == mongo_top_movie["movieId"] and sql_top_movie.RentalCount == mongo_top_movie["rentalCount"]:
    print(f"PASS - Top rented movie matches: {sql_top_movie.Title}")
else:
    print("FAIL - Top rented movie mismatch")
    print(f"SQL: {sql_top_movie.Title}, {sql_top_movie.RentalCount}")
    print(f"MongoDB: {mongo_top_movie['title']}, {mongo_top_movie['rentalCount']}")

# 6. Spot-check: average rating by genre
cursor.execute("""
SELECT
    m.Genre,
    ROUND(AVG(CAST(rv.Rating AS FLOAT)), 2) AS AverageRating
FROM REVIEWS rv
JOIN MOVIES m ON rv.MovieID = m.MovieID
GROUP BY m.Genre
ORDER BY m.Genre;
""")

sql_genre_ratings = cursor.fetchall()

print("\nGenre rating spot-check:")
for row in sql_genre_ratings:
    mongo_movies = movies_collection.find(
        {
            "genre": row.Genre,
            "reviewCount": {"$gt": 0}
        }
    )

    total_weighted_rating = 0
    total_reviews = 0

    for movie in mongo_movies:
        total_weighted_rating += movie["averageRating"] * movie["reviewCount"]
        total_reviews += movie["reviewCount"]

    if total_reviews > 0:
        mongo_average = round(total_weighted_rating / total_reviews, 2)
    else:
        mongo_average = 0

    if float(row.AverageRating) == mongo_average:
        print(f"PASS - {row.Genre}: {mongo_average}")
    else:
        print(f"FAIL - {row.Genre}: SQL={row.AverageRating}, MongoDB={mongo_average}")

sql_conn.close()
client.close()

print("\nValidation completed.")