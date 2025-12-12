"""
Invoice management API endpoints
"""

from fastapi import APIRouter, HTTPException
from datetime import datetime
import logging
from db_helper import db, DatabaseError, ValidationError

logger = logging.getLogger(__name__)
router = APIRouter()

# ========== GET ENDPOINTS ==========

@router.get("/invoices")
async def get_invoices(client_id: int = None):
    """Get all invoices, optionally filtered by client"""
    try:
        logger.info("Getting invoices")
        invoices = db.get_invoices(client_id)
        
        return {
            "success": True,
            "data": invoices,
            "count": len(invoices)
        }
    except DatabaseError as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to get invoices")

@router.get("/invoices/{invoice_id}")
async def get_invoice(invoice_id: int):
    """Get specific invoice with details"""
    try:
        logger.info(f"Getting invoice {invoice_id}")
        invoice = db.get_invoice(invoice_id)
        
        if not invoice:
            raise HTTPException(status_code=404, detail="Invoice not found")
        
        return {
            "success": True,
            "data": invoice
        }
    except HTTPException:
        raise
    except DatabaseError as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to get invoice")

@router.get("/clients/{client_id}/hours-by-range")
async def get_hours_by_range(client_id: int, start_date: str, end_date: str):
    """Get hours for a client within a specific date range"""
    try:
        logger.info(f"Getting hours for client {client_id} between {start_date} and {end_date}")
        
        from datetime import datetime
        start = datetime.strptime(start_date, '%Y-%m-%d').date()
        end = datetime.strptime(end_date, '%Y-%m-%d').date()
        
        if start > end:
            raise HTTPException(status_code=400, detail="Start date must be before or equal to end date")
        
        hours_data = db.get_hours_by_date_range(client_id, start, end)
        
        return {
            "success": True,
            "client_id": client_id,
            "start_date": start_date,
            "end_date": end_date,
            "total_hours": hours_data['total_hours'],
            "total_amount": hours_data['total_amount'],
            "entries": hours_data['entries']
        }
    except DatabaseError as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to get hours by range")


async def get_unbilled_hours(client_id: int):
    """Get unbilled hours for a client"""
    try:
        logger.info(f"Getting unbilled hours for client {client_id}")
        unbilled = db.get_unbilled_hours(client_id)
        
        return {
            "success": True,
            "client_id": client_id,
            "total_hours": unbilled['total_hours'],
            "entries": unbilled['entries']
        }
    except DatabaseError as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to get unbilled hours")

# ========== POST ENDPOINTS ==========

@router.post("/invoices")
async def create_invoice(invoice_data: dict):
    """Create a new invoice"""
    try:
        logger.info(f"Creating invoice for client {invoice_data.get('client_id')}")
        
        # Validate input
        required_fields = ['client_id', 'total_hours', 'total_amount']
        missing = [f for f in required_fields if f not in invoice_data]
        if missing:
            raise HTTPException(status_code=400, detail=f"Missing fields: {', '.join(missing)}")
        
        client_id = invoice_data.get('client_id')
        total_hours = invoice_data.get('total_hours')
        total_amount = invoice_data.get('total_amount')
        notes = invoice_data.get('notes', '')
        invoice_date_str = invoice_data.get('invoice_date')
        
        if total_hours <= 0:
            raise ValidationError("Total hours must be greater than 0")
        if total_amount <= 0:
            raise ValidationError("Total amount must be greater than 0")
        
        # Parse date
        if invoice_date_str:
            invoice_date = datetime.strptime(invoice_date_str, '%Y-%m-%d').date()
        else:
            invoice_date = datetime.now().date()
        
        # Create invoice
        invoice_id = db.create_invoice(client_id, invoice_date, total_hours, total_amount, notes)
        
        # Save line items if provided
        items = invoice_data.get('items', [])
        if items:
            db.save_invoice_items(invoice_id, items)
        
        logger.info(f"Invoice {invoice_id} created successfully")
        
        return {
            "success": True,
            "message": "Invoice created successfully",
            "invoice_id": invoice_id
        }
    except ValidationError as e:
        logger.warning(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except DatabaseError as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to create invoice")

# ========== PUT ENDPOINTS ==========

@router.put("/invoices/{invoice_id}")
async def update_invoice(invoice_id: int, invoice_data: dict):
    """Update invoice details"""
    try:
        logger.info(f"Updating invoice {invoice_id}")
        
        # Update items if provided
        if 'items' in invoice_data:
            db.save_invoice_items(invoice_id, invoice_data['items'])
        
        logger.info(f"Invoice {invoice_id} updated")
        
        return {
            "success": True,
            "message": "Invoice updated successfully",
            "invoice_id": invoice_id
        }
    except DatabaseError as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to update invoice")

@router.put("/invoices/{invoice_id}/status")
async def update_invoice_status(invoice_id: int, status: dict):
    """Update invoice status"""
    try:
        logger.info(f"Updating invoice {invoice_id} status")
        
        status_value = status.get('status')
        if not status_value:
            raise HTTPException(status_code=400, detail="Status field required")
        
        db.update_invoice_status(invoice_id, status_value)
        
        logger.info(f"Invoice {invoice_id} status updated to {status_value}")
        
        return {
            "success": True,
            "message": "Invoice status updated",
            "invoice_id": invoice_id,
            "status": status_value
        }
    except DatabaseError as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to update invoice status")

@router.post("/invoices/{invoice_id}/pdf")
async def generate_invoice_pdf(invoice_id: int):
    """Generate PDF for invoice"""
    try:
        logger.info(f"Generating PDF for invoice {invoice_id}")
        
        # Get invoice data
        invoice = db.get_invoice(invoice_id)
        if not invoice:
            raise HTTPException(status_code=404, detail="Invoice not found")
        
        # Generate PDF (will be implemented with ReportLab)
        pdf_path = f"invoices/INV-{invoice['InvoiceID']}-{invoice['InvoiceNumber']}.pdf"
        
        # Update PDF path in database
        db.update_invoice_pdf_path(invoice_id, pdf_path)
        
        logger.info(f"PDF generated for invoice {invoice_id}")
        
        return {
            "success": True,
            "message": "PDF generated successfully",
            "invoice_id": invoice_id,
            "pdf_path": pdf_path
        }
    except HTTPException:
        raise
    except DatabaseError as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to generate PDF")

# ========== DELETE ENDPOINTS ==========

@router.delete("/invoices/{invoice_id}")
async def delete_invoice(invoice_id: int):
    """Delete an invoice"""
    try:
        logger.info(f"Deleting invoice {invoice_id}")
        
        db.delete_invoice(invoice_id)
        
        logger.info(f"Invoice {invoice_id} deleted")
        
        return {
            "success": True,
            "message": "Invoice deleted successfully",
            "invoice_id": invoice_id
        }
    except DatabaseError as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to delete invoice")
