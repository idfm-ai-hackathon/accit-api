# Run with the following command:
# uvicorn app.fastapi:app --reload

from fastapi import FastAPI

from .api.routes import api_router

# Create FastAPI app instance
app = FastAPI(
    title="IDFM Transport API",
    description="""
    A simple API to get transportation information in Paris.

    ## Features
    * Get list of stations
    * Get information about transport lines
    * Search stations by name
    """,
    version="1.0.0",
)

app.include_router(api_router)
