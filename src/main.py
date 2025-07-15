from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from uvicorn import run
from pydantic import BaseModel
from impact_analizer import BusinessObjective, ImpactAnalyzer
from langfuse import observe
from dotenv import load_dotenv
import os

# Cargar variables de entorno desde .env
load_dotenv()

class ImpactAnalysisRequest(BaseModel):
    initial_investment: float
    business_objective: BusinessObjective
    expected_impact: float
    initiative_name: str

def get_app():
    
    app = FastAPI(title="Product Impact Analyzer", description="Analiza el impacto de iniciativas de negocio")

    # Mount static files
    app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")), name="static")

    @app.get("/health")
    async def health():
        return {"message": "Hello World"}
    
    @app.get("/")
    async def index():
        return FileResponse(os.path.join(os.path.dirname(__file__), "templates", "index.html"))
    
    @app.post("/impact-analysis")
    @observe(name="impact_analysis_endpoint")
    async def impact_analysis(request: ImpactAnalysisRequest):
        analyzer = ImpactAnalyzer()
        return analyzer.analyze_initiative_impact(
            request.initial_investment,
            request.business_objective,
            request.expected_impact,
            request.initiative_name
        )
    
    return app

if __name__ == "__main__":
    run(get_app(), host="0.0.0.0", port=8000) 