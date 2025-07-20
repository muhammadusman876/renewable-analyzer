from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

class AnalysisRequest(BaseModel):
    """Request model for solar analysis"""
    location: str = Field(..., description="City or postal code in Germany")
    roof_area: float = Field(..., gt=0, description="Roof area in square meters")
    orientation: str = Field(default="south", description="Roof orientation (north, south, east, west)")
    weather_analysis: str = Field(default="hybrid", description="Weather analysis type: latest (30 days), historical (5+ years), or hybrid (recommended)")
    budget: Optional[float] = Field(None, gt=0, description="Available budget in EUR")

class EnhancedAnalysisRequest(BaseModel):
    """Enhanced request model with weather analysis options"""
    location: Optional[str] = Field(None, description="City name in Germany")
    latitude: Optional[float] = Field(None, description="Latitude coordinate")
    longitude: Optional[float] = Field(None, description="Longitude coordinate")
    roof_area: float = Field(..., gt=0, description="Roof area in square meters")
    orientation: str = Field(default="south", description="Roof orientation")
    weather_analysis: str = Field(default="hybrid", description="Weather analysis type: latest, historical, or hybrid")
    budget: Optional[float] = Field(None, gt=0, description="Available budget in EUR")

class EnhancedSolarPotential(BaseModel):
    """Enhanced solar potential with weather analysis"""
    annual_kwh: float = Field(..., description="Annual energy production in kWh")
    daily_average: float = Field(..., description="Daily average production in kWh")
    monthly_outputs_kwh: Dict[int, float] = Field(..., description="Monthly production breakdown")
    system_capacity_kw: float = Field(..., description="System capacity in kW")
    capacity_factor: float = Field(..., description="Capacity factor percentage")
    peak_month: int = Field(..., description="Peak production month")
    peak_month_production: float = Field(..., description="Peak month production in kWh")
    weather_analysis: Dict[str, Any] = Field(..., description="Weather analysis data")
    calculation_parameters: Dict[str, Any] = Field(..., description="Calculation parameters used")

class SolarPotential(BaseModel):
    """Solar potential calculation results"""
    annual_kwh: float = Field(..., description="Annual energy production in kWh")
    daily_average: float = Field(..., description="Daily average production in kWh")
    peak_month_production: float = Field(..., description="Peak month production in kWh")
    monthly_production: list[float] = Field(..., description="Monthly production breakdown")

class FinancialAnalysis(BaseModel):
    """Financial analysis results"""
    annual_savings: float = Field(..., description="Annual cost savings in EUR")
    payback_period: float = Field(..., description="Payback period in years")
    roi_percentage: float = Field(..., description="Return on investment percentage")
    total_investment: float = Field(..., description="Total investment required in EUR")
    co2_reduction: float = Field(..., description="Annual CO2 reduction in tons")

class EnhancedAnalysisResponse(BaseModel):
    """Enhanced analysis response with weather integration"""
    location: str
    coordinates: Optional[Dict[str, float]]
    solar_potential: EnhancedSolarPotential
    financial_analysis: FinancialAnalysis
    ai_report: str
    recommendations: list[str]

class AnalysisResponse(BaseModel):
    """Complete analysis response"""
    location: str
    solar_potential: SolarPotential
    financial_analysis: FinancialAnalysis
    feasibility_report: str = Field(..., description="AI-generated feasibility report")
    recommendations: list[str] = Field(..., description="Key recommendations")

class WeatherData(BaseModel):
    """Weather data response"""
    location: str
    sunshine_hours: float
    temperature_avg: float
    irradiance: float
