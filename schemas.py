from datetime import datetime, date
from pydantic import BaseModel


class Location(BaseModel):
    name: str
    slug: str or None = None
    created_at: datetime or None = None
    updated_at: datetime or None = None

    def location_to_dict(self):
        return vars(self)


def LocationResult(job_location) -> dict:
    return {
        "id": job_location[0],
        "name": job_location[1],
        "slug": job_location[2]

    }


def LocationListResult(job_locations) -> list:
    return [LocationResult(job_location) for job_location in job_locations]


