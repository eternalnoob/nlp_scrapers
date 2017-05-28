# designed to get the current top movies that are in theaters and export them to a database
import os
from sqlalchemy import create_engine
import microdata
import urllib
from lxml import html
from utility import typematch
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, JSON, Text, DECIMAL, Integer, String
from sqlalchemy.orm import sessionmaker
from decimal import Decimal
from imdbpie import Imdb
import json

engine = create_engine(os.environ.get('ALEXA_DATABASE_URL'))
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Movie(Base):
    __tablename__ = 'movies'

    id = Column(Integer,  autoincrement=True)
    imdb_id = Column(String(length=10), primary_key=True)
    actors = Column(JSON)  # actors have a nested JSON structure that would take very long to do using foreign key stuff
                           # What I'm doing here is interleaving the richer schema.org structure onto the API
    directors = Column(JSON)
    name = Column(Text)
    poster_url = Column(Text)
    plot_outline = Column(Text)
    runtime_seconds = Column(Integer)
    release_date_string = Column(String(length=12)) # '%Y-%m-%d' is python str(f/p)time format string
    avgrating = Column(DECIMAL)
    certification = String(length=1)

    def __init__(self, item, actors):
        self.name = item.title
        self.imdb_id = item.imdb_id
        self.avgrating = Decimal(item.rating)
        self.certification = item.certification
        self.plot_outline = item.plot_outline
        self.release_date = item.release_date
        self.runtime_seconds = item.runtime
        self.directors = {
                'all': [
                    {
                        'name': director.name,
                        'imdb_id': director.imdb_id
                        } for director in item.directors_summary
                    ]
                }
        self.actors = {'all': actors}

box_office_url = 'http://www.imdb.com/chart/boxoffice'
imdbbaseurl = 'http://www.imdb.com'
imdb_base_name_url = 'http://www.imdb.com/name/'
item_feed = html.fromstring(urllib.request.urlopen(box_office_url).read())

movie_ids = [x.get('data-tconst') for x in
            item_feed.find_class('wlb_ribbon')]

imdb = Imdb(anonymize=True)

movies = list(map(imdb.get_title_by_id, movie_ids))
actors_by_movie = [] 

for movie in movies:
    movie_cast = []
    for actor in movie.cast_summary:
        imdb_id = actor.imdb_id
        actor_schema = next((x for x in microdata.get_items(
                urllib.request.urlopen(imdb_base_name_url+imdb_id))
                if typematch(x, 'http://schema.org/Person')), None)
        movie_cast.append(json.loads(actor_schema.json()))
    actors_by_movie.append(movie_cast)

# should contain everything this library supports at the moment
# now add info about the actors

box_office_movies = [Movie(movie, actors) for movie, actors in zip(movies, actors_by_movie)]
for x in box_office_movies:
    session.add(x)
session.commit()
