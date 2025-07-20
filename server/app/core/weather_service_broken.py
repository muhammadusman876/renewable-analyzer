"""
Comprehensive Weather Analysis Service
Provides latest, historical, and hybrid weather analysis for solar feasibility
"""
from typing import Optional, Dict, List
from datetime import datetime
from .weather_dwd import DWDWeatherFetcher
import json
import os


class WeatherAnalysisService:
 """
 Comprehensive weather analysis service with multiple data sources and timeframes
 Provides latest, historical, and hybrid weather analysis for solar feasibility
 """
 
 def __init__(self):
 self.dwd_fetcher = DWDWeatherFetcher()
 # Caching disabled - always fetch fresh data
 print("Weather Analysis Service initialized (NO CACHING)")
 
 def get_solar_analysis(self, lat: float, lon: float, analysis_type: str = "hybrid") -> Dict:
 """
 Get comprehensive solar analysis based on specified approach
 
 Args:
 lat, lon: Coordinates
 analysis_type: "latest", "historical", or "hybrid"
 """
 print(f"Running {analysis_type} weather analysis for coordinates ({lat}, {lon})")
 
 if analysis_type == "latest":
 return self._get_latest_analysis(lat, lon)
 elif analysis_type == "historical":
 return self._get_historical_analysis(lat, lon)
 else: # hybrid
 return self._get_hybrid_analysis(lat, lon)
 
 def _get_latest_analysis(self, lat: float, lon: float) -> Dict:
 """Latest data analysis (last 30 days)"""
 print("Analyzing recent weather conditions...")
 
 irradiance = self.dwd_fetcher.get_latest_irradiance(lat, lon)
 temperature = self.dwd_fetcher.get_latest_temperature(lat, lon)
 
 # Determine confidence based on data availability
 confidence = "high" if irradiance and temperature else "medium" if irradiance else "low"
 
 return {
 "analysis_type": "latest",
 "timeframe": "Last 30 days",
 "daily_irradiance_kwh_m2": irradiance or self._get_fallback_irradiance(lat, lon),
 "avg_temperature_c": temperature or self._get_fallback_temperature(lat, lon),
 "data_source": "DWD Recent Data",
 "confidence": confidence,
 "seasonal_factor": self._calculate_seasonal_factor(lat, lon),
 "data_quality": {
 "irradiance_available": irradiance is not None,
 "temperature_available": temperature is not None,
 "days_of_data": 30
 }
 }
 
 def _get_historical_analysis(self, lat: float, lon: float) -> Dict:
 """Historical data analysis (multi-year average) - NO CACHING"""
 print("Analyzing long-term historical patterns...")
 
 # ALWAYS fetch fresh data - no caching
 print(" Fetching fresh historical data (no cache)")
 historical_irradiance = self.dwd_fetcher.get_historical_irradiance(lat, lon, years=5)
 historical_temperature = self.dwd_fetcher.get_historical_temperature(lat, lon, years=5)
 
 if historical_irradiance:
 irradiance = historical_irradiance["overall_average"]
 seasonal_variations = historical_irradiance["monthly_averages"]
 years_of_data = historical_irradiance["years_covered"]
 confidence = "very_high"
 else:
 irradiance = self._get_fallback_irradiance(lat, lon)
 seasonal_variations = self._get_default_seasonal_pattern(lat, lon)
 years_of_data = 0
 confidence = "medium"
 
 temperature = (historical_temperature["overall_average"] 
 if historical_temperature 
 else self._get_fallback_temperature(lat, lon))
 
 return {
 "analysis_type": "historical",
 "timeframe": f"Multi-year average ({years_of_data} years)",
 "daily_irradiance_kwh_m2": irradiance,
 "avg_temperature_c": temperature,
 "seasonal_variations": seasonal_variations,
 "data_source": "DWD Historical Database",
 "confidence": confidence,
 "years_of_data": years_of_data,
 "data_quality": {
 "irradiance_available": historical_irradiance is not None,
 "temperature_available": historical_temperature is not None,
 "data_points": historical_irradiance["data_points"] if historical_irradiance else 0
 }
 }
 
 def _get_hybrid_analysis(self, lat: float, lon: float) -> Dict:
 """Hybrid analysis combining recent and historical data"""
 print("Running hybrid analysis (recent + historical)...")
 
 latest = self._get_latest_analysis(lat, lon)
 historical = self._get_historical_analysis(lat, lon)
 
 # Weight recent data 30%, historical 70% for irradiance
 if latest["data_quality"]["irradiance_available"] and historical["data_quality"]["irradiance_available"]:
 hybrid_irradiance = (latest["daily_irradiance_kwh_m2"] * 0.3 + 
 historical["daily_irradiance_kwh_m2"] * 0.7)
 confidence = "very_high"
 elif historical["data_quality"]["irradiance_available"]:
 hybrid_irradiance = historical["daily_irradiance_kwh_m2"]
 confidence = "high"
 else:
 hybrid_irradiance = latest["daily_irradiance_kwh_m2"]
 confidence = "medium"
 
 # Similar approach for temperature
 hybrid_temperature = (latest["avg_temperature_c"] * 0.3 + 
 historical["avg_temperature_c"] * 0.7)
 
 return {
 "analysis_type": "hybrid",
 "timeframe": "Recent trends + Historical patterns",
 "daily_irradiance_kwh_m2": round(hybrid_irradiance, 2),
 "avg_temperature_c": round(hybrid_temperature, 1),
 "recent_trend": latest["daily_irradiance_kwh_m2"],
 "historical_average": historical["daily_irradiance_kwh_m2"],
 "seasonal_variations": historical.get("seasonal_variations", self._get_default_seasonal_pattern(lat, lon)),
 "data_source": "DWD Hybrid Analysis",
 "confidence": confidence,
 "weights": {"recent": 0.3, "historical": 0.7},
 "component_data": {
 "latest": latest["data_quality"],
 "historical": historical["data_quality"]
 }
 }
 
 def _get_fallback_irradiance(self, lat: float, lon: float) -> float:
 """Get fallback irradiance based on German regional averages"""
 regional_data = {
 "north": 3.2, # Hamburg, Bremen area
 "south": 4.1, # Munich, Stuttgart area 
 "east": 3.6, # Berlin, Dresden area
 "west": 3.4, # Cologne, Düsseldorf area
 "center": 3.7 # Frankfurt, Hannover area
 }
 
 region = self._determine_german_region(lat, lon)
 return regional_data.get(region, 3.6) # Default to center
 
 def _get_fallback_temperature(self, lat: float, lon: float) -> float:
 """Get fallback temperature based on German regional averages"""
 regional_temps = {
 "north": 9.5, # Cooler northern regions
 "south": 11.0, # Warmer southern regions
 "east": 10.0, # Continental eastern regions
 "west": 10.5, # Mild western regions
 "center": 10.2 # Central regions
 }
 
 region = self._determine_german_region(lat, lon)
 return regional_temps.get(region, 10.2)
 
 def _determine_german_region(self, lat: float, lon: float) -> str:
 """Determine German region based on coordinates"""
 if lat > 53: # Northern Germany
 return "north"
 elif lat < 48.5: # Southern Germany 
 return "south"
 elif lon > 12: # Eastern Germany
 return "east"
 elif lon < 8: # Western Germany
 return "west"
 else:
 return "center"
 
 def _get_default_seasonal_pattern(self, lat: float = 51.0, lon: float = 10.0) -> Dict:
 """Default seasonal solar irradiance pattern for Germany (kWh/m²/day)"""
 # Base pattern for central Germany
 base_pattern = {
 1: 1.2, 2: 2.1, 3: 3.4, 4: 4.8, 5: 5.9, 6: 6.2,
 7: 6.0, 8: 5.1, 9: 3.8, 10: 2.5, 11: 1.4, 12: 1.0
 }
 
 # Regional adjustments based on location
 region = self._determine_german_region(lat, lon)
 
 # Regional factors for seasonal adjustment
 regional_factors = {
 "north": { # Hamburg, Bremen - less solar, shorter summers
 "winter_factor": 0.8,
 "summer_factor": 0.9,
 "shoulder_factor": 0.95
 },
 "south": { # Munich, Stuttgart - more solar, alpine effect
 "winter_factor": 1.1,
 "summer_factor": 1.15,
 "shoulder_factor": 1.05
 },
 "east": { # Berlin, Dresden - continental climate
 "winter_factor": 0.9,
 "summer_factor": 1.05,
 "shoulder_factor": 1.0
 },
 "west": { # Cologne, Düsseldorf - maritime climate
 "winter_factor": 0.95,
 "summer_factor": 0.95,
 "shoulder_factor": 1.0
 },
 "center": { # Frankfurt, Hannover - baseline
 "winter_factor": 1.0,
 "summer_factor": 1.0,
 "shoulder_factor": 1.0
 }
 }
 
 factors = regional_factors.get(region, regional_factors["center"])
 
 # Apply seasonal adjustments
 adjusted_pattern = {}
 for month, value in base_pattern.items():
 if month in [12, 1, 2]: # Winter months
 adjusted_pattern[month] = round(value * factors["winter_factor"], 2)
 elif month in [6, 7, 8]: # Summer months
 adjusted_pattern[month] = round(value * factors["summer_factor"], 2)
 else: # Shoulder seasons (spring/fall)
 adjusted_pattern[month] = round(value * factors["shoulder_factor"], 2)
 
 return adjusted_pattern
 
 def _calculate_seasonal_factor(self, lat: float = 51.0, lon: float = 10.0) -> float:
 """Calculate current seasonal adjustment factor"""
 current_month = datetime.now().month
 seasonal_pattern = self._get_default_seasonal_pattern(lat, lon)
 annual_average = sum(seasonal_pattern.values()) / 12
 return round(seasonal_pattern[current_month] / annual_average, 2)
 
 # Caching methods removed - no caching for fresh data
 
 def get_weather_summary(self, lat: float, lon: float) -> Dict:
 """Get comprehensive weather summary with all analysis types"""
 print(f"Generating comprehensive weather summary for ({lat}, {lon})")
 
 return {
 "location": {"latitude": lat, "longitude": lon, "region": self._determine_german_region(lat, lon)},
 "analysis_date": datetime.now().isoformat(),
 "latest": self._get_latest_analysis(lat, lon),
 "historical": self._get_historical_analysis(lat, lon), 
 "hybrid": self._get_hybrid_analysis(lat, lon),
 "seasonal_pattern": self._get_default_seasonal_pattern(lat, lon),
 "current_seasonal_factor": self._calculate_seasonal_factor(lat, lon)
 }
 
 def get_analysis_options(self) -> Dict:
 """Get available weather analysis options for frontend"""
 return {
 "latest": {
 "label": "Recent Weather",
 "description": "Based on last 30 days - quick analysis",
 "timeframe": "30 days",
 "speed": "fast",
 "accuracy": "current conditions",
 "icon": ""
 },
 "historical": {
 "label": "Long-term Average", 
 "description": "Based on 5+ years - comprehensive analysis",
 "timeframe": "5+ years",
 "speed": "thorough",
 "accuracy": "long-term patterns",
 "icon": ""
 },
 "hybrid": {
 "label": "Smart Analysis",
 "description": "Combines recent + historical - most accurate",
 "timeframe": "30 days + 5 years",
 "speed": "balanced",
 "accuracy": "optimized",
 "icon": "",
 "recommended": True
 }
 }
