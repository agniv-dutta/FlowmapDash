from pydantic import BaseModel, validator, Field
from typing import Optional, Dict, Any
from datetime import datetime


class EventCreate(BaseModel):
    session_id: str = Field(..., description="Session identifier")
    event_type: str = Field(..., description="Type of event (page_view or click)")
    page_url: str = Field(..., description="URL of the page where event occurred")
    timestamp: str = Field(..., description="ISO format timestamp")
    coordinates: Optional[Dict[str, Any]] = Field(None, description="Click coordinates (x, y)")
    
    @validator('event_type')
    def validate_event_type(cls, v):
        valid_types = ['page_view', 'click', 'scroll', 'form_submit']
        if v not in valid_types:
            raise ValueError(f'event_type must be one of: {", ".join(valid_types)}')
        return v
    
    @validator('page_url')
    def validate_url(cls, v):
        if not v.startswith(('http://', 'https://')):
            raise ValueError('page_url must be a valid URL starting with http:// or https://')
        return v
    
    @validator('timestamp')
    def validate_timestamp(cls, v):
        try:
            datetime.fromisoformat(v.replace('Z', '+00:00'))
        except ValueError:
            raise ValueError('timestamp must be a valid ISO format datetime string')
        return v


class SessionCreate(BaseModel):
    user_id: str = Field(..., description="User identifier")
    start_time: str = Field(..., description="ISO format start time")
    device: Optional[str] = Field(None, description="Device type (desktop, mobile, tablet)")
    browser: Optional[str] = Field(None, description="Browser name")
    os: Optional[str] = Field(None, description="Operating system")
    
    @validator('start_time')
    def validate_start_time(cls, v):
        try:
            datetime.fromisoformat(v.replace('Z', '+00:00'))
        except ValueError:
            raise ValueError('start_time must be a valid ISO format datetime string')
        return v
    
    @validator('device')
    def validate_device(cls, v):
        if v is not None:
            valid_devices = ['desktop', 'mobile', 'tablet']
            if v.lower() not in valid_devices:
                raise ValueError(f'device must be one of: {", ".join(valid_devices)}')
        return v


class HeatmapQuery(BaseModel):
    page_url: str = Field(..., description="URL to generate heatmap for")
    start_date: Optional[str] = Field(None, description="Start date for heatmap data")
    end_date: Optional[str] = Field(None, description="End date for heatmap data")
    
    @validator('page_url')
    def validate_url(cls, v):
        if not v.startswith(('http://', 'https://')):
            raise ValueError('page_url must be a valid URL starting with http:// or https://')
        return v
