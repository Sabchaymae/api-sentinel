
from fastapi import FastAPI, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from database import SessionLocal
from models import MonitoringCheck, Incident
from monitor import check_api
from incident import detect_incident
from security import validate_public_url

app = FastAPI(
    title="API Sentinel",
    description="API Monitoring and Incident Detection Platform",
    version="1.0.0",
)


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "message": "API Sentinel is running",
    }


@app.get("/monitor/check")
def monitor_api(
    url: str = Query(
        ...,
        description="Public HTTP or HTTPS URL to monitor",
    ),
):
    try:
        validate_public_url(url)
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    result = check_api(url)
    incident_data = detect_incident(result)

    # Conserve ici le reste de ton code actuel.

    try:
        with SessionLocal() as db:
            history_entry = MonitoringCheck(**result)
            db.add(history_entry)
            db.flush()
            db.refresh(history_entry)

            if incident_data is not None:
                incident_entry = Incident(**incident_data)
                db.add(incident_entry)

            db.commit()

            return {
                "id": history_entry.id,
                "url": history_entry.url,
                "status_code": history_entry.status_code,
                "response_time_ms": history_entry.response_time_ms,
                "is_available": history_entry.is_available,
                "error": history_entry.error,
                "checked_at": history_entry.checked_at.isoformat(),
            }

    except SQLAlchemyError as exc:
        raise HTTPException(
            status_code=500,
            detail="Failed to save monitoring result to database",
        ) from exc


@app.get("/monitor/history")
def get_monitoring_history():
    try:
        with SessionLocal() as db:
            history = db.scalars(
                select(MonitoringCheck).order_by(
                    MonitoringCheck.id.desc()
                )
            ).all()

            return {
                "total_checks": len(history),
                "history": [
                    {
                        "id": item.id,
                        "url": item.url,
                        "status_code": item.status_code,
                        "response_time_ms": item.response_time_ms,
                        "is_available": item.is_available,
                        "error": item.error,
                        "checked_at": item.checked_at.isoformat(),
                    }
                    for item in history
                ],
            }

    except SQLAlchemyError as exc:
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve monitoring history",
        ) from exc


@app.get("/incidents")
def get_incidents():
    try:
        with SessionLocal() as db:
            incidents = db.scalars(
                select(Incident).order_by(
                    Incident.id.desc()
                )
            ).all()

            return {
                "total_incidents": len(incidents),
                "incidents": [
                    {
                        "id": item.id,
                        "url": item.url,
                        "status_code": item.status_code,
                        "error": item.error,
                        "incident_type": item.incident_type,
                        "detected_at": item.detected_at.isoformat(),
                    }
                    for item in incidents
                ],
            }

    except SQLAlchemyError as exc:
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve incidents",
        ) from exc
