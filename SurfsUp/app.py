# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import pandas as pd

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
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
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Create query and dataframe
    data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > '2016-08-23').order_by(Measurement.date).all()
    df = pd.DataFrame(data, columns =['Date', 'Precipitation (in.)'])

    # Create dictionary from dataframe
    prcp_dict = dict(df.values)

    session.close()

    # Return JSON representation of dictionary
    return jsonify(prcp_dict)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Create query and dataframe
    stations_data = session.query(Station.station).all()

    session.close()

    # Return stations list
    return jsonify(stations_data)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Create query and dataframe
    temps = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date > '2016-08-23').all()
    tobs_df = pd.DataFrame(temps, columns=['Date', 'Temp.'])

    # Create dictionary from dataframe
    tobs_dict = dict(tobs_df.values)

    session.close()

    # Return JSON representation of dictionary
    return jsonify(tobs_dict)

@app.route("/api/v1.0/<start>")
def start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Create query
    temps = session.query(Measurement.tobs).filter(Measurement.date >= start).all()

    # Do some maths
    temps_list = []
    temps_list.append(np.amin(temps))
    temps_list.append(np.amax(temps))
    temps_list.append(np.average(temps))

    session.close()

    # Return list
    return jsonify(temps_list)
    


@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

     # Create query
    temps = session.query(Measurement.tobs).filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    # Do some maths
    temps_list = []
    temps_list.append(np.amin(temps))
    temps_list.append(np.amax(temps))
    temps_list.append(np.average(temps))

    session.close()

    # Return list
    return jsonify(temps_list)