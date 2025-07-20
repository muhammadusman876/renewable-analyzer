from typing import Dict, Optional
import numpy as np
try:
    from app.core.electricity_price import get_electricity_price
except ImportError:
    def get_electricity_price():
        return 0.32


class ROICalculator:
    """Calculate ROI, payback period, and financial metrics for solar installations"""
    
    def __init__(self):
        self.system_cost_per_kw = 1800  # Euro per kW installed capacity (realistic 2025 prices)
        self.maintenance_cost_per_year = 200  # Euro per year (insurance, cleaning, monitoring)
        self.system_lifetime = 25  # years
        self.degradation_rate = 0.005  # 0.5% per year
        self.discount_rate = 0.04  # 4% discount rate
        
    def get_location_specific_factors(self, location: str) -> Dict:
        """Get location-specific factors for Germany"""
        location_factors = {
            "Berlin": {"incentive_multiplier": 1.0, "grid_cost": 0.29},
            "Munich": {"incentive_multiplier": 1.15, "grid_cost": 0.31},
            "Hamburg": {"incentive_multiplier": 1.05, "grid_cost": 0.30},
        }
        return location_factors.get(location, {"incentive_multiplier": 1.0, "grid_cost": 0.30})

    def calculate_self_consumption_rate(self, solar_production_kwh: float, household_consumption_kwh: Optional[float]) -> Dict:
        """Calculate realistic self-consumption rate based on household usage patterns"""
        if not household_consumption_kwh or household_consumption_kwh <= 0:
            # Default German household average
            return {
                "self_consumption_rate": 0.40,
                "method": "default_average",
                "household_coverage": None
            }
        
        # Calculate raw self-consumption potential
        if household_consumption_kwh <= solar_production_kwh:
            # Household consumes less than solar produces
            raw_self_consumption = household_consumption_kwh / solar_production_kwh
            household_coverage = 100.0  # Solar covers 100% of consumption
        else:
            # Household consumes more than solar produces
            raw_self_consumption = 1.0  # All solar production is self-consumed
            household_coverage = (solar_production_kwh / household_consumption_kwh) * 100
        
        # Apply realistic behavior factors:
        # - Time-of-use mismatch (solar peak vs consumption peak)
        # - Seasonal variations (winter consumption vs summer production)
        # - Typical German household consumption patterns
        
        if raw_self_consumption >= 0.8:
            # High self-consumption potential - apply modest adjustment
            adjusted_rate = raw_self_consumption * 0.85
        elif raw_self_consumption >= 0.5:
            # Medium self-consumption - standard adjustment
            adjusted_rate = raw_self_consumption * 0.80
        else:
            # Low self-consumption - minimal adjustment
            adjusted_rate = raw_self_consumption * 0.90
        
        # Cap realistic self-consumption at 95% (some export always occurs)
        final_rate = min(0.95, max(0.20, adjusted_rate))
        
        return {
            "self_consumption_rate": round(final_rate, 3),
            "method": "household_based",
            "household_coverage": round(household_coverage, 1) if household_coverage is not None else None,
            "raw_rate": round(raw_self_consumption, 3)
        }

    def calculate_german_incentives(self, system_capacity_kw: float, location: str) -> Dict:
        """Calculate German solar incentives"""
        location_factors = self.get_location_specific_factors(location)
        
        if system_capacity_kw <= 10:
            base_tariff = 0.082  # 8.2 ct/kWh for systems ≤10 kWp
        elif system_capacity_kw <= 40:
            base_tariff = 0.071  # 7.1 ct/kWh for 10-40 kWp
        else:
            base_tariff = 0.057  # 5.7 ct/kWh for >40 kWp
            
        adjusted_tariff = base_tariff * location_factors["incentive_multiplier"]
        kfw_benefit = min(system_capacity_kw * 200, 10000)
        regional_incentive = system_capacity_kw * 150
        
        return {
            "feed_in_tariff_eur_per_kwh": round(adjusted_tariff, 4),
            "kfw_loan_benefit_eur": round(kfw_benefit, 2),
            "regional_incentive_eur": round(regional_incentive, 2),
            "total_incentives_eur": round(kfw_benefit + regional_incentive, 2)
        }

    def calculate_npv_and_irr(self, annual_savings: float, total_investment: float, system_capacity_kw: float) -> Dict:
        """Calculate Net Present Value and Internal Rate of Return"""
        years = self.system_lifetime
        cash_flows = [-total_investment]
        
        for year in range(1, years + 1):
            degraded_savings = annual_savings * ((1 - self.degradation_rate) ** year)
            net_annual_flow = degraded_savings - self.maintenance_cost_per_year
            cash_flows.append(net_annual_flow)
        
        npv = sum(cf / ((1 + self.discount_rate) ** i) for i, cf in enumerate(cash_flows))
        irr_estimate = (annual_savings / total_investment) * 100
        
        return {
            "npv_eur": round(npv, 2),
            "irr_percentage": round(irr_estimate, 1),
            "lifetime_savings_eur": round(sum(cash_flows[1:]), 2)
        }

    def calculate_roi(self, solar_output: Dict, budget: Optional[float], location: str, household_consumption: Optional[float] = None) -> Dict:
        """Enhanced ROI calculation with budget constraints, system scaling, and household consumption analysis"""
        try:
            annual_kwh = solar_output.get("annual_kwh", 0)
            system_capacity_kw = solar_output.get("system_capacity_kw", 0)
            
            base_installation_cost = system_capacity_kw * self.system_cost_per_kw
            location_factors = self.get_location_specific_factors(location)
            incentives = self.calculate_german_incentives(system_capacity_kw, location)
            
            scaling_info = {"system_scaled": False}
            
            if budget and budget > 0:
                net_system_cost = base_installation_cost - incentives["total_incentives_eur"]
                
                if net_system_cost > budget:
                    scaling_factor = budget / net_system_cost
                    system_capacity_kw = system_capacity_kw * scaling_factor
                    annual_kwh = annual_kwh * scaling_factor
                    
                    base_installation_cost = system_capacity_kw * self.system_cost_per_kw
                    incentives = self.calculate_german_incentives(system_capacity_kw, location)
                    
                    scaling_info = {
                        "system_scaled": True,
                        "scaling_factor": round(scaling_factor, 3),
                        "scaled_capacity_kw": round(system_capacity_kw, 2),
                        "scaled_annual_kwh": round(annual_kwh, 1)
                    }
            
            total_investment = base_installation_cost - incentives["total_incentives_eur"]
            
            if total_investment < 500:
                total_investment = 500
            
            electricity_rate = get_electricity_price()
            
            # Calculate self-consumption based on household usage patterns
            consumption_analysis = self.calculate_self_consumption_rate(annual_kwh, household_consumption)
            self_consumption_rate = consumption_analysis["self_consumption_rate"]
            feed_in_rate = 1.0 - self_consumption_rate
            
            # Calculate direct electricity savings (self-consumed portion)
            self_consumed_kwh = annual_kwh * self_consumption_rate
            annual_electricity_savings = self_consumed_kwh * electricity_rate
            
            # Calculate feed-in income (exported portion)
            fed_in_kwh = annual_kwh * feed_in_rate
            feed_in_income = fed_in_kwh * incentives["feed_in_tariff_eur_per_kwh"]
            
            # Total annual benefit
            annual_savings = annual_electricity_savings + feed_in_income
            
            if annual_savings > 0:
                payback_period = total_investment / annual_savings
            else:
                payback_period = 999
            
            roi_percentage = ((annual_savings * self.system_lifetime) - total_investment) / total_investment * 100
            financial_metrics = self.calculate_npv_and_irr(annual_savings, total_investment, system_capacity_kw)
            
            # CO₂ reduction calculation with correct German grid carbon factor
            # German grid carbon factor: 0.401 kg CO₂/kWh (2023 data)
            co2_reduction_kg_per_year = annual_kwh * 0.401  # kg CO₂ per year
            co2_reduction_tons_per_year = co2_reduction_kg_per_year / 1000  # Convert to tons per year
            co2_reduction_tons_lifetime = co2_reduction_tons_per_year * self.system_lifetime
            
            return {
                "annual_savings": round(annual_savings, 2),
                "payback_period": round(payback_period, 1),
                "roi_percentage": round(roi_percentage, 1),
                "total_investment": round(total_investment, 2),
                "co2_reduction": round(co2_reduction_tons_per_year, 2),  # Annual CO₂ reduction in tons
                "co2_reduction_lifetime": round(co2_reduction_tons_lifetime, 1),  # 25-year lifetime reduction
                "system_capacity_kw": round(system_capacity_kw, 2),
                "annual_kwh_adjusted": round(annual_kwh, 1),
                "self_consumed_kwh": round(self_consumed_kwh, 1),
                "fed_in_kwh": round(fed_in_kwh, 1),
                "electricity_savings_eur": round(annual_electricity_savings, 2),
                "feed_in_income_eur": round(feed_in_income, 2),
                "electricity_rate_eur_per_kwh": round(electricity_rate, 3),
                "self_consumption_rate": round(self_consumption_rate * 100, 1),  # Convert to percentage
                "household_coverage": consumption_analysis.get("household_coverage"),
                "consumption_analysis": consumption_analysis,
                "incentives": incentives,
                "location_factors": location_factors,
                "scaling_info": scaling_info,
                **financial_metrics
            }
            
        except Exception as e:
            raise Exception(f"ROI calculation failed: {str(e)}")

    def get_financing_options(self, total_investment: float) -> Dict:
        """Get available financing options for solar installation"""
        return {
            "cash_payment": {
                "amount": total_investment,
                "total_cost": total_investment,
                "description": "Full upfront payment"
            }
        }
