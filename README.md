pip install -r requirements.txt

Also need to install a database driver for this, like pymysql or similar.

The environment variable ALEXA_DATABASE_URL should be set to the [SQLAlchemy
connection string](http://docs.sqlalchemy.org/en/latest/core/engines.html#database-urls) to access the database.

additionally, alembic.ini should be modified to change line #35 to 
`sqlalchemy.url = YOUR_DATABASE_CONNECTION_STRING`

To initially setup the schema for a database, you can run `alembic upgrade head` 

If a database is already provisioned and has the table schema necessary, then
simply running `python bestbuy.py` will load all of the top new tech products
and store them in the database.
