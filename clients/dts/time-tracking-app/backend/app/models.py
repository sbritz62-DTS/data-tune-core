"""
Data models for request/response validation
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import date

# ========== CLIENT MODELS ==========

class ClientCreate(BaseModel):
    """Request model for creating a client"""
    name: str = Field(..., min_length=1, max_length=200)
    rate: float = Field(..., gt=0, le=10000)
    terms: int = Field(default=30, ge=0, le=365)
    contact_name: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    billing_address: Optional[str] = None
    
    @field_validator('rate')
    @classmethod
    def validate_rate(cls, v):
        if v < 0:
            raise ValueError('Rate cannot be negative')
        if v > 10000:
            raise ValueError('Rate too high')
        return v

class ClientUpdate(BaseModel):
    """Request model for updating a client"""
    name: Optional[str] = None
    rate: Optional[float] = None
    terms: Optional[int] = None
    contact_name: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    billing_address: Optional[str] = None

class ClientResponse(BaseModel):
    """Response model for client data"""
    ClientID: int
    ClientName: str
    DefaultRate: float
    PaymentTerms: int
    Active: bool
    ContactName: Optional[str]
    ContactEmail: Optional[str]
    ContactPhone: Optional[str]
    BillingAddress: Optional[str]

# ========== TIMESHEET MODELS ==========

class TimeEntry(BaseModel):
    """Request model for time entry"""
    client_id: int
    week_start_date: date
    day_of_week: int = Field(..., ge=1, le=7)
    hours_worked: float = Field(default=0, ge=0, le=24)
    rate_used: float = Field(gt=0)
    notes: Optional[str] = None
    
    @field_validator('hours_worked')
    @classmethod
    def validate_hours(cls, v):
        if v < 0:
            raise ValueError('Hours cannot be negative')
        if v > 24:
            raise ValueError('Hours cannot exceed 24 per day')
        return v

class TimesheetResponse(BaseModel):
    """Response model for timesheet data"""
    client_id: int
    client_name: str
    default_rate: float
    days: dict

# ========== INVOICE MODELS ==========

class InvoiceCreate(BaseModel):
    """Request model for creating invoice"""
    client_id: int
    week_start_date: Optional[date] = None
    total_hours: float = Field(gt=0)
    total_amount: float = Field(gt=0)
    notes: Optional[str] = None

class InvoiceUpdate(BaseModel):
    """Request model for updating invoice"""
    status: Optional[str] = None
    notes: Optional[str] = None

class InvoiceResponse(BaseModel):
    """Response model for invoice data"""
    InvoiceID: int
    ClientID: int
    ClientName: str
    Status: str
    TotalHours: float
    TotalAmount: float
    CreatedDate: str
    DueDate: Optional[str]

# ========== ERROR MODELS ==========

class ErrorResponse(BaseModel):
    """Error response model"""
    error: str
    detail: Optional[str] = None
