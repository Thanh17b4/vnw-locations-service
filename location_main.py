import uvicorn
from fastapi import FastAPI
from locations.location import location_router
app = FastAPI()
app.include_router(location_router)
uvicorn.run(app, host="localhost", port=5001)
