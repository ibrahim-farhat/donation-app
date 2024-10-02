from django.db.models.query import QuerySet

from .models import HospitalRequest

def fetch_pending_requests() -> QuerySet[HospitalRequest]:
    """Fetch pending hospital requests."""
    
    return HospitalRequest.objects.filter(request_status=HospitalRequest.RequestStatus.PENDING)