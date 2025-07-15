import datetime
import pathlib


def timestamp(datetimestr):
    return datetime.datetime.fromisoformat(datetimestr).timestamp()
    

DBNAME = "bresser.db"
DBPATH = pathlib.Path(__file__).parent.joinpath(DBNAME)
DBFIELDS = dict(time=dict(db="REAL", cfn=timestamp), temperature_C=dict(db="REAL", cfn=float), humidity=dict(db="REAL", cfn=float), wind_dir_deg=dict(db="REAL", cfn=float), wind_avg_m_s=dict(db="REAL", cfn=float), wind_max_m_s=dict(db="REAL", cfn=float), rain_mm=dict(db="REAL", cfn=float))
DBVALUES = ", ".join(f":{key}" for key in DBFIELDS)


def convert_datetime(value):
    """Convert ISO 8601 datetime to datetime.datetime object."""
    return datetime.datetime.fromisoformat(value)


def adapt_datetime_iso(value):
    """Adapt datetime.datetime to timezone-naive ISO 8601 date."""
    return value.replace(tzinfo=None).isoformat()
