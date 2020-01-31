[![Build Status](https://travis-ci.org/mbhs/silverchips.svg?branch=master)](https://travis-ci.org/mbhs/silverchips)
[![codecov](https://codecov.io/gh/mbhs/silverchips/branch/master/graph/badge.svg)](https://codecov.io/gh/mbhs/silverchips)
# Silver Chips Online

Silver Chips Online is an award-winning school newspaper from Montgomery Blair
High School in Silver Spring, MD. Further specifications for things like data models,
site maps, and feature wishlists are stored in the boards and issues. Note that
while the intent is to keep this framework generic as to support news sites for
different organizations, parts may be hardcoded until a full fork and release.

## Getting Started
Prequisites: Python 3+, `pip`, and `pipenv`. Ruby, `gem`, and `sass` (gem sass only) for static precompilation. `postgresql-server-dev-11` for `psycopg2`, the postgres database interface, to install properly.
`pip` should come shipped with Python 3 when you install it (just make sure it's on PATH); to install `virtualenv` and `virtualenvwrapper-win`, run (on the command line):
  - `pip install pipenv`
### Quick Start
1. Clone this repository: `git clone https://github.com/mbhs/silverchips.git`.
2. `cd` into `silverchips`: `cd silverchips`.
3. Run `pipenv --three install --dev` to make a new virtualenv/pipenv
4. Run `pipenv shell` to enter the new environment
5. Make migrations and apply:
   - `python manage.py makemigrations core`
   - `python manage.py migrate --run-syncdb`
6. Load test data: `python manage.py loaddata core/fixtures/recent.json`.
7. Run server: `python manage.py runserver`.
8. Visit in browser: `localhost:8000`

And voila!

## Organization
Django code is organized broadly into *models*, which store data in the database and you can interact nicely with in
Python; *views*, which perform server-side logic on models data, possibly making changes or organizing data for display;
and *templates*, which render view results to HTML. For more information, see the excellent
[official Django tutorial](https://docs.djangoproject.com/en/2.0/intro/tutorial01/).

This code is organized into three main Django apps and a number of auxiliary scripts. The apps are:

* `core`: Shared functionality between all aspects of Silver Chips Online. Models live here.
* `home`: Public-facing functionality that any user can see when they load the site.
* `staff`: Private functionality that only Silver Chips staff accesses to administer the newspaper.


## Advanced

### Creating Fixtures

Simply run the command `python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes.contenttype -e auth.permission > core/fixtures/recent.json`.
