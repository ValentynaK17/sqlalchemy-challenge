# Import the dependencies.
import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, and_, null

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)


# Save references to each table
Measurement=Base.classes.measurement
Station=Base.classes.station

# Create our session (link) from Python to the DB
session=Session(engine)

#################################################
# Flask Setup
#################################################
app=Flask(__name__)

#find the latest date in the db with observations
def most_recent_date(Classname):
    most_recent_date_tuple=session.query(Classname.date).order_by(Classname.date.desc()).first()
    most_recent_date_string=most_recent_date_tuple[0]
    return  most_recent_date_string

#find the earliest date in db with observations
def earliest_date(Classname):
    earliest_date_tuple=session.query(Classname.date).order_by(Classname.date).first()
    earliest_date_string=earliest_date_tuple[0]
    return earliest_date_string

#find the date, which is 365 days before the latest date in the db with observations
def start_date(Classname):
    most_recent_date_string=most_recent_date(Classname)
    starting_point = dt.datetime.strptime(most_recent_date_string,'%Y-%m-%d') 
    end_point=starting_point-dt.timedelta(days=365) 
    end_point_string=dt.datetime.strftime(end_point,'%Y-%m-%d')
    return  end_point_string

#jsonify the list of tuples of 2 elemetns
def jsonify_list_of_tuples(list_of_tuples):
    list_res = [{t1:t2} for t1, t2 in list_of_tuples]
    return jsonify(list_res)

#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    "List all the available routes."
    end_point_string=start_date(Measurement)
    most_recent_date_string=most_recent_date(Measurement)
    first_date=earliest_date(Measurement)
    return (
        f"Available Routes:<br/>"
        f" - /api/v1.0/precipitation<br/> This route returns a JSON list of precipitation data from {end_point_string} till {most_recent_date_string} inclusive <br/>"
        f" - /api/v1.0/stations<br/> This route returns a JSON list of stations <br/>"
        f" - /api/v1.0/tobs<br/> This route returns a JSON list of temperature observations data from {end_point_string} till {most_recent_date_string} inclusive, for the most active station (based on observations count)<br/>"
        f" - /api/v1.0/<start><br/> This route returns a JSON list of Average, Maximum amd Minimum temperatures for a date range starting a date, entered manually as a parameter in the URL in YYYY-MM-DD format, till the end of dataset <br/>"
        f" - /api/v1.0/<start>/<end><br/> This route returns a JSON list of Average, Maximum amd Minimum temperatures for a date range with start and end points, entered manually as a parameter in the URL in YYYY-MM-DD format <br/>"
    )

@app.route("/api/v1.0/precipitation")
def percipitation():
     end_point_string=start_date(Measurement)
     perc_scores_list_of_tuples=session.query(Measurement.date,Measurement.prcp).filter(Measurement.date>=end_point_string).order_by(Measurement.date).all()
     return jsonify_list_of_tuples(perc_scores_list_of_tuples)

@app.route("/api/v1.0/stations")
def stations():
    stations_list_of_tuples=session.query(Station.station.distinct()).order_by(Station.station).all()
    all_stations = [{"name":name[0]} for name in stations_list_of_tuples]
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def temperature_observations():
    most_active_station=session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()[0][0]
    end_point_string=start_date(Measurement)
    temperatures_list_of_tuples=session.query(Measurement.date,Measurement.tobs).filter(and_(Measurement.date>=end_point_string,Measurement.station==most_active_station)).order_by(Measurement.date).all()
    return jsonify_list_of_tuples(temperatures_list_of_tuples)

@app.route("/api/v1.0/<start>")
def temperatures(start):
    try: 
        dt.datetime.strptime(start, '%Y-%m-%d')
    except ValueError: 
        return jsonify({"error": f"Wrong date entered. Pleae use YYYY-MM-DD format for a date!"}), 404
    tempr=session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date>=start).all()
    (t_min, t_max, t_avg) = tempr[0]
    if t_avg is not None: 
        dict_t={
            "Min temperature":t_min,
            "Max temperature":t_max,
            "Average temperature":t_avg
        }
        return jsonify(dict_t)
    else:
        most_recent_date_string=most_recent_date(Measurement)
        return jsonify({"error": f"No data found for a range starting {start}. Please note that the latest date with data is {most_recent_date_string}"}), 404

@app.route("/api/v1.0/<start>/<end>")
def temperature_s_e(start,end):
    try: 
        dt.datetime.strptime(start, '%Y-%m-%d')
        dt.datetime.strptime(end, '%Y-%m-%d')
    except ValueError: 
        return jsonify({"error": f"Wrong date(s) entered. Pleae use YYYY-MM-DD format for a date!"}), 404
    tempr=session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(and_(Measurement.date>=start, Measurement.date<=end)).all()
    if tempr[0][2] is not None: 
        dict_t={
            "Min temperature":tempr[0][0],
            "Max temperature":tempr[0][1],
            "Average temperature":tempr[0][2]
        }
        return jsonify(dict_t)
    else:
        most_recent_date_string=most_recent_date(Measurement)
        first_date=earliest_date(Measurement)
        if start<end: 
            return jsonify({"error": f"No data found for a range [{start},{end}]. Please note that we have data for [{first_date},{most_recent_date_string}] date range."}), 404
        elif start==end:
            return jsonify({"error": f"No data found for {start} date. Please note that we have data for [{first_date},{most_recent_date_string}] date range."}), 404
        else:
            return jsonify({"error": f"Be sure that starting date point entered is less than or equal to the ending date point."}), 404

if __name__== "__main__":
    app.run(debug=True)