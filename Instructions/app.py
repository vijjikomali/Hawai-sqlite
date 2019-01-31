#1. Import Flask

import datetime as dt
import pandas as pd
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#-----------------------------------------------
# Flask App Setup                              |
#-----------------------------------------------

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(bind=engine)

# 2.reate an app
app = Flask(__name__)

# 3. Define static routes
@app.route("/")
def Opening():
       
        return (
                "<h1>Hello, Everyone</h1><p>Welcome to the Climate Analysis of Hawaii!</p>"
                
                f"<H3>!<br/><br />"
                f"<br/>"
                f"Climate Data:<br/>"
                f"<br/>"
                f"/api/v1.0/precipitation<br/>"
                f"-- The past year's precipitation data<br/>"
                f"<br/>"
                f"/api/v1.0/stations<br/>"
                f" - Local observation stations<br/>"
                f"<br/>"
                f"/api/v1.0/tobs<br/>"
                f"- The past year's temperature observatons<br/>"
                f"<br/>"
                f"/api/v1.0/start<br/>"
                f" - Temperature statistics for all dates past and including the given <em>start date</em> (Please use YYYY-MM-DD)<br/>"
                f"<br/>"
                f"/api/v1.0/start/end<br/>" 
                f"- Temperature statistics for the given <em>start date/end date</em> (Please use YYYY-MM-DD)<br/>"
        )
# 4. Define main behavior
if __name__ == '__main__':
        app.run(debug=True) 

# 5. Define static route - precipitation on Measurement Table
@app.route("/api/v1.0/precipitation")
def precipt():
#    * Query for the dates and precipitation observations from the last year.
#           * Convert the query results to a Dictionary using `date` as the key and `prcp` as the value.
#           * Return the json representation of your dictionary.
       
        month_presp= session.query(Measurement.date).order_by(Measurement.id.desc()).first()
        last_year = dt.date(2017,8,23) - dt.timedelta(days=365)
        
        rain = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= last_year).\
        order_by(Measurement.date).all()
        presp_df = pd.DataFrame(rain)


# Create a list of dicts with `date` and `prcp` as the keys and values
        rain_totals = []
        for result in rain:

            row = {}
            row["date"] = rain[0]
            row["prcp"] = rain[1]
            rain_totals.append(row)
   # Jsonify the list
        return jsonify(month_presp)
   

## staions'''''''
@app.route("/api/v1.0/stations")
def stations():
       
        list_st= session.query(Measurement.tobs).order_by(Measurement.tobs.desc()).first()
        
        active_station = session.query(Measurement.station, func.count(Measurement.tobs)).group_by(Measurement.station).\
        order_by(func.count(Measurement.tobs).desc()).all()
        
        hitemp_obsrv= session.query(Measurement.station, Measurement.tobs).\
        filter(Measurement.station  == 'USC00519281').\
        filter(Measurement.date > last_year).all()
        return jsonify(stations.to_dict())
        

##  TOBS

@app.route("/api/v1.0/tobs")
def tobs():
    """Return a list of temperatures for prior year"""
#  ////  Query for the dates and temperature observations from the last year.
#  ////  Convert the query results to a Dictionary using `date` as the key and `tobs` as the value.
#  ////  Return the json representation of your dictionary.
    month_presp = session.query(Measurements.date).order_by(Measurements.date.desc()).first()
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    temperature = session.query(Measurements.date, Measurements.tobs).\
        filter(Measurements.date > last_year).\
        order_by(Measurements.date).all()

# Create a list of dicts with `date` and `tobs` as the keys and values
    temperature_totals = []
    for result in temperature:
        row = {}
        row["date"] = temperature[0]
        row["tobs"] = temperature[1]
        temperature_totals.append(row)

    return jsonify(temperature_totals)


@app.route("/api/v1.0/<start>")
def trip1(start):

 # go back one year from start date and go to end of data for Min/Avg/Max temp   
    start_date= dt.datetime.strptime(start, '%Y-%m-%d')
    last_year = dt.timedelta(days=365)
    start = start_date-last_year
    end =  dt.date(2017, 8, 23)
    trip_data = session.query(func.min(Measurements.tobs), func.avg(Measurements.tobs), func.max(Measurements.tobs)).\
        filter(Measurements.date >= start).filter(Measurements.date <= end).all()
    trip = list(np.ravel(trip_data))
    return jsonify(trip)


###----------------------------------------#######

@app.route("/api/v1.0/<start>/<end>")
def trip2(start,end):

  # go back one year from start/end date and get Min/Avg/Max temp     
    start_date= dt.datetime.strptime(start, '%Y-%m-%d')
    end_date= dt.datetime.strptime(end,'%Y-%m-%d')
    last_year = dt.timedelta(days=365)
    start = start_date-last_year
    end = end_date-last_year
    trip_data = session.query(func.min(Measurements.tobs), func.avg(Measurements.tobs), func.max(Measurements.tobs)).\
        filter(Measurements.date >= start).filter(Measurements.date <= end).all()
    trip = list(np.ravel(trip_data))
    return jsonify(trip)



if __name__ == '__main__':
        app.run(debug=True, port=5002)