from fastapi import APIRouter, HTTPException
from app.api.models import AnalysisRequest, AnalysisResponse, WeatherData, EnhancedAnalysisRequest, EnhancedAnalysisResponse, EnhancedSolarPotential
from app.core.solar_calculator import SolarCalculator
from app.core.weather_dwd import DWDWeatherFetcher
from app.core.geo_utils import geocode_location
from app.core.roi_calculator import ROICalculator
from app.rag.llm_service import EnergyRAGSystem
import os
from app.core.electricity_price import get_electricity_price, update_electricity_price, fetch_live_electricity_price
import threading
import time

router = APIRouter()

# Initialize services
EDA_DATASET_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "processed_eda_data", "renewable_weather.csv")

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_solar_potential(request: AnalysisRequest, data_source: str = "eda"):
    """
    Main analysis endpoint that combines solar potential, financial analysis, and AI reporting
    Now supports weather analysis type selection: latest, historical, or hybrid
    """
    try:
        # Get coordinates for location if needed
        coords = geocode_location(request.location)
        if not coords:
            raise HTTPException(status_code=400, detail="Could not geocode location.")

        # 1. Calculate solar potential with weather analysis integration
        if data_source == "dwd":
            # Use DWD direct integration (legacy path)
            dwd = DWDWeatherFetcher()
            irradiance = dwd.get_latest_irradiance(*coords)
            if not irradiance:
                raise HTTPException(status_code=400, detail="No DWD irradiance data available for this location.")
            # Use same constants as SolarCalculator
            panel_eff = 0.20
            system_losses = 0.85
            orientation_factors = {
                "south": 1.0, "southeast": 0.95, "southwest": 0.95,
                "east": 0.85, "west": 0.85, "northeast": 0.75, "northwest": 0.75, "north": 0.6
            }
            orientation_factor = orientation_factors.get(request.orientation.lower(), 0.85)
            daily_kwh = irradiance * request.roof_area * panel_eff * system_losses * orientation_factor
            annual_kwh = daily_kwh * 365
            # Use SolarCalculator for monthly breakdown
            solar_calc = SolarCalculator()  # Uses complete dataset by default
            monthly_production = solar_calc.calculate_monthly_production(annual_kwh)
            peak_month_kwh = max(monthly_production)
            solar_output = {
                "annual_kwh": round(annual_kwh, 1),
                "daily_average": round(daily_kwh, 1),
                "peak_month_production": round(peak_month_kwh, 1),
                "monthly_production": [round(x, 1) for x in monthly_production],
                "system_capacity_kw": round(request.roof_area * 0.2, 1),
                "capacity_factor": round((annual_kwh / (request.roof_area * 0.2 * 8760)) * 100, 1)
            }
        else:
            # Use enhanced calculation with weather analysis integration
            solar_calc = SolarCalculator()
            enhanced_result = solar_calc.calculate_annual_output_enhanced(
                location=request.location,
                latitude=coords[0],
                longitude=coords[1],
                roof_area=request.roof_area,
                orientation=request.orientation,
                weather_analysis=request.weather_analysis
            )

            # Convert to legacy format for compatibility
            solar_output = {
                "annual_kwh": enhanced_result["annual_output_kwh"],
                "daily_average": enhanced_result["daily_average_kwh"], 
                "peak_month_production": enhanced_result["peak_month_production"],
                "monthly_production": list(enhanced_result["monthly_outputs_kwh"].values()),
                "system_capacity_kw": enhanced_result["system_capacity_kw"],
                "capacity_factor": enhanced_result["capacity_factor"],
                "weather_analysis_type": request.weather_analysis,
                "weather_data": enhanced_result["weather_analysis"]
            }
        
        # 2. Calculate ROI and financial metrics
        roi_calc = ROICalculator()
        financial_analysis_dict = roi_calc.calculate_roi(
            solar_output, 
            request.budget, 
            request.location
        )
        
        # Update solar output with scaled values if system was scaled due to budget
        scaling_info = financial_analysis_dict.get("scaling_info", {})
        if scaling_info.get("system_scaled", False):
            scaling_factor = scaling_info.get("scaling_factor", 1.0)
            # Update solar output to reflect the actually affordable system
            solar_output["annual_kwh"] = scaling_info.get("scaled_annual_kwh", solar_output["annual_kwh"])
            solar_output["system_capacity_kw"] = scaling_info.get("scaled_capacity_kw", solar_output["system_capacity_kw"])
            solar_output["daily_average"] = round(solar_output["annual_kwh"] / 365, 2)
            # Scale monthly production proportionally
            solar_output["monthly_production"] = [round(month * scaling_factor, 2) for month in solar_output["monthly_production"]]
            solar_output["peak_month_production"] = max(solar_output["monthly_production"])
            # Recalculate capacity factor
            solar_output["capacity_factor"] = round((solar_output["annual_kwh"] / (solar_output["system_capacity_kw"] * 8760)) * 100, 1)
        
        # 3. Generate AI-powered feasibility report
        rag_system = EnergyRAGSystem()
        report = await rag_system.generate_feasibility_report(
            request.dict(), 
            {**solar_output, **financial_analysis_dict}
        )
        
        # 4. Generate recommendations
        recommendations = generate_recommendations(solar_output, financial_analysis_dict)
        
        # 5. Create proper model objects
        from app.api.models import SolarPotential, FinancialAnalysis
        
        solar_potential_obj = SolarPotential(
            annual_kwh=solar_output["annual_kwh"],
            daily_average=solar_output["daily_average"],
            peak_month_production=solar_output["peak_month_production"],
            monthly_production=solar_output["monthly_production"]
        )
        
        financial_analysis_obj = FinancialAnalysis(
            annual_savings=financial_analysis_dict["annual_savings"],
            payback_period=financial_analysis_dict["payback_period"],
            roi_percentage=financial_analysis_dict["roi_percentage"],
            total_investment=financial_analysis_dict["total_investment"],
            co2_reduction=financial_analysis_dict["co2_reduction"]
        )

        return AnalysisResponse(
            location=request.location,
            solar_potential=solar_potential_obj,
            financial_analysis=financial_analysis_obj,
            feasibility_report=report,
            recommendations=recommendations
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

# Commenting out original weather endpoint due to WeatherService import issue
# @router.get("/weather/{location}", response_model=WeatherData)
# async def get_weather_data(location: str):
#     """Get historical weather data for a specific location"""
#     try:
#         weather_service = WeatherService()
#         data = weather_service.get_historical_data(location)
#         return data
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Weather data retrieval failed: {str(e)}")

@router.get("/locations")
async def get_supported_locations():
    """Get list of supported German cities/regions"""
    return {
        "locations": [
            "Berlin", "Hamburg", "Munich", "Cologne", "Frankfurt",
            "Stuttgart", "Düsseldorf", "Dortmund", "Leipzig", "Bremen"
        ]
    }

@router.get("/weather-analysis-options")
async def get_weather_analysis_options():
    """Get available weather analysis options for frontend"""
    from app.core.weather_service import WeatherAnalysisService
    weather_service = WeatherAnalysisService()
    return weather_service.get_analysis_options()

# Endpoint to get current electricity price
@router.get("/electricity-price")
def get_price():
    return {"electricity_price_eur_per_kwh": get_electricity_price()}

# Endpoint to update price from live API
@router.post("/electricity-price/update-live")
def update_price_live():
    price = fetch_live_electricity_price()
    if price is not None:
        update_electricity_price(price)
        return {"success": True, "new_price": price}
    else:
        raise HTTPException(status_code=503, detail="Failed to fetch live price.")

# Endpoint to update price manually
@router.post("/electricity-price/update-manual")
def update_price_manual(price: float):
    update_electricity_price(price)
    return {"success": True, "new_price": price}

# Optional: background thread to update price every 24h
def periodic_price_update(interval_hours=24):
    def updater():
        while True:
            price = fetch_live_electricity_price()
            if price is not None:
                update_electricity_price(price)
            time.sleep(interval_hours * 3600)
    
    thread = threading.Thread(target=updater, daemon=True)
    thread.start()

# Start background updater on server start (optional)
periodic_price_update()

def generate_recommendations(solar_output: dict, financial_analysis: dict) -> list[str]:
    """Generate actionable recommendations based on analysis results"""
    recommendations = []
    
    # ROI-based recommendations
    if financial_analysis["payback_period"] < 10:
        recommendations.append("SUCCESS: Excellent investment opportunity with payback period under 10 years")
    elif financial_analysis["payback_period"] < 15:
        recommendations.append("Good investment opportunity with reasonable payback period")
    else:
        recommendations.append("WARNING: Consider waiting for better incentives or technology improvements")
    
    # Production-based recommendations
    if solar_output["annual_kwh"] > 1000:
        recommendations.append("High solar potential - consider maximizing roof coverage")
    else:
        recommendations.append("INFO: Consider energy efficiency improvements before solar installation")
    
    # Financial recommendations
    if financial_analysis["annual_savings"] > 1000:
        recommendations.append("Significant annual savings potential - prioritize installation")
    
    # Environmental impact
    if financial_analysis["co2_reduction"] > 2:
        recommendations.append("Substantial environmental impact - great for carbon footprint reduction")
    
    return recommendations


@router.post("/analyze-enhanced", response_model=EnhancedAnalysisResponse)
async def analyze_solar_potential_enhanced(request: EnhancedAnalysisRequest):
    """
    Enhanced analysis endpoint with weather service integration
    Supports coordinate-based analysis and multiple weather analysis types
    """
    try:
        # Initialize solar calculator
        solar_calc = SolarCalculator()  # Uses complete dataset by default
        
        # Perform enhanced calculation with weather integration
        result = solar_calc.calculate_annual_output_enhanced(
            location=request.location,
            latitude=request.latitude,
            longitude=request.longitude,
            roof_area=request.roof_area,
            orientation=request.orientation,
            weather_analysis=request.weather_analysis
        )
        
        # Create enhanced solar potential object
        solar_potential = EnhancedSolarPotential(
            annual_kwh=result["annual_output_kwh"],
            daily_average=result["daily_average_kwh"],
            monthly_outputs_kwh=result["monthly_outputs_kwh"],
            system_capacity_kw=result["system_capacity_kw"],
            capacity_factor=result["capacity_factor"],
            peak_month=result["peak_month"],
            peak_month_production=result["peak_month_production"],
            weather_analysis=result["weather_analysis"],
            calculation_parameters=result["calculation_parameters"]
        )
        
        # Calculate financial analysis
        roi_calc = ROICalculator()
        
        # Create solar output dict in the format expected by ROI calculator
        solar_output_dict = {
            "annual_kwh": result["annual_output_kwh"],
            "system_capacity_kw": result["system_capacity_kw"],
            "monthly_production": list(result["monthly_outputs_kwh"].values())
        }
        
        financial_analysis = roi_calc.calculate_roi(
            solar_output=solar_output_dict,
            budget=request.budget,
            location=request.location or "Germany"
        )
        
        # Generate AI report using RAG system
        try:
            rag_system = EnergyRAGSystem()
            
            # Create context for AI analysis
            context = {
                "location": request.location or f"Coordinates ({request.latitude}, {request.longitude})",
                "weather_analysis": request.weather_analysis,
                "annual_production": result['annual_output_kwh'],
                "system_capacity": result['system_capacity_kw'],
                "capacity_factor": result['capacity_factor'],
                "roi": financial_analysis['roi_percentage'],
                "payback_period": financial_analysis['payback_period']
            }
            
            ai_report = await rag_system.generate_feasibility_report(
                user_input={"location": request.location, "roof_area": request.roof_area},
                calculations={"solar": result, "financial": financial_analysis}
            )
        except Exception as e:
            print(f"AI report generation failed: {e}")
            ai_report = f"Based on the enhanced weather analysis using {request.weather_analysis} data, your solar installation shows promising results with {result['annual_output_kwh']:.0f} kWh annual production and {financial_analysis['payback_period']:.1f} year payback period."
        
        # Generate recommendations
        recommendations = generate_recommendations(solar_potential.dict(), financial_analysis)
        
        # Create FinancialAnalysis object
        from app.api.models import FinancialAnalysis
        financial_analysis_obj = FinancialAnalysis(
            annual_savings=financial_analysis["annual_savings"],
            payback_period=financial_analysis["payback_period"],
            roi_percentage=financial_analysis["roi_percentage"],
            total_investment=financial_analysis["total_investment"],
            co2_reduction=financial_analysis["co2_reduction"]
        )
        
        # Determine location string and coordinates
        location_str = request.location or f"Coordinates ({request.latitude}, {request.longitude})"
        coordinates = None
        if request.latitude and request.longitude:
            coordinates = {"latitude": request.latitude, "longitude": request.longitude}
        
        return EnhancedAnalysisResponse(
            location=location_str,
            coordinates=coordinates,
            solar_potential=solar_potential,
            financial_analysis=financial_analysis_obj,
            ai_report=ai_report,
            recommendations=recommendations
        )
        
    except Exception as e:
        print(f"Enhanced analysis error: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
