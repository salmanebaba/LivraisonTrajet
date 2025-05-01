from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import requests

app = FastAPI()

# CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Truck starting point (garage)
HOME = (33.979448, -6.866329)  # latitude, longitude

class LocationRequest(BaseModel):
    locations: List[List[float]]  # [[lat, lon], ...]

@app.get("/get-home")
def get_home():
    return {"home": HOME}

@app.post("/optimized-route")
def optimized_route(req: LocationRequest):
    locs = req.locations
    if not locs:
        return {"error": "No coordinates provided"}

    # Include HOME as the starting point
    all_coords = [HOME] + locs
    coords_str = ";".join(f"{lon},{lat}" for lat, lon in all_coords)

    url = (
        f"http://osrm:5000/trip/v1/driving/{coords_str}"
        f"?source=first&roundtrip=true&overview=full&geometries=geojson"
    )

    try:
        res = requests.get(url)
        data = res.json()

        if data["code"] == "Ok":
            # Sort waypoints by OSRM's optimized order
            optimized_order = sorted(data["waypoints"], key=lambda wp: wp["waypoint_index"])
            ordered = [wp["location"] for wp in optimized_order]

            return {
                "ordered": ordered,
                "geometry": data["trips"][0]["geometry"]
            }

        print("OSRM response error:", data)
        return {"error": data.get("message", "Unknown OSRM error")}
    except Exception as e:
        print("Exception:", str(e))
        return {"error": str(e)}
