# MovieNest — NoSQL Migration Project

This project demonstrates the migration of a relational SQL Server database to a MongoDB NoSQL database using a movie rental platform called **MovieNest**.

\---

#### Project Overview

MovieNest is a movie rental database system that manages users, movies, actors, rentals, and reviews. The project starts with a relational database in **Microsoft SQL Server** and migrates the data to **MongoDB** using Python.

The migration is not a simple table-to-collection copy. Instead, the relational data is transformed into **denormalized MongoDB documents** with embedded actor information and derived fields such as rental counts, review counts, average ratings, total user rentals, and total user reviews.

\---

#### Technologies Used

* Microsoft SQL Server
* SQL Server Management Studio
* MongoDB
* MongoDB Compass
* Docker
* Python
* Power BI
* GitHub

\---

#### Python Libraries

|Library|Purpose|
|-|-|
|`pandas`|Data manipulation|
|`faker`|Synthetic data generation|
|`pyodbc`|SQL Server connection|
|`pymongo`|MongoDB connection|

Install all dependencies using:

```bash
pip install -r requirements.txt
```

\---

#### Setup Instructions

The following steps describe how to set up and run the complete MovieNest **SQL Server → MongoDB** migration pipeline.

#### Prerequisites

Before running the project, install the following software:

* Microsoft SQL Server
* SQL Server Management Studio (SSMS)
* Python 3.13 or newer
* Docker Desktop
* MongoDB Compass
* Power BI Desktop

Install the required Python libraries:

```bash
pip install pandas faker pyodbc pymongo
```

Or install from the requirements file:

```bash
pip install -r requirements.txt
```

\---

#### Step 1 — Create the SQL Server Database

1. Open **SQL Server Management Studio** and connect to your SQL Server instance.
2. Open the SQL script located at:

```
   sql/CreatingTables.sql
   ```

3. Execute the script to create the **MovieNest** database and all relational tables:

   * `USERS`
   * `ACTORS`
   * `MOVIES`
   * `ACTORS\_MOVIES`
   * `RENTALS`
   * `REVIEWS`

\---

#### Step 2 — Generate the Dataset

Navigate to the Python folder and run the data generation script:

```bash
cd python
python generate\_data.py
```

This script generates synthetic CSV files using the **Faker** library. The generated files are stored inside the `data/` folder:

|File|Table|Records|
|-|-|-:|
|`users.csv`|USERS|2,000|
|`actors.csv`|ACTORS|500|
|`movies.csv`|MOVIES|1,000|
|`actors\_movies.csv`|ACTORS\_MOVIES|3,000|
|`rentals.csv`|RENTALS|20,000|
|`reviews.csv`|REVIEWS|10,000|

**Total records: 36,500**

\---

#### Step 3 — Import CSV Files into SQL Server

Use SQL Server **BULK INSERT** commands to populate the relational database. Open and execute:

```
sql/DataInserts.sql
```

Import the tables in the following order to preserve all foreign key relationships:

1. `USERS`
2. `ACTORS`
3. `MOVIES`
4. `ACTORS\_MOVIES`
5. `RENTALS`
6. `REVIEWS`

After importing, verify the data using:

```sql
SELECT
  (SELECT COUNT(\*) FROM USERS),
  (SELECT COUNT(\*) FROM ACTORS),
  (SELECT COUNT(\*) FROM MOVIES),
  (SELECT COUNT(\*) FROM ACTORS\_MOVIES),
  (SELECT COUNT(\*) FROM RENTALS),
  (SELECT COUNT(\*) FROM REVIEWS);
```

**Expected result:** `2000 | 500 | 1000 | 3000 | 20000 | 10000`

\---

#### Step 4 — Start MongoDB

1. Start **Docker Desktop**.
2. Open PowerShell and run one of the following:

```bash
   docker-compose up -d
   ```

   or

   ```bash
   docker run -d --name movienest-mongodb -p 27017:27017 mongo
   ```

3. Verify the container is running:

   ```bash
   docker ps
   ```

4. Open **MongoDB Compass** and connect using:

   ```
   mongodb://localhost:27017
   ```

   \---

   #### Step 5 — Run the Migration

   Navigate to the Python folder and run the migration script:

   ```bash
cd python
python migration.py
```

   The script reads data from SQL Server and creates a new MongoDB database named **`MovieNestMongo`** with the following collections:

* `users`
* `movies`

  #### Derived Fields Computed During Migration

  **Movies collection:**

|Field|Description|
|-|-|
|`rentalCount`|Total number of times rented|
|`reviewCount`|Total number of reviews|
|`averageRating`|Average rating across all reviews|

**Users collection:**

|Field|Description|
|-|-|
|`totalRentals`|Total rentals by this user|
|`totalReviews`|Total reviews written by this user|

> \*\*Note:\*\* The migration script is \*\*idempotent\*\* — it can be executed multiple times without creating duplicate documents.

\---

#### Step 6 — Validate the Migration

Navigate to the validation folder and run the validation script:

```bash
cd validation
python validation.py
```

The validation script compares SQL Server and MongoDB and verifies:

* User count
* Movie count
* Rental count
* Review count
* Top rented movie
* Average rating by genre

The script should display **PASS** messages for all validation checks.

\---

#### Step 7 — Export MongoDB Collections

1. Open **MongoDB Compass**.
2. Export the following collections as CSV:

   * `users` → save as `data/mongo\_users.csv`
   * `movies` → save as `data/mongo\_movies.csv`

\---

#### Step 8 — Open Power BI Dashboard

1. Open **Power BI Desktop**.
2. Import the exported files via **Home → Get Data → Text/CSV**:

   * `mongo\_users.csv`
   * `mongo\_movies.csv`
3. Open the provided dashboard file:

```
   powerbi/MovieNest\_Dashboard.pbix
   ```

#### Dashboard Visualizations

|Visualization|Description|
|-|-|
|Top 10 Most Rented Movies|Movies ranked by rental count|
|Top 10 Most Active Users|Users ranked by total activity|
|Average Movie Rating by Genre|Genre-level rating breakdown|
|User Type Distribution|Breakdown of user types across the platform|

The visualizations use the **denormalized MongoDB collections** and the derived fields generated during migration.

\---

#### Project Pipeline

```
Python (Faker)
      │
      ▼
CSV Dataset
      │
      ▼
SQL Server
(Relational Database)
      │
      ▼
Python Migration Script
      │
      ▼
MongoDB
(Denormalized Collections)
      │
      ▼
Validation Script
      │
      ▼
Power BI Dashboard
```

The entire pipeline demonstrates **relational database design**, **NoSQL modeling**, **data transformation**, **migration**, **validation**, and **visualization** in a complete end-to-end data engineering workflow.

