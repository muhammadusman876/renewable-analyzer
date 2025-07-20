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
            # For latest analysis, use the base irradiance without additional seasonal adjustment
            # The latest_irradiance already includes seasonal effects from DWD fallback
            
            # Get seasonal variations for monthly calculations
            seasonal_variations = self._get_default_seasonal_pattern(lat, lon)
            
            return {
                "daily_irradiance_kwh_m2": latest_irradiance,  # Use direct value, no extra seasonal factor
                "temperature_celsius": latest_temperature or 15.0,
                "seasonal_factor": 1.0,  # No additional seasonal adjustment
                "seasonal_variations": seasonal_variations,
                "data_source": "DWD_latest",
                "analysis_date": datetime.now().isoformat()
            }
        else:
            # Fallback to regional patterns
            return self._get_regional_fallback(lat, lon)

    def _get_historical_analysis(self, lat: float, lon: float) -> Dict:
        """Historical data analysis using EDA 2012-2017 data"""
        print("Analyzing long-term historical patterns...")
        
        # Check if DWD fetcher has historical methods (backwards compatibility)
        historical_irradiance = None
        historical_temperature = None
        
        if hasattr(self.dwd_fetcher, 'get_historical_irradiance'):
            print("Fetching fresh historical data (no cache)")
            historical_irradiance = self.dwd_fetcher.get_historical_irradiance(lat, lon, years=5)
            historical_temperature = self.dwd_fetcher.get_historical_temperature(lat, lon, years=5)
        else:
            print("Historical methods not available - using EDA data 2012-2017")
            historical_irradiance, historical_temperature = self._extract_eda_historical_data(lat, lon)
        
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
            "data_source": "EDA_2012_2017" if historical_irradiance else "regional_patterns",
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
        
        # Show data source composition
        historical_source = historical.get("data_source", "unknown")
        hybrid_source = f"hybrid_30pct_recent_70pct_{historical_source}"
        
        return {
            "daily_irradiance_kwh_m2": hybrid_irradiance,
            "temperature_celsius": hybrid_temperature,
            "seasonal_variations": historical.get("seasonal_variations", {}),
            "data_source": hybrid_source,
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

    def _extract_eda_historical_data(self, lat: float, lon: float) -> tuple:
        """Extract historical solar irradiance and temperature from EDA 2012-2017 data"""
        try:
            import pandas as pd
            import os
            
            # Path to EDA data
            eda_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed_eda_data', 'renewable_weather.csv')
            
            if not os.path.exists(eda_path):
                print(f"EDA data not found at {eda_path}")
                return None, None
                
            print(f"Loading EDA historical data from {eda_path}")
            df = pd.read_csv(eda_path)
            
            # Check actual column names
            print(f"EDA columns: {list(df.columns)}")
            
            # Convert Date column to datetime
            df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y', errors='coerce')
            
            # Filter to 2012-2017 reliable period
            df_filtered = df[(df['Date'].dt.year >= 2012) & (df['Date'].dt.year <= 2017)]
            
            print(f"EDA data: {len(df_filtered)} records from 2012-2017")
            
            if len(df_filtered) == 0:
                print("No EDA data in 2012-2017 range")
                return None, None
            
            # Calculate overall averages using actual column names
            solar_avg = df_filtered['Solar'].mean() if 'Solar' in df_filtered else None
            temp_avg = df_filtered['temperature_air_mean_2m_germany_avg'].mean() if 'temperature_air_mean_2m_germany_avg' in df_filtered else None
            
            # Calculate monthly patterns
            monthly_solar = {}
            if 'Solar' in df_filtered.columns:
                df_filtered['month'] = df_filtered['Date'].dt.month
                monthly_averages = df_filtered.groupby('month')['Solar'].mean()
                for month in range(1, 13):
                    monthly_solar[str(month)] = monthly_averages.get(month, solar_avg)
            
            # Convert solar from original units to daily irradiance
            # EDA Solar is in GWh, convert to kWh/m2 daily irradiance for German conditions
            # Approximate conversion: 1 GWh = 4.2 kWh/m2 daily for Germany
            if solar_avg:
                daily_irradiance = solar_avg * 4.2 / 1000  # Convert GWh to kWh/m2
                
                historical_irradiance = {
                    "overall_average": daily_irradiance,
                    "monthly_averages": {k: v * 4.2 / 1000 for k, v in monthly_solar.items()}
                }
                print(f"EDA extraction: Solar={solar_avg:.1f} GWh -> Irradiance={daily_irradiance:.3f} kWh/m²")
            else:
                historical_irradiance = None
                print("No solar data available in EDA dataset")
            
            if temp_avg:
                historical_temperature = {"overall_average": temp_avg}
                print(f"Temperature: {temp_avg:.1f}°C")
            else:
                historical_temperature = None
                print("No temperature data available in EDA dataset")
            return historical_irradiance, historical_temperature
            
        except Exception as e:
            print(f"Error extracting EDA data: {e}")
            import traceback
            traceback.print_exc()
            return None, None

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
