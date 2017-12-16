# HYDT

How You Doin Today?

## Installation

* Python3.5+

### Setup a Virtual Environment

```
cd /to/where/you/want/the/virt/env/stored
python3 -m venv env
```

### Start Virtual Environment

```
cd /to/where/you/stored/the/virt/env/stored
source env/bin/activate
```

### Install the Requirements

```
cd /to/where/this/project/lives
pip install -r requirements.txt
```

## Running the Application

There are a few options hidden behind the `hydt.py` file:

* `build_database` -- This will create a local SQLite file
* `migrate` -- This will update the database based on schema changes in the `models.sql` file
* `start` -- This will start the server on port 9090
