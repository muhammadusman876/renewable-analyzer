import pandas as pd
import numpy as np
from typing import Dict, Optional, Optional
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
 
 def get_location_irradiance(self, location: str) -> pd.Series:
 """
 Get solar irradiance data using reliable 2012-2017 EDA solar data
 """
 if self.eda_data is not None and 'Solar' in self.eda_data.columns:
 # Use actual solar production data from reliable EDA period (2012-2017)
 solar_production = self.eda_data['Solar']
 
 # Convert solar production to irradiance estimates
 # German solar capacity: ~32GW (2012) to ~42GW (2017), avg ~37GW
 # Total panel area: ~220 million m² (more conservative estimate)
 avg_capacity_gw = 37
 estimated_area_million_m2 = 220
 
 # Convert GWh production to kWh/m²/day irradiance
 # Account for capacity factor: actual production vs theoretical max
 # Germany capacity factor ~11%, so divide by this to get potential irradiance
 capacity_factor = 0.11
 
 irradiance = (solar_production * 1000 * capacity_factor) / (estimated_area_million_m2 * self.PANEL_EFFICIENCY * self.SYSTEM_LOSSES)
 
 # Ensure realistic values for Germany (0.2 to 8.0 kWh/m²/day)
 irradiance = irradiance.clip(lower=0.2, upper=8.0)
 
 # Fill any remaining NaN values with the mean
 irradiance = irradiance.fillna(irradiance.mean())
 
 return irradiance
 else:
 # This should not happen with reliable data, but provide a safety net
 if self.eda_data is not None and 'sunshine_duration_germany_avg' in self.eda_data.columns:
 sunshine_hours = self.eda_data['sunshine_duration_germany_avg']
 # Convert sunshine duration to irradiance (conservative factor)
 irradiance = sunshine_hours * 0.0005 # kWh/m²/hour during sunshine
 irradiance = irradiance.clip(lower=0.2, upper=8.0)
 return irradiance.fillna(4.0) # German average
 else:
 raise Exception("No reliable solar or sunshine data available in dataset")
 
 def get_orientation_factor(self, orientation: str) -> float:
 """Get efficiency factor based on roof orientation"""
 return self.ORIENTATION_FACTORS.get(orientation.lower(), 0.85)
 
 def calculate_monthly_production(self, annual_kwh: float) -> list[float]:
 """Calculate monthly production distribution based on real EDA solar data"""
 # Calculate actual monthly distribution from EDA dataset
 if self.eda_data is not None and 'Solar' in self.eda_data.columns and 'Date' in self.eda_data.columns:
 try:
 # Parse dates if needed and extract months
 if not pd.api.types.is_datetime64_any_dtype(self.eda_data['Date']):
 self.eda_data['Date'] = pd.to_datetime(self.eda_data['Date'], format='%d-%m-%Y')
 
 self.eda_data['Month'] = self.eda_data['Date'].dt.month
 
 # Calculate monthly solar production averages from real data
 monthly_solar = self.eda_data.groupby('Month')['Solar'].mean()
 total_solar = monthly_solar.sum()
 
 # Convert to monthly factors (what fraction of annual production each month represents)
 monthly_factors = [monthly_solar.get(i, 0) / total_solar for i in range(1, 13)]
 
 return [annual_kwh * factor for factor in monthly_factors]
 
 except Exception as e:
 print(f"Error calculating monthly factors from EDA data: {e}")
 
 # Fallback to estimated factors based on German solar patterns if EDA data unavailable
 # Realistic German solar production: Low in winter, peak in summer (June/July)
 monthly_factors = [
 0.03, 0.05, 0.08, 0.11, 0.14, 0.16, # Jan-Jun (winter → spring → early summer)
 0.17, 0.15, 0.12, 0.08, 0.05, 0.03 # Jul-Dec (peak summer → autumn → winter)
 ]
 
 return [annual_kwh * factor for factor in monthly_factors]
 
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
 
 Args:
 location: German city or region (optional if lat/lon provided)
 latitude, longitude: Coordinates for weather analysis
 roof_area: Available roof area in m²
 orientation: Roof orientation
 weather_analysis: "latest", "historical", or "hybrid"
 
 Returns:
 Dictionary with enhanced production estimates including weather analysis
 """
 try:
 # Use coordinates if provided, otherwise get from location
 if latitude is None or longitude is None:
 if location:
 # German city coordinates (major cities covered by DWD weather stations)
 city_coords = {
 "berlin": (52.52, 13.405),
 "munich": (48.137, 11.576),
 "hamburg": (53.55, 9.993),
 "cologne": (50.937, 6.96),
 "frankfurt": (50.11, 8.682),
 "stuttgart": (48.776, 9.182),
 "düsseldorf": (51.225, 6.782),
 "dortmund": (51.513, 7.463),
 "essen": (51.458, 7.014),
 "leipzig": (51.339, 12.374),
 "bremen": (53.079, 8.801),
 "dresden": (51.049, 13.738),
 "hannover": (52.375, 9.732),
 "nuremberg": (49.453, 11.077),
 "duisburg": (51.435, 6.761),
 "bochum": (51.481, 7.216),
 "wuppertal": (51.256, 7.150),
 "bielefeld": (52.020, 8.532),
 "bonn": (50.735, 7.100),
 "münster": (51.960, 7.625)
 }
 coords = city_coords.get(location.lower(), (51.165, 10.452)) # German geographic center
 latitude, longitude = coords
 else:
 latitude, longitude = 51.165, 10.452 # German geographic center
 
 # Get weather analysis
 weather_data = self.weather_service.get_solar_analysis(
 latitude, longitude, weather_analysis
 )
 
 # Extract solar irradiance and other parameters
 daily_irradiance = weather_data['daily_irradiance_kwh_m2']
 seasonal_variations = weather_data.get('seasonal_variations', {})
 
 # Apply orientation factor
 orientation_factor = self.get_orientation_factor(orientation)
 
 # Calculate system capacity based on roof area
 # Assuming 150W/m² for typical installations
 system_capacity_kw = roof_area * 0.15 # 150W per m²
 
 # Calculate monthly production using seasonal data
 monthly_outputs = {}
 annual_output = 0
 
 if seasonal_variations:
 # Use actual seasonal data (handle both string and int keys)
 for month in range(1, 13):
 monthly_irradiance = seasonal_variations.get(str(month), seasonal_variations.get(month, daily_irradiance))
 days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month-1]
 
 monthly_output = (
 monthly_irradiance * 
 days_in_month *
 system_capacity_kw * 
 orientation_factor * 
 self.SYSTEM_LOSSES
 )
 
 monthly_outputs[month] = round(monthly_output, 2)
 annual_output += monthly_output
 else:
 # Use average daily irradiance
 annual_output = (
 daily_irradiance * 
 365 * 
 system_capacity_kw * 
 orientation_factor * 
 self.SYSTEM_LOSSES
 )
 
 # Calculate monthly distribution
 monthly_production = self.calculate_monthly_production(annual_output)
 monthly_outputs = {i+1: round(monthly_production[i], 2) for i in range(12)}
 
 # Calculate additional metrics
 capacity_factor = (annual_output / (system_capacity_kw * 8760)) * 100 if system_capacity_kw > 0 else 0
 peak_month = max(monthly_outputs.keys(), key=lambda k: monthly_outputs[k])
 peak_month_production = monthly_outputs[peak_month]
 
 return {
 "annual_output_kwh": round(annual_output, 2),
 "monthly_outputs_kwh": monthly_outputs,
 "daily_average_kwh": round(annual_output / 365, 2),
 "system_capacity_kw": round(system_capacity_kw, 2),
 "capacity_factor": round(capacity_factor, 1),
 "peak_month": peak_month,
 "peak_month_production": peak_month_production,
 "weather_analysis": weather_data,
 "calculation_parameters": {
 "roof_area_m2": roof_area,
 "orientation": orientation,
 "orientation_factor": orientation_factor,
 "system_efficiency": self.SYSTEM_LOSSES,
 "panel_efficiency": self.PANEL_EFFICIENCY,
 "weather_type": weather_analysis,
 "coordinates": {"latitude": latitude, "longitude": longitude}
 }
 }
 
 except Exception as e:
 print(f"Enhanced calculation error: {e}")
 # Fallback to basic calculation
 return self.calculate_annual_output(location or "Germany", roof_area, orientation)
 
 def calculate_annual_output(
 self, 
 location: str, 
 roof_area: float, 
 orientation: str = "south"
 ) -> Dict:
 """
 Calculate expected annual solar output using EDA data
 
 Args:
 location: German city or region
 roof_area: Available roof area in m²
 orientation: Roof orientation
 
 Returns:
 Dictionary with production estimates
 """
 try:
 # Get historical solar irradiance for location
 irradiance_data = self.get_location_irradiance(location)
 
 # Calculate average daily irradiance
 avg_daily_irradiance = irradiance_data.mean() # kWh/m²/day
 
 # Apply orientation factor
 orientation_factor = self.get_orientation_factor(orientation)
 
 # Calculate annual production
 # Formula: Irradiance × Area × Efficiency × System_Losses × Orientation × Days
 daily_kwh = (
 avg_daily_irradiance * 
 roof_area * 
 self.PANEL_EFFICIENCY * 
 self.SYSTEM_LOSSES * 
 orientation_factor
 )
 
 annual_kwh = daily_kwh * 365
 
 # Calculate monthly breakdown
 monthly_production = self.calculate_monthly_production(annual_kwh)
 
 # Peak month production (typically June/July in Germany)
 peak_month_kwh = max(monthly_production)
 
 return {
 "annual_kwh": round(annual_kwh, 1),
 "daily_average": round(daily_kwh, 1),
 "peak_month_production": round(peak_month_kwh, 1),
 "monthly_production": [round(x, 1) for x in monthly_production],
 "system_capacity_kw": round(roof_area * 0.2, 1), # Assuming 200W/m²
 "capacity_factor": round((annual_kwh / (roof_area * 0.2 * 8760)) * 100, 1)
 }
 
 except Exception as e:
 raise Exception(f"Solar calculation failed: {str(e)}")
 
 def estimate_system_size(self, annual_consumption_kwh: float, roof_area: float) -> Dict:
 """
 Estimate optimal system size based on consumption and available roof area
 """
 # Calculate maximum possible production with available roof area
 max_production = self.calculate_annual_output("Germany", roof_area, "south")
 
 # Determine optimal size (typically 80-100% of annual consumption)
 optimal_coverage = min(1.0, annual_consumption_kwh / max_production["annual_kwh"])
 optimal_area = roof_area * optimal_coverage
 
 optimal_system = self.calculate_annual_output("Germany", optimal_area, "south")
 
 return {
 "recommended_area": round(optimal_area, 1),
 "coverage_ratio": round(optimal_coverage * 100, 1),
 **optimal_system
 }
