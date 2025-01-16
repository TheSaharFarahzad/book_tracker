# Book Tracker

**Book Tracker** is a Django project developed as a practical example for my article on "Performance Optimization with Django Debug Toolbar" published on Medium. The project features a book list displayed on the home page, where users can explore books added by the admin. Each user can manage their personal book list by adding books, tracking reading progress (start/end dates), updating status, leaving ratings, and writing notes.

Explore different stages of the project by clicking on the version titles below:

- [Initial Unoptimized Project](https://github.com/TheSaharFarahzad/book_tracker/tree/v1)
- [Django Debug Toolbar for Performance Monitoring](https://github.com/TheSaharFarahzad/book_tracker/tree/v2)
- [Using `select_related` and `prefetch_related` to Solve the N+1 Query Problem](https://github.com/TheSaharFarahzad/book_tracker/tree/v3)
- [Filtering for Query Optimization](https://github.com/TheSaharFarahzad/book_tracker/tree/v4)
- [Optimizing Complex Queries with Q Objects](https://github.com/TheSaharFarahzad/book_tracker/tree/v5)
- [Using `only` and `defer` to Fetch Required Fields](https://github.com/TheSaharFarahzad/book_tracker/tree/v6)
- [Pagination to Fix Page Loading Issues](https://github.com/TheSaharFarahzad/book_tracker/tree/v7)
- [Annotations and Aggregations for Database-Level Computations](https://github.com/TheSaharFarahzad/book_tracker/tree/v8)


## Clone the Repository

To clone the repository initially:

```bash
git clone https://github.com/TheSaharFarahzad/book_tracker.git
```

## System Requirements

You'll need Python 3, python3-pip, python3-venv to be installed on your machine.

## Python Environment and Install Necessary Packages

### 1. Set up virtual environment:

Windows:
```bash
cd book_tracker
python -m venv venv
```

Linux:
```bash
cd book_tracker
python3 -m venv .venv
```

**NOTE**: Ensure you add virtual environment directory to `.gitignore` to avoid committing unnecessary files to the repository.

### 2. Activate the environment:

Windows:
```bash
venv\Scripts\activate
```

Linux:
```bash
source .venv/bin/activate
```

### 3. Install all requirements:

```bash
pip install -r requirements.txt
```

## Run Server

Execute the `migrate` command to create your database tables:

```bash
python manage.py migrate
```

Run this command to populate the database with all data in `tracker/management/commands/populate_db.py`:
```bash
python manage.py populate_db
```

Then run the following command:

```bash
python manage.py runserver
```

You can see the application in a browser at [http://localhost:8000](http://localhost:8000).
