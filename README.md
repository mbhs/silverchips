[![Build Status](https://travis-ci.org/mbhs/silverchips.svg?branch=master)](https://travis-ci.org/mbhs/silverchips)
[![codecov](https://codecov.io/gh/mbhs/silverchips/branch/master/graph/badge.svg)](https://codecov.io/gh/mbhs/silverchips)
[![CodeFactor](https://www.codefactor.io/repository/github/mbhs/silverchips/badge)](https://www.codefactor.io/repository/github/mbhs/silverchips)
# Silver Chips Online

Silver Chips Online is an award-winning school newspaper from Montgomery Blair
High School in Silver Spring, MD. Further specifications for things like data models,
site maps, and feature wishlists are stored in the boards and issues. Note that
while the intent is to keep this framework generic as to support news sites for
different organizations, parts may be hardocoded until a full fork and release.

## Quick Start
1. Clone this repository: `git clone https://github.com/markojungo/silverchips.git`.
2. `cd` into `silverchips`: `cd silverchips`.
3. Make a virtual environment: `mkvirtualenv sco`.
4. Install requirements: `pip install -r requirements.txt`.
5. Make migrations and apply:
  - `python manage.py makemigrations core`
  - `python manage.py migrate`
6. Load test data: `manage.py loaddata core/fixtures/recent.json`.
6. Run server: `python manage.py runserver`.
