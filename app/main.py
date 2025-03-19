from fastapi import FastAPI, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from typing import List, Annotated
from db import SessionLocal, engine
import models
from models import Organization, Activity, Building

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/organizations", response_model=List[dict])
def list_organizations(db: Session = Depends(get_db)):
    return db.query(Organization).all()


@app.get("/organizations/{org_id}", response_model=dict)
def get_organization(org_id: Annotated[int, Path()], db: Session = Depends(get_db)):
    org = db.query(Organization).filter(Organization.id == org_id).first()
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return org


@app.get("/organizations/by_radius", response_model=List[dict])
def get_organizations_by_radius(lat: float, lon: float, radius: float, db: Session = Depends(get_db)):
    pass


@app.get("/organizations/by_activity", response_model=List[dict])
def get_organizations_by_activity(activity_id: int, db: Session = Depends(get_db)):
    def get_sub_activities(activity):
        subs = activity.children
        for sub in activity.children:
            subs.extend(get_sub_activities(sub))
        return subs

    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    activities = [activity] + get_sub_activities(activity)
    return db.query(Organization).filter(Organization.activities.any(Activity.id.in_([a.id for a in activities]))).all()