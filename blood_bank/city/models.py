from django.db import models
from geopy.distance import great_circle

class City(models.Model):
    name = models.CharField(max_length=100, null=True)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    
    def __str__(self):
        return self.name

    def distance_to(self, other_city):
        if not isinstance(other_city, City):
            raise ValueError("other_city must be an instance of City")
        
        coord1 = (self.latitude, self.longitude)
        coord2 = (other_city.latitude, other_city.longitude)

        return great_circle(coord1, coord2).kilometers
    
