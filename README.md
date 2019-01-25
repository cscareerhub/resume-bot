[![Discord Chat](https://img.shields.io/discord/334891772696330241.svg)](https://discord.gg/ndFR4RF)
[![License](https://img.shields.io/github/license/CS-Career-Hackers/resume-bot.svg)](LICENSE)
# Resume-Bot

A bot that keeps track of resumes to be reviewed.

## Set up
### Prerequisites:
- Python 3.6+
- PostgreSQL
- pip3 (or have pip reference Python3 installation)

### Installation
Note: this should be pretty generic among all Linux, MacOS, and Windows systems.

- Run `service postgresql start` to enable the Postgres server. _**Note:** this step may get removed in the future for dockerfile._
- Move into the directory with `main.py`
- Run `pip3 install -r requirements.txt` (or `pip install -r requirements.txt` depending on Python versions)
- Create a `.env` file in the current directory. It should contain the following variables:
```
TOKEN=<Discord Developer Token>
USERNAME=<PostgreSQL account username for bot>
PASSWORD=<PostgreSQL account password for bot>
DB_NAME=<Name of the database>
DB_HOST=<Host of the database>
ENVIRONMENT=<DEV or PROD>
DEV_CHAN=<Channel to listen on in development>
PROD_CHAN=<Channel to listen on in production>
```
_Note here that you will need to create an account for the postgres user manually, as well as a database for the bot to use._

- Run `python3 main.py` (or again depending on install `python main.py` could suffice).<br>
If successful, this should be present on the terminal:
```
Logged in as
Resume-Bot
00000000000000 # This will vary as it is the Bot ID
------
``` 

## Usage

* Run `python3 main.py` to start the bot.
