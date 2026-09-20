from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import sys
import os

# Allow backend modules to be imported
sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

from services.munsoon_engine import assess_energy_risk
from services.compare_strategies import compare_strategies
from agent.munsoon_agent import run_munsoon_agent


# --------------------------------
# FASTAPI APP
# --------------------------------

app = FastAPI(
    title="MUNSOON",
    description="AI-powered energy resilience for monsoon-prone solar homes",
    version="0.3.0"
)


# --------------------------------
# CORS
# --------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://munsoon.onrender.com"
],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------
# REQUEST MODEL
# --------------------------------

class EnergyRequest(BaseModel):

    solar_generation: list[float]

    household_demand: list[float]

    battery_capacity_kwh: float = 5.0

    battery_soc: float = 50.0

    grid_available: bool = False


# --------------------------------
# BASIC ROUTES
# --------------------------------

@app.get("/")
def root():

    return {
        "project": "MUNSOON",
        "status": "running"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


# --------------------------------
# MAIN MUNSOON ANALYSIS
# --------------------------------

@app.post("/api/munsoon/analyze")
def analyze_energy(request: EnergyRequest):

    # Energy engine
    analysis = assess_energy_risk(
        solar_generation=request.solar_generation,
        household_demand=request.household_demand,
        battery_capacity_kwh=request.battery_capacity_kwh,
        battery_soc=request.battery_soc,
        grid_available=request.grid_available
    )

    # Agent + RAG
    agent_result = run_munsoon_agent(
        analysis
    )

    return {
        "project": "MUNSOON",
        "analysis": analysis,
        "agent": agent_result
    }


# --------------------------------
# REACTIVE VS MUNSOON
# --------------------------------

@app.get("/api/munsoon/compare")
def compare_energy_strategies():

    result = compare_strategies()

    return {
        "project": "MUNSOON",

        "comparison": {

            "reactive": {

                "shortage_kwh":
                    result["reactive"]["shortage_kwh"],

                "energy_coverage_percent":
                    result["reactive"][
                        "energy_coverage_percent"
                    ]

            },

            "munsoon": {

                "shortage_kwh":
                    result["munsoon"]["shortage_kwh"],

                "energy_coverage_percent":
                    result["munsoon"][
                        "energy_coverage_percent"
                    ]

            },

            "shortage_reduction_kwh":
                result["shortage_reduction_kwh"],

            "coverage_improvement_percentage_points":
                result[
                    "coverage_improvement_percentage_points"
                ]
        },

        "note":
            "Controlled prototype simulation, not field validation."
    }