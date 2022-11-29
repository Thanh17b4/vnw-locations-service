from starlette import status
from model.check_data import is_blank
from config import mydb
from locations.schemas import Location, LocationResult, LocationListResult
from slugify import slugify
from fastapi import APIRouter, Response

location_router = APIRouter()


@location_router.post('/locations/create/', status_code=201)
def create_location(request: Location, response: Response):
    location = request.location_to_dict()
    # Validate data
    is_ok, msg = __validate(location)
    if is_ok is False:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return msg
    slug = slugify(location["name"])
    with mydb:
        my_cursor = mydb.cursor()
        sql = "INSERT INTO locations (name, slug) VALUES (%s, %s)"
        val = (location["name"], slug)
        my_cursor.execute(sql, val)
        mydb.commit()
        response.status_code = status.HTTP_201_CREATED
        return f"{my_cursor.rowcount} location has been inserted successfully"


def __validate(req: dict):
    if req.get("name") is None or is_blank(req.get("name")) is True:
        return False, "name cannot be null"
    return req, ""


@location_router.get('/locations/detail/{id}', status_code=200)
def detail_location(id: int, response: Response):
    with mydb:
        my_cursor = mydb.cursor()
        my_cursor.execute("SELECT * FROM locations WHERE id = %d" % id)
        location = my_cursor.fetchone()
        if location is None:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return False, f"location_id is not correct"
        return True, LocationResult(location)


@location_router.get('/locations/all/', status_code=200)
def all_location(page: int, limit: int, response: Response):
    with mydb:
        my_cursor = mydb.cursor()
        my_cursor.execute("SELECT COUNT(*) FROM locations")
        total_locations = my_cursor.fetchone()[0]
        d = total_locations % limit
        if d == 0:
            total_page = total_locations // limit
        else:
            total_page = total_locations // limit + 1
        offset = (page - 1) * limit
        if page > total_page or page <= 0:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return f"page is not exist, total page is {total_page}"
        my_cursor.execute("SELECT * FROM locations LIMIT %s OFFSET %s", (limit, offset))
        location = my_cursor.fetchall()
        if location is None:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return f"query was wrong"
        return LocationListResult(location)


@location_router.put('/locations/update/{id}', status_code=200)
async def update_location(id: int, req: Location, response: Response):
    location = req.location_to_dict()
    boolean, result = detail_location(id, response)
    if boolean is False:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return result
    # check have some changes or not
    ok, msg = __check_exist(result, location)
    if ok is False:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return msg
    slug = slugify(location["name"])
    with mydb:
        my_cursor = mydb.cursor()
        sql = "UPDATE locations SET name = %s, slug = %s   WHERE id = %s"
        val = (location["name"], slug, id)
        my_cursor.execute(sql, val)
        return f"{my_cursor.rowcount} row affected"


def __check_exist(req: dict, new_req: dict):
    if req["name"] == new_req["name"]:
        return False, "no information have been changed"
    return new_req, ""


@location_router.delete('/locations/delete/{id}', status_code=200)
async def update_job(id: int, response: Response):
    boolean, result = detail_location(id, response)
    if boolean is False:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return result
    with mydb:
        my_cursor = mydb.cursor()
        my_cursor.execute("DELETE FROM locations WHERE id = %d" % id)
        return f"{my_cursor.rowcount} row affected"
