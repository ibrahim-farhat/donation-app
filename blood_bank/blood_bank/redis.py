from django.conf import settings

from stock.models import BloodUnit

import redis

# connect to redis
r = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB
)


# Initialize the redis values every time the sever goes down
for type in BloodUnit.BloodType:
    units = BloodUnit.objects.filter(type=type, availability=True).count()
    r.set(f'blood_type:{type}', units)
