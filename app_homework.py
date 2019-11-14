
from flask import Flask, jsonify
import numpy as np
import pandas as pd

import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

engine = create_engine("sqlite:///hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)


app= Flask(__name__)

@app.route("/")
def welcome ():
    return(f" Welcome <br/>"
    f" available routes"
    f"api/v1.0/precipitation"
    f"/api/v1.0/stations"
    f"/api/v1.0/tobs"
    f"/api/v1.0/<start>"
    f"//api/v1.0/<start>/<end>")


@app.route("/api/v1.0/precipitation")
def precipitation ():
    session.query(Measurement.date).order_by(Measurement.date.desc()).first()

    pr_data = session.query(Measurement.date, Measurement.prcp).\
              filter(Measurement.date >= '2016-08-23').\
              filter(Measurement.date <= '2017-08-23').\
              order_by(Measurement.date).all()
            
            

                                                          
    return jsonify(pr_data)


@app.route("/api/v1.0/stations")
def stations():
    stations = session.query(Measurement.station, func.count(Measurement.station)).\
    group_by(Measurement.station).\
    order_by(func.count(Measurement.station).desc()).all()

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == "USC00519281").\
        filter(Measurement.date >='2016-08-23'). all()
    return jsonify(results)

@app.route("/api/v1.0/<start>")
def temperatures(start):
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()

    return jsonify(results)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    return jsonify(results)

if __name__=="__main__":
    app.run(debug = True)
