import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

#reflect an existing database into a new model
Base = automap_base()

#reflect the tables
Base.prepare(engine, reflect=True)

#Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt<br/>"
        f"/api/v1.0/&lt;start&gt/&lt;end&gt"
    )
 
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query percipiration based off the date key passed to the api
    percip_data = session.query(Measurement.date, Measurement.prcp).all()
    session.close()

    # INSTRUCTIONS: Convert the query results to a Dictionary using date as the key and prcp as the value
    # Per instructions this returns <Date>:<Value> - Key:Value Pair
    
    # Create a dictionary from the row data and append to a based off date
    percipitation = []
    for date, prcp in percip_data:
        percip_dict = {}
        percip_dict[date] = prcp 
        percipitation.append(percip_dict)
        
    #INSTRUCTIONS: Return the JSON representation of your dictionary.
    return jsonify(percipitation)
  
@app.route("/api/v1.0/stations")
def station():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all passengers
    station_results = session.query(Station.station).all()
    session.close()

    # Convert list of tuples into normal list
    station_list = list(np.ravel(station_results))

    #INSTRUCTIONS: Return a JSON list of stations from the dataset.
    return jsonify(station_list)
  
@app.route("/api/v1.0/tobs")
def tobs():
    #INSTRUCTIONS: query for the dates and temperature observations from a year from the last data point.
    
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #Calculate the date 1 year ago from the last data point in the database
    from dateutil.relativedelta import relativedelta
    import datetime

    max_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first().date
    max_date = datetime.datetime.strptime(max_date, '%Y-%m-%d')
    year_ago = max_date - relativedelta(months=12)

    # Perform a query to retrieve the data and precipitation scores
    percip_data = session.query(Measurement.date, Measurement.tobs)\
                  .filter(Measurement.date >= year_ago).all()
                  
    #Create a dictionary from the row data and append to a based off date
    percipitation = []
    for date, tobs in percip_data:
        percip_dict = {}
        percip_dict[date] = tobs 
        percipitation.append(percip_dict)            

    #INSTRUCTIONS: Return a JSON list of Temperature Observations (tobs) for the previous year.
    return jsonify(percipitation)   

@app.route("/api/v1.0/<start>")
def start_date(start):
    #INSTRUCTIONS: When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.
  
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    tobs_start_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))\
                      .filter(Measurement.date >= start)\
                      .all()
    session.close()

    # Convert list of tuples into normal list
    tobs_list = list(np.ravel(tobs_start_data))
    
    #INSTRUCTIONS: Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
    return jsonify(tobs_list)
    
    
@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
    #INSTRUCTIONS: When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.
  
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    tobs_start_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))\
                      .filter(Measurement.date >= start)\
                      .filter(Measurement.date <= end)\
                      .all()
    session.close()

    # Convert list of tuples into normal list
    tobs_list = list(np.ravel(tobs_start_data))
    
    #INSTRUCTIONS: Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
    return jsonify(tobs_list)