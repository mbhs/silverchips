[![Build Status](https://travis-ci.org/mbhs/silverchips.svg?branch=master)](https://travis-ci.org/mbhs/silverchips)
[![codecov](https://codecov.io/gh/mbhs/silverchips/branch/master/graph/badge.svg)](https://codecov.io/gh/mbhs/silverchips)
# Silver Chips Online

Silver Chips Online is an award-winning school newspaper from Montgomery Blair
High School in Silver Spring, MD. Further specifications for things like data models,
site maps, and feature wishlists are stored in the boards and issues. Note that
while the intent is to keep this framework generic as to support news sites for
different organizations, parts may be hardcoded until a full fork and release.

## Getting Started
It's recommended to use the supplied `Dockerfile` and `docker-compose.yml`. Simply clone the repository and run `docker-compose up` and the site will be up and running.

### Manual Installation
You have to install Python 3+, pip, sass, and pipenv. The version of `sass` that's installable via `gem` is outdated and **will not** work. If using postgres, the postgres server development libraries need to be installed (`postgresql-server-dev-12` on Ubuntu).
### Environment setup
1. Clone this repository: `git clone https://github.com/mbhs/silverchips.git`.
2. `cd` into `silverchips`: `cd silverchips`.
3. Run `pipenv --three install --dev` to install the environment. If this doesn't work, run `pipenv lock --pre --clear` beforehand.
4. Run `pipenv shell` to enter the new environment.
5. Make migrations and apply:
   - `python manage.py makemigrations`
   - `python manage.py migrate`
6. Make an appropriate `secure_settings.py` in the `silverchips` folder. An example can be found in `silverchips/secure_settings.py.postgres_example`.
7. If using postgres, you can load the `sco.sql` database dump into the database. If not, you can load a fixture: `python manage.py loaddata core/fixtures/recent.json`. Note that the database dump is preferred since the fixture is missing many things, such as permissions.
8. Run the server: `python manage.py runserver`.
9. Visit in browser: `localhost:8000`.


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

### Development Notes

The `core/fixtures/testing.json` fixture and `sco.sql` database dump has a superuser with username `admin` and password `password`.
