import pandas as pd
import numpy as np
from typing import Dict, Optional
from .weather_service import WeatherAnalysisService
import os

class SolarCalculator:
    """
    Solar potential calculator using EDA dataset from Germany renewable energy analysis
    """
    
    def __init__(self, eda_dataset_path: Optional[str] = None):
        """Initialize with path to the processed EDA dataset"""
        # Use original dataset (2012-2017 is our reliable historical period)
        if eda_dataset_path is None:
            eda_dataset_path = "app/data/processed_eda_data/renewable_weather.csv"
        
        self.eda_dataset_path = eda_dataset_path
        self.eda_data = None
        self.weather_service = WeatherAnalysisService()
        self.load_eda_data()
        
        # Solar panel efficiency constants
        self.PANEL_EFFICIENCY = 0.20  # 20% efficiency for modern panels
        self.SYSTEM_LOSSES = 0.85     # 15% system losses (inverter, wiring, etc.)
        self.DEGRADATION_RATE = 0.005 # 0.5% annual degradation
        
        # Orientation factors (compared to optimal south-facing)
        self.ORIENTATION_FACTORS = {
            "south": 1.0,
            "southeast": 0.95,
            "southwest": 0.95,
            "east": 0.85,
            "west": 0.85,
            "northeast": 0.75,
            "northwest": 0.75,
            "north": 0.6
        }

    def load_eda_data(self):
        """Load the EDA dataset focusing on reliable 2012-2017 data"""
        try:
            if os.path.exists(self.eda_dataset_path):
                # Load with Date parsing
                sample = pd.read_csv(self.eda_dataset_path, nrows=1)
                parse_dates = ['Date'] if 'Date' in sample.columns else []
                self.eda_data = pd.read_csv(self.eda_dataset_path, parse_dates=parse_dates if parse_dates else False)
                
                # Filter to reliable data period (2012-2017) if Date column exists
                if 'Date' in self.eda_data.columns:
                    if not pd.api.types.is_datetime64_any_dtype(self.eda_data['Date']):
                        self.eda_data['Date'] = pd.to_datetime(self.eda_data['Date'], format='%d-%m-%Y')
                    
                    # Focus on reliable data period: 2012-2017
                    self.eda_data = self.eda_data[
                        (self.eda_data['Date'].dt.year >= 2012) & 
                        (self.eda_data['Date'].dt.year <= 2017)
                    ].copy()
                    
                    print(f"Loaded EDA data: {len(self.eda_data)} records (2012-2017 reliable period)")
                    
                    # Verify data quality for this period
                    solar_missing = self.eda_data['Solar'].isna().sum()
                    wind_missing = self.eda_data['Wind'].isna().sum()
                    print(f"Data quality: Solar missing {solar_missing}, Wind missing {wind_missing}")
                else:
                    print(f"Loaded EDA data: {len(self.eda_data)} records")
            else:
                raise FileNotFoundError(f"EDA dataset not found: {self.eda_dataset_path}")
                
        except Exception as e:
            print(f"Error loading EDA data: {e}")
            raise Exception(f"Failed to load reliable EDA dataset: {e}")

    def calculate_annual_output_enhanced(
        self, 
        location: Optional[str] = None,
        latitude: Optional[float] = None,
        longitude: Optional[float] = None, 
        roof_area: float = 0, 
        orientation: str = "south",
        weather_analysis: str = "hybrid"
    ) -> Dict:
        """
        Enhanced calculation using weather analysis service
        """
        try:
            # Get weather analysis results
            if latitude is not None and longitude is not None:
                weather_results = self.weather_service.analyze_weather_conditions(
                    latitude, longitude, weather_analysis
                )
            else:
                raise ValueError("Latitude and longitude are required")
            
            # Extract weather data
            weather_data = weather_results.get(weather_analysis, {})
            daily_irradiance = weather_data.get('daily_irradiance_kwh_m2', 3.5)  # Default fallback
            
            # Calculate system capacity (200W/m² realistic panel density for Germany)
            system_capacity_kw = roof_area * 0.20
            
            # Apply orientation factor
            orientation_factor = self.ORIENTATION_FACTORS.get(orientation.lower(), 0.85)
            
            # Calculate annual output using ANNUAL AVERAGE irradiance (not daily peak)
            # Convert daily irradiance to annual average (July peak ÷ 1.4 seasonal factor)
            annual_avg_irradiance = daily_irradiance / 1.4  # Convert July peak to annual average
            
            annual_output_kwh = (
                annual_avg_irradiance * 
                roof_area * 
                self.PANEL_EFFICIENCY * 
                self.SYSTEM_LOSSES * 
                orientation_factor * 
                365
            )
            
            # Calculate monthly outputs using seasonal pattern
            seasonal_pattern = weather_data.get('seasonal_variations', {})
            monthly_outputs = {}
            
            for month in range(1, 13):
                # Use seasonal pattern to distribute annual production
                monthly_factor = seasonal_pattern.get(str(month), 1.0)
                # Normalize by average factor to ensure total = annual
                avg_factor = sum(seasonal_pattern.values()) / 12 if seasonal_pattern else 1.0
                normalized_factor = monthly_factor / avg_factor if avg_factor > 0 else 1.0
                monthly_outputs[month] = annual_output_kwh * normalized_factor / 12
            
            # Find peak month
            peak_month = max(monthly_outputs.keys(), key=lambda x: monthly_outputs[x])
            peak_month_production = monthly_outputs[peak_month]
            
            return {
                "annual_output_kwh": round(annual_output_kwh, 2),
                "monthly_outputs_kwh": monthly_outputs,
                "daily_average_kwh": round(annual_output_kwh / 365, 2),
                "system_capacity_kw": round(system_capacity_kw, 1),
                "capacity_factor": round((annual_output_kwh / (system_capacity_kw * 8760)) * 100, 1),
                "peak_month": peak_month,
                "peak_month_production": round(peak_month_production, 2),
                "weather_analysis": weather_results,
                "calculation_parameters": {
                    "roof_area_m2": roof_area,
                    "orientation": orientation,
                    "orientation_factor": orientation_factor,
                    "panel_efficiency": self.PANEL_EFFICIENCY,
                    "system_losses": self.SYSTEM_LOSSES,
                    "daily_irradiance_peak": daily_irradiance,
                    "annual_avg_irradiance": annual_avg_irradiance,
                    "system_capacity_calculation": f"{roof_area}m² × 0.20 = {system_capacity_kw}kW"
                }
            }
            
        except Exception as e:
            print(f"Error in enhanced solar calculation: {e}")
            raise Exception(f"Solar calculation failed: {e}")
