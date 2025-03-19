from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from db import Base

class Building(Base):
    __tablename__ = "buildings"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, index=True)
    latitude = Column(Float)
    longitude = Column(Float)

    organizations = relationship("Organization", back_populates="building")

class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    parent_id = Column(Integer, ForeignKey("activities.id"), nullable=True)

    children = relationship("Activity", remote_side=[id])
    organizations = relationship("Organization", secondary="organization_activity")

class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    phone_numbers = Column(String)
    building_id = Column(Integer, ForeignKey("buildings.id"))

    building = relationship("Building", back_populates="organizations")
    activities = relationship("Activity", secondary="organization_activity")

class OrganizationActivity(Base):
    __tablename__ = "organization_activity"

    organization_id = Column(Integer, ForeignKey("organizations.id"), primary_key=True)
    activity_id = Column(Integer, ForeignKey("activities.id"), primary_key=True)
