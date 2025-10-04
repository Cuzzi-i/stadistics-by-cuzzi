"""
Event Analytics API
===================

A FastAPI-based event tracking and analytics system.

Author: Ramiro Boccuzzi (Cuzzi)
GitHub: @Cuzzi-i
License: MIT
Version: 1.0.1
"""


from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta, timezone
from typing import Optional, List
from fastapi.middleware.cors import CORSMiddleware

import models
import schemas
from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Stadistics Cuzzi API", version="1.0.0")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/events/", response_model=schemas.Event)
def create_event(event: schemas.EventCreate, db: Session = Depends(get_db)):
    """
    Create a new event
    
    - **user_id**: Identifier for the user
    - **event_type**: Type of event (e.g., 'login', 'purchase')
    - **metadata**: Optional JSON data with additional info
    """

    event_dict = event.model_dump(by_alias=False)

    db_event = models.Event(**event_dict)
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


@app.get("/events/", tags=["Events"])
def get_events(
    skip: int = Query(0, description="Number of records to skip"),
    limit: int = Query(100, description="Maximum number of records to return"),
    user_id: Optional[str] = Query(None, description="Filter by user ID"),
    event_type: Optional[str] = Query(None, description="Filter by event type"),
    db: Session = Depends(get_db)
):
    """
    Get a list of events with optional filters

    This uses pagination (skip/limit) to avoid loading too much data at once.
    """
    query = db.query(models.Event)

    if user_id:
        query = query.filter(models.Event.user_id == user_id)
    if event_type:
        query = query.filter(models.Event.event_type == event_type)

    events = query.offset(skip).limit(limit).all()
    return events


## === Estadistics Endpoints === ##

@app.get("/stats/total", tags=["Statistics"])
def get_total_events(db: Session = Depends(get_db)):
    """
    Get the total number of events recorded
    """
    total_events= db.query(func.count(models.Event.id)).scalar()
    unique_users = db.query(func.count(func.distinct(models.Event.user_id))).scalar()
    unique_event_types = db.query(func.count(func.distinct(models.Event.event_type))).scalar()

    return {
        "total_events": total_events,
        "unique_users": unique_users,
        "unique_event_types": unique_event_types
    }

@app.get("/stats/by-event-type", tags=["Statistics"])
def get_stats_by_event_type(db: Session = Depends(get_db)):
    """
    Get the number of events grouped by event type
    """
    results = (db.query(
        models.Event.event_type,
        func.count(models.Event.id).label("count")
    )
    .group_by(models.Event.event_type)
    .order_by(func.count(models.Event.id).desc())
    .all()
    )

    return [{"event_type": event_type, "count": count} for event_type, count in results]

@app.get("/stats/by-user", tags=["Statistics"])
def get_stats_by_user(limit: int = Query(10, description="Top N users to return"),db: Session = Depends(get_db)):
    """
    Get most active users by number of events
    """

    result = (db.query(models.Event.user_id, func.count(models.Event.id).label("count"))
                       .group_by(models.Event.user_id)
                       .order_by(func.count(models.Event.id).desc())
                       .limit(limit)
                       .all()
                       )
    
    return [{"user_id": user_id, "count": count} for user_id, count in result]

@app.get("/stats/over-time", tags=["Statistics"])
def get_stats_over_time(
    days: int = Query(7, description="Number of days to look back"),
    db: Session = Depends(get_db)
):
    """
    Get event counts over time (by day)
    """
    start_date = datetime.now(timezone.utc) - timedelta(days=days)
    
    results = (
        db.query(
            func.date(models.Event.timestamp).label('date'),
            func.count(models.Event.id).label('count')
        )
        .filter(models.Event.timestamp >= start_date)
        .group_by(func.date(models.Event.timestamp))
        .order_by(func.date(models.Event.timestamp))
        .all()
    )
    
    return [
        {"date": str(date), "count": count}
        for date, count in results
    ]

@app.get("/stats/user-activity/{user_id}", tags=["Statistics"])
def get_user_activity(user_id: str, db: Session = Depends(get_db)):
    """
    Get detailed statistics for a specific user
    """
    total = db.query(func.count(models.Event.id))\
        .filter(models.Event.user_id == user_id)\
        .scalar()
    
    by_type = (
        db.query(
            models.Event.event_type,
            func.count(models.Event.id).label('count')
        )
        .filter(models.Event.user_id == user_id)
        .group_by(models.Event.event_type)
        .all()
    )
    
    last_event = (
        db.query(models.Event.timestamp)
        .filter(models.Event.user_id == user_id)
        .order_by(models.Event.timestamp.desc())
        .first()
    )
    
    return {
        "user_id": user_id,
        "total_events": total,
        "events_by_type": [
            {"event_type": et, "count": c} for et, c in by_type
        ],
        "last_event_at": last_event[0] if last_event else None
    }

@app.get("/stats/recent-activity", tags=["Statistics"])
def get_recent_activity(
    minutes: int = Query(60, description="Look back this many minutes"),
    db: Session = Depends(get_db)
):
    """
    Get activity in recent time window
    """
    start_time = datetime.utcnow() - timedelta(minutes=minutes)
    
    results = (
        db.query(
            models.Event.event_type,
            func.count(models.Event.id).label('count')
        )
        .filter(models.Event.timestamp >= start_time)
        .group_by(models.Event.event_type)
        .all()
    )
    
    total = sum(count for _, count in results)
    
    return {
        "time_window_minutes": minutes,
        "total_events": total,
        "by_type": [
            {"event_type": et, "count": c} for et, c in results
        ]
    }

## === Health Check Endpoint === ##

@app.get("/", tags=["Health"])
def root():
    """
    Health check endpoint
    """
    return {{
        "name": "Event Analytics API",
        "version": "1.0.1",
        "author": "Ramiro Boccuzzi (Cuzzi)",
        "github": "https://github.com/Cuzzi-i",
        "documentation": {
            "interactive_docs": "/docs",
            "redoc": "/redoc",
            "openapi_schema": "/openapi.json"
        },
        "endpoints": {
            "create_event": "POST /events/",
            "get_events": "GET /events/",
            "total_stats": "GET /stats/total",
            "events_by_type": "GET /stats/by-event-type",
            "top_users": "GET /stats/by-user",
            "time_series": "GET /stats/over-time",
            "user_activity": "GET /stats/user-activity/{user_id}",
            "recent_activity": "GET /stats/recent-activity"
        }
    }}
