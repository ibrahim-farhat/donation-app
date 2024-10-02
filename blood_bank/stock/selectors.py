from .models import BloodUnit
from accounts.models import City

def fetch_available_blood_units_by_type(type: BloodUnit.BloodType) -> list[BloodUnit]:
    """Fetch availabe units """
    return list(BloodUnit.objects.filter(availability=True, type=type))

def fetch_available_blood_units_ordered_by_city(type: BloodUnit.BloodType, city: City) -> list[BloodUnit]:
    available_units = fetch_available_blood_units_by_type(type)
    sorted_available_units = sorted(available_units, key=lambda unit: city.distance_to(unit.city))
    return sorted_available_units
