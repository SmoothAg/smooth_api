

from sqlalchemy import Column, Integer, String
from database import Base


class Control(Base):
    __tablename__ = "control"

    id = Column(Integer, primary_key=True, index=True)
    rover_number = Column(String)
    rover_name = Column(String)
    location = Column(String)
    status = Column(String)
    fuel_lev = Column(String)
    feed_lev = Column(String)
    input_comm = Column(String)
    