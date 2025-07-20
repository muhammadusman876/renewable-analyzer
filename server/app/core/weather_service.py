from typing import Dict, Optional
import json
import os
from datetime import datetime
from .weather_dwd import DWDWeatherFetcher


class WeatherAnalysisService:
    """
    Advanced weather analysis service for solar potential calculations
    Provides latest, historical, and hybrid weather analysis for solar feasibility
    """
    
    def __init__(self):
        self.dwd_fetcher = DWDWeatherFetcher()
        # Caching disabled - always fetch fresh data
        print("Weather Analysis Service initialized (NO CACHING)")

    def analyze_weather_conditions(self, lat: float, lon: float, analysis_type: str = "hybrid") -> Dict:
        """
        Analyze weather conditions for solar potential
        
        Args:
            lat, lon: Coordinates
            analysis_type: "latest", "historical", or "hybrid"
        """
        print(f"Running {analysis_type} weather analysis for coordinates ({lat}, {lon})")
        
        if analysis_type == "latest":
            return {"latest": self._get_latest_analysis(lat, lon)}
        elif analysis_type == "historical":
            return {"historical": self._get_historical_analysis(lat, lon)}
        elif analysis_type == "hybrid":
            print("Running hybrid analysis (recent + historical)...")
            return {
                "latest": self._get_latest_analysis(lat, lon),
                "historical": self._get_historical_analysis(lat, lon),
                "hybrid": self._get_hybrid_analysis(lat, lon)
            }
        else:
            raise ValueError(f"Unknown analysis type: {analysis_type}")

    def _get_latest_analysis(self, lat: float, lon: float) -> Dict:
        """Latest weather data analysis (recent conditions)"""
        print("Analyzing recent weather conditions...")
        
        # Get latest irradiance and temperature
        latest_irradiance = self.dwd_fetcher.get_latest_irradiance(lat, lon)
        latest_temperature = self.dwd_fetcher.get_latest_temperature(lat, lon)
        
        if latest_irradiance:
            # Current month seasonal factor
            seasonal_factor = self._get_current_seasonal_factor(lat, lon)
            adjusted_irradiance = latest_irradiance * seasonal_factor
            
            return {
                "daily_irradiance_kwh_m2": adjusted_irradiance,
                "temperature_celsius": latest_temperature or 15.0,
                "seasonal_factor": seasonal_factor,
                "data_source": "DWD_latest",
                "analysis_date": datetime.now().isoformat()
            }
        else:
            # Fallback to regional patterns
            return self._get_regional_fallback(lat, lon)

    def _get_historical_analysis(self, lat: float, lon: float) -> Dict:
        """Historical data analysis (multi-year average) - NO CACHING"""
        print("Analyzing long-term historical patterns...")
        
        # ALWAYS fetch fresh data - no caching
        print("Fetching fresh historical data (no cache)")
        historical_irradiance = self.dwd_fetcher.get_historical_irradiance(lat, lon, years=5)
        historical_temperature = self.dwd_fetcher.get_historical_temperature(lat, lon, years=5)
        
        if historical_irradiance:
            irradiance = historical_irradiance["overall_average"]
            seasonal_variations = historical_irradiance["monthly_averages"]
        else:
            print("Using regional historical patterns for 5 years")
            irradiance = self._get_regional_irradiance_average(lat, lon)
            seasonal_variations = self._get_default_seasonal_pattern(lat, lon)
        
        if historical_temperature:
            temperature = historical_temperature["overall_average"]
        else:
            print("Using regional temperature patterns for 5 years")
            temperature = self._get_regional_temperature_average(lat, lon)
        
        return {
            "daily_irradiance_kwh_m2": irradiance,
            "temperature_celsius": temperature,
            "seasonal_variations": seasonal_variations,
            "data_source": "DWD_historical" if historical_irradiance else "regional_patterns",
            "analysis_date": datetime.now().isoformat()
        }

    def _get_hybrid_analysis(self, lat: float, lon: float) -> Dict:
        """Hybrid analysis combining recent and historical data"""
        latest = self._get_latest_analysis(lat, lon)
        historical = self._get_historical_analysis(lat, lon)
        
        # Weighted combination: 30% recent, 70% historical
        hybrid_irradiance = (latest["daily_irradiance_kwh_m2"] * 0.3 + 
                           historical["daily_irradiance_kwh_m2"] * 0.7)
        
        hybrid_temperature = (latest["temperature_celsius"] * 0.3 + 
                            historical["temperature_celsius"] * 0.7)
        
        return {
            "daily_irradiance_kwh_m2": hybrid_irradiance,
            "temperature_celsius": hybrid_temperature,
            "seasonal_variations": historical.get("seasonal_variations", {}),
            "data_source": "hybrid_analysis",
            "analysis_date": datetime.now().isoformat(),
            "weighting": {"recent": 0.3, "historical": 0.7}
        }

    def _get_regional_fallback(self, lat: float, lon: float) -> Dict:
        """Regional fallback when no DWD data available"""
        irradiance = self._get_regional_irradiance_average(lat, lon)
        temperature = self._get_regional_temperature_average(lat, lon)
        seasonal_pattern = self._get_default_seasonal_pattern(lat, lon)
        
        return {
            "daily_irradiance_kwh_m2": irradiance,
            "temperature_celsius": temperature,
            "seasonal_variations": seasonal_pattern,
            "data_source": "regional_fallback",
            "analysis_date": datetime.now().isoformat()
        }

    def _get_regional_irradiance_average(self, lat: float, lon: float) -> float:
        """Get regional average irradiance based on location"""
        # Germany regional averages (kWh/m²/day)
        if lat > 54.0:  # Northern Germany
            return 3.2
        elif lat > 51.5:  # Central-North Germany
            return 3.5
        elif lat > 49.0:  # Central Germany
            return 3.8
        else:  # Southern Germany
            return 4.1

    def _get_regional_temperature_average(self, lat: float, lon: float) -> float:
        """Get regional average temperature"""
        # Germany regional temperature averages (°C)
        if lat > 54.0:  # Northern Germany
            return 12.5
        elif lat > 51.5:  # Central-North Germany
            return 13.5
        elif lat > 49.0:  # Central Germany
            return 14.5
        else:  # Southern Germany
            return 15.5

    def _get_default_seasonal_pattern(self, lat: float, lon: float) -> Dict:
        """Get default seasonal irradiance pattern for location"""
        # Base seasonal pattern for Germany
        base_pattern = {
            "1": 0.4, "2": 0.6, "3": 0.8, "4": 1.1,
            "5": 1.3, "6": 1.4, "7": 1.4, "8": 1.2,
            "9": 1.0, "10": 0.7, "11": 0.5, "12": 0.3
        }
        
        # Regional adjustments
        region = self._determine_german_region(lat, lon)
        if region == "north":
            # Northern regions have more variation
            for month in ["6", "7"]:
                base_pattern[month] *= 1.1
            for month in ["12", "1", "2"]:
                base_pattern[month] *= 0.9
        elif region == "south":
            # Southern regions have higher winter values
            for month in ["12", "1", "2"]:
                base_pattern[month] *= 1.2
        
        return base_pattern

    def _determine_german_region(self, lat: float, lon: float) -> str:
        """Determine German region from coordinates"""
        if lat > 53.5:
            return "north"
        elif lat > 51.0:
            return "center"
        else:
            return "south"

    def _get_current_seasonal_factor(self, lat: float, lon: float) -> float:
        """Get seasonal adjustment factor for current month"""
        current_month = datetime.now().month
        seasonal_pattern = self._get_default_seasonal_pattern(lat, lon)
        annual_average = sum(seasonal_pattern.values()) / 12
        return round(seasonal_pattern[str(current_month)] / annual_average, 2)

    # Caching methods removed - no caching for fresh data
    
    def get_weather_summary(self, lat: float, lon: float) -> Dict:
        """Get comprehensive weather summary with all analysis types"""
        print(f"Generating comprehensive weather summary for ({lat}, {lon})")
        
        return {
            "location": {"latitude": lat, "longitude": lon, "region": self._determine_german_region(lat, lon)},
            "analysis_date": datetime.now().isoformat(),
            "latest": self._get_latest_analysis(lat, lon),
            "historical": self._get_historical_analysis(lat, lon),
            "hybrid": self._get_hybrid_analysis(lat, lon)
        }
