"""
Timesheet API endpoints
"""

from fastapi import APIRouter, HTTPException, Query
import logging
from datetime import datetime
from db_helper import db, DatabaseError, ValidationError
from app.models import TimeEntry

logger = logging.getLogger(__name__)
router = APIRouter()

# ========== GET ENDPOINTS ==========

@router.get("/timesheet")
async def get_timesheet(week_start: str = Query(..., description="Week start date (YYYY-MM-DD)")):
    """Get weekly timesheet for specified week"""
    try:
        logger.info(f"Getting timesheet for week {week_start}")
        
        # Parse date
        try:
            week_start_date = datetime.strptime(week_start, "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
        
        # Get timesheet
        timesheet = db.get_weekly_timesheet(week_start_date)
        
        logger.info(f"Retrieved timesheet for {len(timesheet)} clients")
        
        return {
            "success": True,
            "week_start": str(week_start_date),
            "data": timesheet,
            "client_count": len(timesheet)
        }
    except DatabaseError as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to get timesheet")

@router.get("/timesheet/current")
async def get_current_week_timesheet():
    """Get current week's timesheet"""
    try:
        logger.info("Getting current week timesheet")
        
        week_start = db.get_week_start()
        timesheet = db.get_weekly_timesheet(week_start)
        
        logger.info(f"Retrieved timesheet for {len(timesheet)} clients")
        
        return {
            "success": True,
            "week_start": str(week_start),
            "data": timesheet,
            "client_count": len(timesheet)
        }
    except DatabaseError as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to get timesheet")

# ========== POST ENDPOINTS ==========

@router.post("/timesheet")
async def save_time_entry(entry: TimeEntry):
    """Save or update a time entry"""
    try:
        logger.info(f"Saving time entry for client {entry.client_id}, day {entry.day_of_week}")
        
        # Validate input
        if entry.day_of_week < 1 or entry.day_of_week > 7:
            raise ValidationError("Day of week must be 1-7")
        if entry.hours_worked < 0:
            raise ValidationError("Hours cannot be negative")
        if entry.hours_worked > 24:
            raise ValidationError("Hours cannot exceed 24 per day")
        if entry.rate_used < 0:
            raise ValidationError("Rate cannot be negative")
        
        # Save entry
        entry_id = db.save_time_entry(
            client_id=entry.client_id,
            week_start_date=entry.week_start_date,
            day_of_week=entry.day_of_week,
            hours_worked=entry.hours_worked,
            rate_used=entry.rate_used,
            notes=entry.notes or ""
        )
        
        logger.info(f"Time entry saved with ID: {entry_id}")
        
        return {
            "success": True,
            "message": "Time entry saved successfully",
            "entry_id": entry_id
        }
    except ValidationError as e:
        logger.warning(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except DatabaseError as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to save time entry")

@router.post("/timesheet/save-all")
async def save_all_entries(entries: list[TimeEntry]):
    """Save multiple time entries at once"""
    try:
        logger.info(f"Saving {len(entries)} time entries")
        
        saved_count = 0
        errors = []
        
        for entry in entries:
            try:
                # Validate
                if entry.hours_worked < 0 or entry.hours_worked > 24:
                    continue
                
                # Save
                db.save_time_entry(
                    client_id=entry.client_id,
                    week_start_date=entry.week_start_date,
                    day_of_week=entry.day_of_week,
                    hours_worked=entry.hours_worked,
                    rate_used=entry.rate_used,
                    notes=entry.notes or ""
                )
                saved_count += 1
            except Exception as e:
                errors.append(f"Entry {entry.client_id}-{entry.day_of_week}: {str(e)}")
                logger.warning(f"Failed to save entry: {e}")
        
        logger.info(f"Saved {saved_count} time entries")
        
        return {
            "success": True,
            "saved_count": saved_count,
            "errors": errors,
            "message": f"Saved {saved_count} time entries"
        }
    except DatabaseError as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to save time entries")

# ========== DELETE ENDPOINTS ==========

@router.delete("/timesheet/{entry_id}")
async def delete_time_entry(entry_id: int):
    """Delete a time entry"""
    try:
        logger.info(f"Deleting time entry {entry_id}")
        
        success = db.delete_time_entry(entry_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="Time entry not found")
        
        logger.info(f"Time entry {entry_id} deleted")
        
        return {
            "success": True,
            "message": "Time entry deleted successfully"
        }
    except DatabaseError as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to delete time entry")
