#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from asyncio.base_subprocess import WriteSubprocessPipeProto
import json
import webbrowser
import dateutil.parser
import babel
from datetime import datetime
import os
from flask import Flask, render_template, request, Response, flash, redirect, url_for,jsonify,abort
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from os import sys

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
app.debug = True
migrate = Migrate(app, db)

# TODO: connect to a local postgresql database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://emmilina:emmilina@localhost:5432/fyyur'

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'venue'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    genres= db.Column(db.String(120))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    facebook_link = db.Column(db.String(500))
    image_link = db.Column(db.String(500))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    website_link = db.Column(db.String(500))
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(500))
    
    def __init__(self, name, city, state, address, phone, genres, facebook_link, image_link,website_link, seeking_talent,seeking_description):
       self.name = name
       self.city = city
       self.state = state
       self.address = address
       self.phone = phone
       self.genres =genres
       self.facebook_link = facebook_link
       self.image_link = image_link
       self.website_link = website_link
       self.seeking_talent = seeking_talent
       self.seeking_description = seeking_description
class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    facebook_link = db.Column(db.String(500))
    image_link = db.Column(db.String(500))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    website_link = db.Column(db.String(500))
    seeking_venue = db.Column(db.Boolean,default=False)
    seeking_description =db.Column(db.String(500))
    
# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
    def __init__(self, name, city, state, address, phone, genres, facebook_link, image_link,website_link, seeking_venue,seeking_description):
       self.name = name
       self.city = city
       self.state = state
       self.address = address
       self.phone = phone
       self.genres =genres
       self.facebook_link = facebook_link
       self.image_link = image_link
       self.website_link = website_link
       self.seeking_venue = seeking_venue
       self.seeking_description = seeking_description
class Show(db.Model):
    __tablename__ = 'show'

    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)
    start_time = db.Column(db.DateTime)

    def __init__(self, artist_id, venue_id,start_time):
       self.artist_id = artist_id
       self.venue_id = venue_id
       self.start_time = start_time
       


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
  data=Venue.query.all()
  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  response={
    "count": 1,
    "data": [{
      "id": 2,
      "name": "The Dueling Pianos Bar",
      "num_upcoming_shows": 0,
    }]
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  data1 = Venue.query.get(venue_id) 

 
  data = list(filter(lambda d: d['id'] == venue_id, [data1]))[0]
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  error =False
  form = VenueForm(request.form)

  try:
      name = form.name.data
      genres= form.genres.data
      address = form.address.data
      city = form.city.data
      state = form.state.data
      phone = form.phone.data
      website_link = form.website_link.data
      facebook_link =form.facebook_link.data
      seeking_talent = form.seeking_talent.data
      seeking_description = form.seeking_description.data
      image_link = form.image_link.data


      venue = Venue(name,genres,address,city, state,  phone,  facebook_link, image_link,website_link, seeking_talent,seeking_description )
      db.session.add(venue)
      db.session.commit();
      # flash('Venue ' + form.name.data + ' was successfully listed!')

      return render_template('pages/home.html')


 
  except:
   db.session.rollback()
   error=True
   print(sys.exc_info())
  finally:
   db.session.close()
   if  error == True:
     abort(400)
   else:            
        return render_template('pages/home.html')
    
        
  
  # TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  try:
        #Todo.query.filter_by(id=todo_id).delete()
   venue = Venue.query.get(venue_id) 
   db.session.delete(venue) # or...
   Venue.query.filter_by(id=venue_id).delete()
   db.session.commit() 
       
  except:
   db.session.rollback()
   error = True
  finally:
   db.session.close()
  if error:
   abort(500)
  else:
    return jsonify({'success': True})
         
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  data=Artist.query.all()
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  response={
    "count": 1,
    "data": [{
      "id": 4,
      "name": "Guns N Petals",
      "num_upcoming_shows": 0,
    }]
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
  data1=Artist.query.filter(id=artist_id)
  
  data = list(filter(lambda d: d['id'] == artist_id, [data1]))[0]
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist=Artist.query.filter(artist_id==artist_id)
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  form = ArtistForm()
  try:
   
    artist = Artist.query.get(artist_id)
    artist.name = form.name.data
    artist.city = form.city.data
    artist.state = form.state.data
    artist.phone = form.phone.data
    artist.facebook_link =form.facebook_link.data
    artist.image_link = form.image_link.data
    artist.website_link = form.website_link.data
    artist.seeking_venue = form.seeking_venue.data
    artist.seeking_description = form.seeking_description.data
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()
    return redirect(url_for('index'))

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue=Venue.query.filter(venue=venue_id)
  # TODO: populate form with values from venue with ID <venue_id>
  form.name = venue.name
  form.city = venue.city
  form.address = venue.address
  form.phone = venue.phone
  form.facebook_link = venue.facebook_link
  form.image_link = venue.image_link
  form.website_link = venue.website_link
  form.state= venue.state
  form.seeking_talent = venue.seeking_talent
  form.seeking_description=venue.seeking_description
  
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  form = VenueForm()

  try:
    
    venue = Venue.query.get(venue_id)
    venue.name = form.name.data
    venue.city = form.city.data
    venue.state = form.state.data
    venue.address = form.address.data
    venue.phone = form.phone.data
    venue.facebook_link =form.facebook_link.data
    venue.image_link = form.image_link.data
    venue.website_link = form.website_link.data
    venue.seeking_talent = form.seeking_talent.data
    venue.seeking_description = form.seeking_description.data
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()
    return redirect(url_for('index'))
  # venue record with ID <venue_id> using the new attributes
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  form = ArtistForm(request.form)

  try:
      print(form.city.data)
      name = form.name.data
      city = form.city.data
      state = form.state.data
      phone = form.phone.data
      genres =  "".join(str(e) for e in form.genres.data)
      facebook_link =form.facebook_link.data
      image_link = form.image_link.data
      website_link = form.website_link.data
      seeking_venue = form.seeking_venue.data
      seeking_description = form.seeking_description.data
     

      artist = Artist( name,genres, city, state,  phone,  facebook_link, image_link,website_link, seeking_venue,seeking_description )
      db.session.add(artist)
      db.session.commit();
      flash('Artist ' + form.name.data + ' was successfully listed!')

      render_template('pages/home.html')

  except:
   db.session.rollback()
   error=True
  #  flash('An error occurred. Artist ' + artist.name + ' could not be listed.')
   print(sys.exc_info())
  finally:
   db.session.close()
  # TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., 
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  data= Show.query.all()
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
 form = ShowForm(request.form)

 try:
      artist_id = form.artist_id.data

      venue_id = form.venue_id.data
      start_time =form.start_time.data 
      

      show = Show(artist_id = artist_id,venue_id = venue_id,start_time = start_time)
      db.session.add(show)
      db.session.commit();
      flash('Show was successfully listed!')
      return render_template('pages/home.html')

      
 except:
   db.session.rollback()
   error=True
   print(sys.exc_info())
 finally:
   db.session.close()
  # on successful db insert, flash success
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
   return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
# if __name__ == '__main__':
#     app.run()

# Or specify port manually:
# '''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
# '''
