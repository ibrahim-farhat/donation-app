from .models import Donation

def get_donation_by_id(id: int) -> Donation | None:
    return Donation.objects.get(id=id)