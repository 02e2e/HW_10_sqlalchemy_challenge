import numpy as np
import datetime as dt 

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

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
        f"/api/v1.0/preciptation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/preciptation<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query dates and prcp values 
    results = session.query(measurement.date,measurement.prcp)\
        .order_by(measurement.date).all()

    session.close()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))

    return jsonify(all_names)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all stations
    results = session.query(station.name, station.station).all()

    session.close()


    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)


    last_measurement = session.query(measurement.date).order_by(measurement.date.desc()).first().date
    last_date = dt.datetime.strptime(last_measurement, "%Y-%m-%d").date()
    start = last_date - dt.timedelta(days=365)
    start_date = start.strftime("%Y-%m-%d")
    
    results = session.query(measurement.tobs, measurement.station)\
    .filter(measurement.date.between(start_date,last_date))\
    .order_by(measurement.date.desc()).all()
    
    session.close()

    # Convert list of tuples into normal list
    all_tobs = list(np.ravel(results))

    return jsonify(all_tobs)


@app.route("/api/v1.0/<start>")
def temp_range_start(start):
   

    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    last_measurement = session.query(measurement.date).order_by(measurement.date.desc()).first().date
    
    last_date = dt.datetime.strptime(last_measurement, "%Y-%m-%d").date()
    
    start = last_date - dt.timedelta(days=365)
    
    start_date = start.strftime("%Y-%m-%d")
    
    max = func.max(measurement.tobs)
    min = func.min(measurement.tobs)
    avg = func.avg(measurement.tobs)

    results = session.query(measurement.station, max, min, avg)\
    .filter(measurement.date >= start_date).all()

 

    session.close()    
    all_start = list(np.ravel(results))
    return jsonify(all_start)


@app.route("/api/v1.0/<start>/<end>")
def temp_range_start_end(start, last_date):


    # Create our session (link) from Python to the DB
    session = Session(engine)

    last_measurement = session.query(measurement.date).order_by(measurement.date.desc()).first().date
    last_date = dt.datetime.strptime(last_measurement, "%Y-%m-%d").date()
    start = last_date - dt.timedelta(days=365)
    start_date = start.strftime("%Y-%m-%d")
    
    max = func.max(measurement.tobs)
    min = func.min(measurement.tobs)
    avg = func.avg(measurement.tobs)
    
    results = session.query(measurement.station, max, min, avg)\
    .filter(measurement.date >= start_date)\
    .filter(measurement.date <= last_date).all()

    session.close()    
    all_end = list(np.ravel(results))
    return jsonify(all_end)


if __name__ == '__main__':
    app.run(debug=True)
