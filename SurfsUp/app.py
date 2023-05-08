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
def home():
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
    for date, precipatation in prcp_score:
        station_dict = {}
        station_dict["date"] = date
        station_dict["precipatation"] = precipatation
        
        station_prec.append(station_dict)

    return jsonify(station_prec)



@app.route("/api/v1.0/stations")
def stations ():
    # Create our session (link) from Python to the DB
    session = Session(engine)
  
    # Design a query to calculate the total number of stations in the dataset

    total_stations = session.query(measurement.station).distinct()
    
    session.close()

    # return the jason list of stations
    for station in total_stations:
        return jsonify(station)
    
@app.route("/api/v1.0/tobs")
def temp():
    # List the stations and their counts in descending order.
    active_stations = session.query(measurement.station, func.count(measurement.station)).group_by(measurement.station).order_by(func.count(measurement.station).desc()).all()

    session.close()

    for active_station in active_stations:
        return jsonify(active_station)
    

if __name__ == '__main__':
    app.run(debug=True)
