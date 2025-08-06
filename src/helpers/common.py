from uuid import UUID
from datetime import datetime
from decimal import Decimal

def custom_serializer(obj):
    """Custom serializer
    """
    if isinstance(obj, UUID):
        # Convert UUID to string format
        return str(obj)
    if isinstance(obj, datetime):
        # Convert datetime to ISO 8601 string format
        return obj.isoformat()
    if isinstance(obj, Decimal):
        # Convert Decimal to float
        return float(obj)
    raise TypeError(f"Type {type(obj)} not serializable")
