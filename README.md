pip install -r requirements.txt

Also need to install a database driver for this, like pymysql or similar.

The environment variable ALEXA_DATABASE_URL should be set to the SQLAlchemy
connection string to access the database.

additionally, alembic.ini should be modified to change line #35 to 
`sqlalchemy.url = YOUR_DATABASE_CONNECTION_STRING`


