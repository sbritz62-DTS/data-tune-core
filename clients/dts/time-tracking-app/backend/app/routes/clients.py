"""
Client management API endpoints
"""

from fastapi import APIRouter, HTTPException
import logging
from db_helper import db, DatabaseError, ValidationError
from app.models import ClientCreate, ClientUpdate, ClientResponse

logger = logging.getLogger(__name__)
router = APIRouter()

# ========== GET ENDPOINTS ==========

@router.get("/clients")
async def get_all_clients():
    """Get all active clients"""
    try:
        logger.info("Getting all clients")
        clients = db.get_all_clients(active_only=True)
        return {
            "success": True,
            "data": clients,
            "count": len(clients)
        }
    except DatabaseError as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to get clients")

@router.get("/clients/{client_id}")
async def get_client(client_id: int):
    """Get specific client by ID"""
    try:
        logger.info(f"Getting client {client_id}")
        client = db.get_client_by_id(client_id)
        if not client:
            raise HTTPException(status_code=404, detail="Client not found")
        return {
            "success": True,
            "data": client
        }
    except DatabaseError as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to get client")

# ========== POST ENDPOINTS ==========

@router.post("/clients")
async def create_client(client: ClientCreate):
    """Create a new client"""
    try:
        logger.info(f"Creating client: {client.name}")
        
        # Validate input
        if not client.name or len(client.name.strip()) == 0:
            raise ValidationError("Client name is required")
        if client.rate < 0:
            raise ValidationError("Rate cannot be negative")
        if client.rate > 10000:
            raise ValidationError("Rate too high")
        
        # Create client
        client_id = db.add_client(
            client_name=client.name,
            default_rate=client.rate,
            payment_terms=client.terms,
            active=True,
            contact_name=client.contact_name,
            contact_email=client.contact_email,
            contact_phone=client.contact_phone,
            billing_address=client.billing_address
        )
        
        logger.info(f"Client created with ID: {client_id}")
        
        return {
            "success": True,
            "message": "Client created successfully",
            "client_id": client_id
        }
    except ValidationError as e:
        logger.warning(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except DatabaseError as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to create client")

# ========== PUT ENDPOINTS ==========

@router.put("/clients/{client_id}")
async def update_client(client_id: int, client: ClientUpdate):
    """Update an existing client"""
    try:
        logger.info(f"Updating client {client_id}")
        
        # Build update parameters (only non-None values)
        updates = {}
        if client.name is not None:
            if len(client.name.strip()) == 0:
                raise ValidationError("Client name cannot be empty")
            updates['client_name'] = client.name
        if client.rate is not None:
            if client.rate < 0:
                raise ValidationError("Rate cannot be negative")
            updates['default_rate'] = client.rate
        if client.terms is not None:
            updates['payment_terms'] = client.terms
        if client.contact_name is not None:
            updates['contact_name'] = client.contact_name
        if client.contact_email is not None:
            updates['contact_email'] = client.contact_email
        if client.contact_phone is not None:
            updates['contact_phone'] = client.contact_phone
        if client.billing_address is not None:
            updates['billing_address'] = client.billing_address
        
        if not updates:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        # Update client
        success = db.update_client(client_id, **updates)
        
        if not success:
            raise HTTPException(status_code=404, detail="Client not found")
        
        logger.info(f"Client {client_id} updated successfully")
        
        return {
            "success": True,
            "message": "Client updated successfully"
        }
    except ValidationError as e:
        logger.warning(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except DatabaseError as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to update client")

# ========== DELETE ENDPOINTS ==========

@router.delete("/clients/{client_id}")
async def delete_client(client_id: int):
    """Delete (deactivate) a client"""
    try:
        logger.info(f"Deleting client {client_id}")
        
        success = db.delete_client(client_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="Client not found")
        
        logger.info(f"Client {client_id} deleted successfully")
        
        return {
            "success": True,
            "message": "Client deleted successfully"
        }
    except DatabaseError as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to delete client")
