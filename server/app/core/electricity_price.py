import json
import os
from datetime import datetime
from typing import Optional
import requests

# Configuration path for storing electricity price
CONFIG_PATH = os.path.join(os.path.dirname(__file__), '..', 'config', 'electricity_price.json')

def get_electricity_price() -> float:
    """
    Read the latest electricity price (EUR/kWh) from config file.
    """
    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return float(data.get('electricity_price_eur_per_kwh', 0.34))
    except Exception as e:
        print(f"Error reading electricity price config: {e}")
        # Updated fallback to current German household average (2025)
        return 0.34  # fallback: current German household electricity price

def update_electricity_price(new_price: float, timestamp: Optional[str] = None):
    """
    Update the electricity price in the config file.
    """
    if not timestamp:
        timestamp = datetime.utcnow().isoformat() + 'Z'
    
    data = {
        "electricity_price_eur_per_kwh": new_price,
        "last_updated": timestamp,
        "source": "manual_update"
    }
    
    # Ensure config directory exists
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    
    try:
        with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        print(f"Updated electricity price to {new_price} EUR/kWh")
    except Exception as e:
        print(f"Error updating electricity price config: {e}")

def fetch_live_electricity_price() -> Optional[float]:
    """
    Fetch live electricity price from German energy charts API.
    Returns price in EUR/kWh or None if failed.
    URL: https://api.energy-charts.info/price?bzn=DE-LU
    """
    try:
        print("Fetching live electricity price from German energy charts...")
        
        # Fetch data from German energy charts API
        url = "https://api.energy-charts.info/price?bzn=DE-LU"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # The API returns price data - extract the most recent price
        if 'price' in data and data['price']:
            # Get the latest price (usually the last entry)
            latest_price_raw = data['price'][-1] if isinstance(data['price'], list) else data['price']
            
            # Convert from EUR/MWh to EUR/kWh
            latest_price_kwh = latest_price_raw / 1000.0
            
            # Add household surcharges and taxes (approximate German household price multiplier)
            # German household electricity includes grid fees, taxes, surcharges
            household_multiplier = 3.5  # Approximate multiplier for wholesale to household price
            household_price = latest_price_kwh * household_multiplier
            
            # Ensure reasonable bounds (German household electricity typically 0.25-0.45 EUR/kWh)
            if household_price < 0.20:
                household_price = 0.30
            elif household_price > 0.50:
                household_price = 0.40
            
            print(f"Wholesale price: {latest_price_kwh:.4f} EUR/kWh")
            print(f"Estimated household price: {household_price:.4f} EUR/kWh")
            
            return round(household_price, 4)
        else:
            print("No price data found in API response")
            return None
            
    except requests.RequestException as e:
        print(f"Network error fetching electricity price: {e}")
        return None
    except Exception as e:
        print(f"Failed to fetch live electricity price: {e}")
        return None

def initialize_electricity_price():
    """
    Initialize the electricity price config file if it doesn't exist.
    Try to fetch live price, fallback to default if unavailable.
    """
    if not os.path.exists(CONFIG_PATH):
        print("Initializing electricity price config...")
        
        # Try to fetch live price first
        live_price = fetch_live_electricity_price()
        initial_price = live_price if live_price else 0.34
        
        update_electricity_price(
            initial_price, 
            datetime.utcnow().isoformat() + 'Z'
        )
        
        if live_price:
            print(f"Initialized with live price: {initial_price} EUR/kWh")
        else:
            print(f"Initialized with fallback price: {initial_price} EUR/kWh")
    else:
        print("Electricity price config already exists")

def update_price_from_api():
    """
    Update electricity price from the German energy charts API.
    Returns True if successful, False otherwise.
    """
    try:
        live_price = fetch_live_electricity_price()
        if live_price:
            update_electricity_price(
                live_price,
                datetime.utcnow().isoformat() + 'Z'
            )
            return True
        else:
            print("Failed to fetch live price - keeping current price")
            return False
    except Exception as e:
        print(f"Error updating price from API: {e}")
        return False

# Initialize on import
if __name__ != "__main__":
    initialize_electricity_price()

# Alias for backward compatibility
get_current_electricity_price = get_electricity_price
