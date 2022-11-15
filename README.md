# PYTHON SYNC AUTOMATION

Python sync automation is a Python library for sync data from database oracle (premise) to database postgresql (cloud)

## Installation
Set up the environment variables in .env file, example :

```bash
CHUNKSIZE=100

PGDATABASE=postgres
PGHOST=localhost
PGPASSWORD=secret
PGUSER=root
PGPORT=5432

ORADATABASE=oracle
ORAHOST=localhost
ORAPASSWORD=secret
ORAUSER=root
ORAPORT=5432
```

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the libraries.

```bash
# Install the dependencies
$ pip install -r requirements.txt

# Use this command to edit a crontab entries
$ crontab -e

# Add this script (example)
$ * * * * * python3 ~/path/main.py

# To verify the file was successfully saved, you can use the command
$ crontab -l
```

## License

[MIT](https://choosealicense.com/licenses/mit/)