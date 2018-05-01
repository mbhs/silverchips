[![Build Status](https://travis-ci.org/mbhs/silverchips.svg?branch=master)](https://travis-ci.org/mbhs/silverchips)
[![codecov](https://codecov.io/gh/mbhs/silverchips/branch/master/graph/badge.svg)](https://codecov.io/gh/mbhs/silverchips)
[![CodeFactor](https://www.codefactor.io/repository/github/mbhs/silverchips/badge)](https://www.codefactor.io/repository/github/mbhs/silverchips)
# Silver Chips Online

Silver Chips Online is an award-winning school newspaper from Montgomery Blair
High School in Silver Spring, MD. Further specifications for things like data models,
site maps, and feature wishlists are stored in the boards and issues. Note that
while the intent is to keep this framework generic as to support news sites for
different organizations, parts may be hardocoded until a full fork and release.

## Getting Started
Prequisites: Python 3+, `pip`, `virtualenv`, `virtualenvwrapper-win`, and Ruby `sass`.
`pip` should come shipped with Python 3 when you install it (just make sure it's on PATH); to install `virtualenv` and `virtualenvwrapper-win`, run (on the command line):
  - `pip install virtualenv`
  - `pip install virtualenvwrapper-win`
### Quick Start
1. Clone this repository: `git clone https://github.com/markojungo/silverchips.git`.
2. `cd` into `silverchips`: `cd silverchips`.
3. Make a virtual environment: `mkvirtualenv sco`. (sco) should now appear at the beginning of your command line.
   - NOTE: Make sure to run `workon sco` every time you reopen the command line, or else you'll get an error
4. Install requirements: `pip install -r requirements.txt`. Run `pip freeze`; you should see **at least**:
   - django>=2.0
   - django_forms_bootstrap>=3.1.0
   - django-static-precompiler
   - django-inspect
   - Pillow>=4.1.1
   - codecov>=2.0.9
   - django-autocomplete-light
   - six
5. Make migrations and apply:
   - `python manage.py makemigrations core`
   - `python manage.py migrate`
6. Load test data: `manage.py loaddata core/fixtures/recent.json`.
7. Run server: `python manage.py runserver`.
8. Go to: `localhost:8000`

And voila!
