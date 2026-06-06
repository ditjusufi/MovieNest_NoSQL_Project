from faker import Faker
import pandas as pd
import random
from datetime import date

fake = Faker()

# -----------------------------
# CONFIGURATION
# -----------------------------

NUM_USERS = 2000
NUM_ACTORS = 500
NUM_MOVIES = 1000
NUM_ACTOR_MOVIES = 3000
NUM_RENTALS = 20000
NUM_REVIEWS = 10000

genres = [
    "Action",
    "Adventure",
    "Comedy",
    "Drama",
    "Fantasy",
    "Horror",
    "Mystery",
    "Romance",
    "Sci-Fi",
    "Thriller"
]

actor_roles = [
    "Lead Actor",
    "Supporting Actor",
    "Cameo"
]

# -----------------------------
# USERS
# -----------------------------

users = []

for i in range(1, NUM_USERS + 1):

    r = random.random()

    if r < 0.85:
        user_type = "Regular"
    elif r < 0.99:
        user_type = "Premium"
    else:
        user_type = "Admin"

    users.append({
        "UserID": i,
        "FullName": fake.name(),
        "Email": fake.unique.email(),
        "DateOfRegistration": fake.date_between(
            start_date="-5y",
            end_date="today"
        ),
        "UserType": user_type
    })

df_users = pd.DataFrame(users)

# -----------------------------
# ACTORS
# -----------------------------

actors = []

for i in range(1, NUM_ACTORS + 1):

    actors.append({
        "ActorID": i,
        "FullName": fake.name(),
        "DateOfBirth": fake.date_of_birth(
            minimum_age=20,
            maximum_age=90
        )
    })

df_actors = pd.DataFrame(actors)

# -----------------------------
# MOVIES
# -----------------------------

movies = []

for i in range(1, NUM_MOVIES + 1):

    movies.append({
        "MovieID": i,
        "Title": fake.sentence(nb_words=3).replace(".", ""),
        "ReleaseYear": random.randint(1980, 2026),
        "Duration": random.randint(80, 180),
        "Genre": random.choice(genres),
        "Description": fake.text(max_nb_chars=200)
    })

df_movies = pd.DataFrame(movies)

# -----------------------------
# ACTORS_MOVIES
# -----------------------------

actor_movie_pairs = set()
actors_movies = []

while len(actors_movies) < NUM_ACTOR_MOVIES:

    actor_id = random.randint(1, NUM_ACTORS)
    movie_id = random.randint(1, NUM_MOVIES)

    pair = (actor_id, movie_id)

    if pair not in actor_movie_pairs:

        actor_movie_pairs.add(pair)

        actors_movies.append({
            "ActorID": actor_id,
            "MovieID": movie_id,
            "ActorRole": random.choice(actor_roles)
        })

df_actors_movies = pd.DataFrame(actors_movies)

# -----------------------------
# RENTALS
# -----------------------------

rentals = []

for i in range(1, NUM_RENTALS + 1):

    user_id = random.randint(1, NUM_USERS)
    movie_id = random.randint(1, NUM_MOVIES)

    rental_date = fake.date_between(
        start_date="-3y",
        end_date="today"
    )

    status_rand = random.random()

    if status_rand < 0.90:

        status = "Returned"

        return_date = fake.date_between(
            start_date=rental_date,
            end_date="today"
        )

    elif status_rand < 0.97:

        status = "Active"
        return_date = None

    else:

        status = "Late"
        return_date = None

    rentals.append({
        "RentalID": i,
        "UserID": user_id,
        "MovieID": movie_id,
        "RentalDate": rental_date,
        "ReturnDate": return_date,
        "RentalStatus": status
    })

df_rentals = pd.DataFrame(rentals)

# -----------------------------
# REVIEWS
# -----------------------------

reviews = []

review_pairs = set()

while len(reviews) < NUM_REVIEWS:

    rental = random.choice(rentals)

    pair = (
        rental["UserID"],
        rental["MovieID"]
    )

    if pair not in review_pairs:

        review_pairs.add(pair)

        reviews.append({
            "ReviewID": len(reviews) + 1,
            "UserID": rental["UserID"],
            "MovieID": rental["MovieID"],
            "Rating": random.randint(1, 5),
            "Comment": fake.sentence(nb_words=10),
            "ReviewDate": fake.date_between(
                start_date=rental["RentalDate"],
                end_date="today"
            )
        })

df_reviews = pd.DataFrame(reviews)

# -----------------------------
# EXPORT CSV FILES
# -----------------------------

df_users.to_csv("../data/users.csv", index=False)
df_actors.to_csv("../data/actors.csv", index=False)
df_movies.to_csv("../data/movies.csv", index=False)
df_actors_movies.to_csv("../data/actors_movies.csv", index=False)
df_rentals.to_csv("../data/rentals.csv", index=False)
df_reviews.to_csv("../data/reviews.csv", index=False)

# -----------------------------
# SUMMARY
# -----------------------------

print("Generation completed successfully!\n")

print(f"Users: {len(df_users)}")
print(f"Actors: {len(df_actors)}")
print(f"Movies: {len(df_movies)}")
print(f"Actors_Movies: {len(df_actors_movies)}")
print(f"Rentals: {len(df_rentals)}")
print(f"Reviews: {len(df_reviews)}")