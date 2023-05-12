import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import pandas as pd
import datetime as dt

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station

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
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<enddate><br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation ():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of stations precipitation"""
    # The most recent date in the data set.
    recent_date = dt.date(2017, 8, 23)

    # The date one year from the last date in data set.
    year_ago = recent_date - dt.timedelta(days=365)

    #A query to retrieve the data and precipitation scores
    prcp_score = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >= year_ago).all()

    session.close()

    # Create a dictionary from the date as a key and prcp as value
    station_prec = []
    for date, precipitation in prcp_score:
        station_dict = {}
        station_dict["Date"] = date
        station_dict["Precipitation"] = precipitation
        
        station_prec.append(station_dict)

    return jsonify(station_prec)



@app.route("/api/v1.0/stations")
def stations ():
    # Create our session (link) from Python to the DB
    session = Session(engine)
  
    # Design a query to calculate the total number of stations in the dataset

    total_stations = session.query(measurement.station).distinct().all()
    
    session.close()

    # Unravel results into a 1D array and convert to a list
    station_name = list(np.ravel(total_stations))

    # return the jason list of stations
    return jsonify(station_name)
    
    
@app.route("/api/v1.0/tobs")
def temp():

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # List the dates and temperature observations of the most-active station for the previous year of data.
    active_stations = session.query(measurement.station, func.count(measurement.station)).group_by(measurement.station).order_by(func.count(measurement.station).desc()).all()

    session.close()

    # Unravel results into a 1D array and convert to a list
    active_stations = list(np.ravel(active_stations))

     # return the jason list of stations
    return jsonify(active_stations)

@app.route("/api/v1.0/<start>")

def dates (start):


    # Create our session (link) from Python to the DB
    session = Session(engine)

   
   # calculate TMIN, TAVG, TMAX with start 
    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= start).all()

    session.close()

    # Unravel results into a 1D array and convert to a list
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

@app.route("/api/v1.0/<start>/<end>")
def ends(start, end):

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # calculate TMIN, TAVG, TMAX with stop 
    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date <= end, measurement.date >= start).all()
    
    session.close()

    # Unravel results into a 1D array and convert to a list
    temps = list(np.ravel(results))
    return jsonify(temps =temps)


if __name__ == '__main__':
    app.run(debug=True)
