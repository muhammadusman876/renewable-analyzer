"""
Report Generator - Handles report template generation and formatting
"""
from typing import Dict, List


class ReportGenerator:
    """
    Generates solar feasibility reports using templates and dynamic content
    """

    def __init__(self):
        pass

        def create_prompt_template(self, user_input: Dict, calculations: Dict, context: List[str]) -> str:
            """Create a comprehensive prompt for LLM-based report generation"""

            context_text = "\n".join(context)

            prompt = f"""You are an expert renewable energy consultant specializing in German solar installations.
            Create a detailed, personalized solar panel investment feasibility report.

            CUSTOMER PROFILE:
            - Location: {user_input.get('location', 'Germany')}
            - Roof Area: {user_input.get('roof_area', 'N/A')} m²
            - Roof Orientation: {user_input.get('orientation', 'south')}
            - Available Budget: €{user_input.get('budget', 'Not specified')}
            - Energy Usage: {user_input.get('annual_consumption', 'Not specified')} kWh/year

            TECHNICAL CALCULATIONS:
            - Annual Production: {calculations.get('annual_kwh', 'N/A')} kWh
            - System Capacity: {calculations.get('system_capacity_kw', 'N/A')} kW
            - Capacity Factor: {calculations.get('capacity_factor', 'N/A')}%
            - Monthly Peak Production: {calculations.get('peak_month_production', 'N/A')} kWh

            FINANCIAL ANALYSIS:
            - Total Investment: €{calculations.get('total_investment', 'N/A')}
            - Annual Savings: €{calculations.get('annual_savings', 'N/A')}
            - Payback Period: {calculations.get('payback_period', 'N/A')} years
            - ROI: {calculations.get('roi_percentage', 'N/A')}%
            - CO2 Reduction: {calculations.get('co2_reduction', 'N/A')} tons/year

            REGULATORY & MARKET CONTEXT:
            {context_text}

            INSTRUCTIONS:
            1. Write in a professional but accessible tone for German homeowners
            2. Provide specific, actionable recommendations based on the data
            3. Include location-specific insights where possible
            4. Address potential concerns and risks
            5. Use the provided financial calculations exactly as given
            6. Structure with clear headings and bullet points
            7. Keep technical explanations simple but accurate

            Generate a comprehensive feasibility report covering:
            - Executive Summary with clear recommendation
            - Technical Feasibility Assessment
            - Financial Analysis and ROI breakdown
            - Environmental Impact
            - Regulatory Considerations and Incentives
            - Personalized Recommendations and Next Steps
            - Risk Assessment and Mitigation

            Write approximately 800-1000 words total.
            """

            return prompt

        def generate_basic_template_report(self, user_input: Dict, calculations: Dict) -> str:
            """Generate a basic template-based report when LLM is not available"""

            location = user_input.get('location', 'your location')
            roof_area = user_input.get('roof_area', 0)
            annual_kwh = calculations.get('annual_kwh', 0)
            total_investment = calculations.get('total_investment', 0)
            annual_savings = calculations.get('annual_savings', 0)
            payback_period = calculations.get('payback_period', 0)
            roi_percentage = calculations.get('roi_percentage', 0)
            co2_reduction = calculations.get('co2_reduction', 0)

            # Determine feasibility rating
            feasibility, recommendation = self._assess_feasibility(payback_period, roi_percentage)

            report = f"""
            # Solar Panel Investment Feasibility Report
            ## Location: {location}

            ### INFO: Executive Summary
            Your solar installation project shows **{feasibility}** feasibility. Based on our comprehensive analysis of your {roof_area}m² roof space in {location}, we {recommendation}.

            ### Technical Analysis
            - **Annual Energy Production**: {annual_kwh:,.0f} kWh
            - **System Capacity**: {calculations.get('system_capacity_kw', 0):.1f} kW
            - **Capacity Factor**: {calculations.get('capacity_factor', 0):.1f}%
            - **Peak Production Month**: {calculations.get('peak_month_production', 0):,.0f} kWh

            Your roof orientation ({user_input.get('orientation', 'south')}) is well-suited for solar energy generation in Germany.

            ### Financial Analysis
            - **Total Investment**: €{total_investment:,.0f}
            - **Annual Savings**: €{annual_savings:,.0f}
            - **Payback Period**: {payback_period:.1f} years
            - **Return on Investment**: {roi_percentage:.1f}%
            - **25-Year Net Savings**: €{calculations.get('total_lifetime_savings', 0) - total_investment:,.0f}

            ### Environmental Impact
            - **Annual CO2 Reduction**: {co2_reduction:.1f} tons
            - **25-Year CO2 Reduction**: {co2_reduction * 25:.1f} tons
            - **Equivalent to**: Planting {int(co2_reduction * 45)} trees annually

            ### Regulatory Advantages (2025)
            - **Zero VAT**: No additional tax on solar installations since 2023
            - **Feed-in Tariff**: €0.082/kWh for surplus electricity
            - **KfW Financing**: Low-interest loans available up to €50,000
            - **Simplified Process**: Streamlined approval for systems under 30kW

            ### INFO: Key Recommendations

            **Immediate Actions:**
            1. Obtain detailed roof assessment from certified installer
            2. Apply for KfW financing to reduce upfront costs
            3. Register installation with local grid operator
            4. Consider battery storage for increased self-consumption

            **Optimization Opportunities:**
            - Current self-consumption rate: ~30%
            - Potential improvement with battery storage: up to 70%
            - Smart home integration can increase efficiency by 10-15%

            **Timeline:**
            - Planning and permits: 4-6 weeks
            - Installation: 1-2 days
            - Grid connection: 2-4 weeks
            - Full operation: 6-12 weeks from contract

            ### WARNING: Important Considerations
            - Weather variability can affect actual production by ±15%
            - Regular maintenance required every 2-3 years
            - Insurance coverage recommended for weather damage
            - Monitor performance to ensure optimal operation

            ### Next Steps
            1. Contact certified installers for detailed quotes
            2. Schedule roof structural assessment
            3. Apply for financing if needed
            4. Begin permit application process

            This analysis is based on current German regulations and market conditions. Consult with local experts for site-specific recommendations.
            """

            return report.strip()

        def generate_enhanced_template_report(self, user_input: Dict, calculations: Dict, policy_context: List[str]) -> str:
            """Generate an enhanced template-based report with policy context"""

            location = user_input.get('location', 'your location')
            roof_area = user_input.get('roof_area', 0)
            annual_kwh = calculations.get('annual_kwh', 0)
            total_investment = calculations.get('total_investment', 0)
            annual_savings = calculations.get('annual_savings', 0)
            payback_period = calculations.get('payback_period', 0)
            roi_percentage = calculations.get('roi_percentage', 0)
            co2_reduction = calculations.get('co2_reduction', 0)

            # Determine feasibility rating
            feasibility, recommendation, confidence = self._assess_detailed_feasibility(payback_period, roi_percentage)

            # Extract relevant information from policy context
            policy_summary = self._extract_policy_highlights(policy_context)

            report = f"""
            # Solar Panel Investment Feasibility Report
            ## Location: {location}

            ### INFO: Executive Summary
            Your solar installation project shows **{feasibility}** feasibility with **{confidence} confidence**. Based on our comprehensive analysis of your {roof_area}m² roof space in {location}, we {recommendation}.

            **Key Metrics:**
            - **Investment**: €{total_investment:,.0f}
            - **Annual Production**: {annual_kwh:,.0f} kWh
            - **Payback Period**: {payback_period:.1f} years
            - **ROI**: {roi_percentage:.1f}% annually

            ### Technical Analysis
            - **Annual Energy Production**: {annual_kwh:,.0f} kWh
            - **System Capacity**: {calculations.get('system_capacity_kw', 0):.1f} kW
            - **Capacity Factor**: {calculations.get('capacity_factor', 0):.1f}%
            - **Peak Production Month**: {calculations.get('peak_month_production', 0):,.0f} kWh
            - **Daily Average Production**: {annual_kwh/365:.1f} kWh

            Your roof orientation ({user_input.get('orientation', 'south')}) is well-suited for solar energy generation in Germany. The system size is optimized for your available roof space.

            ### Financial Analysis
            - **Total Investment**: €{total_investment:,.0f}
            - **Annual Savings**: €{annual_savings:,.0f}
            - **Payback Period**: {payback_period:.1f} years
            - **Return on Investment**: {roi_percentage:.1f}%
            - **25-Year Net Profit**: €{calculations.get('total_lifetime_savings', 0) - total_investment:,.0f}
            - **Monthly Savings**: €{annual_savings/12:.0f}

            ### Environmental Impact
            - **Annual CO2 Reduction**: {co2_reduction:.1f} tons
            - **25-Year CO2 Reduction**: {co2_reduction * 25:.1f} tons
            - **Equivalent to**: Planting {int(co2_reduction * 45)} trees annually
            - **Car Emissions Offset**: {co2_reduction * 1000 / 4.6:.0f} km of driving per year

            ### Current Policy Benefits (2025)
            Based on retrieved policy data:
            {policy_summary}

            ### INFO: Personalized Recommendations

            **Priority Actions:**
            1. **Installer Selection**: Get quotes from at least 3 certified installers
            2. **Financing**: {"Apply for KfW loan to reduce upfront costs" if total_investment > 15000 else "Consider self-financing for better ROI"}
            3. **Grid Connection**: Register with local grid operator early
            4. **Battery Storage**: {"Highly recommended" if annual_savings > 1500 else "Consider for future upgrade"}

            **Optimization Opportunities:**
            - Current self-consumption rate: ~30%
            - Potential with battery storage: up to 70%
            - Smart home integration: additional 10-15% efficiency
            - {"East-west orientation might yield better results" if user_input.get('orientation') == 'south' else "Current orientation is optimal"}

            **Installation Timeline:**
            - Planning and permits: 4-6 weeks
            - Equipment procurement: 2-3 weeks
            - Installation: 1-2 days
            - Grid connection: 2-4 weeks
            - **Total timeline**: 8-15 weeks from contract

            ### WARNING: Risk Assessment

            **Weather Risks**: {"Low - consistent German weather patterns" if roi_percentage > 6 else "Moderate - consider weather insurance"}
            **Technology Risks**: Low - mature technology with 25-year warranties
            **Financial Risks**: {"Low" if payback_period < 15 else "Moderate"} - {"stable returns expected" if roi_percentage > 5 else "monitor energy prices"}
            **Regulatory Risks**: Low - German solar policies are stable

            ### Next Steps
            1. **Immediate**: Contact local installers for detailed site assessment
            2. **Week 1**: Apply for financing and permits
            3. **Week 2-4**: Compare detailed quotes and select installer
            4. **Month 2-3**: Installation and grid connection
            5. **Ongoing**: Monitor performance and maintain system

            ### Performance Monitoring
            - Expected monthly production range: {annual_kwh/12*0.3:.0f}-{annual_kwh/12*1.7:.0f} kWh
            - First-year degradation: <1%
            - Annual performance degradation: 0.5-0.8%
            - Warranty period: 25 years (80% performance guarantee)

            ---
            *This enhanced report combines accurate calculations with retrieved policy data for personalized recommendations. Generated on {location} analysis with {confidence} confidence level.*
            """

            return report.strip()

        def _assess_feasibility(self, payback_period: float, roi_percentage: float) -> tuple:
            """Assess project feasibility and return rating and recommendation"""
            if payback_period <= 10 and roi_percentage >= 8:
                return "EXCELLENT", "strongly recommend proceeding"
            elif payback_period <= 15 and roi_percentage >= 5:
                return "GOOD", "recommend proceeding"
            elif payback_period <= 20:
                return "MODERATE", "consider proceeding with careful evaluation"
            else:
                return "CHALLENGING", "suggest waiting for better conditions"

        def _assess_detailed_feasibility(self, payback_period: float, roi_percentage: float) -> tuple:
            """Assess project feasibility with detailed confidence rating"""
            if payback_period <= 10 and roi_percentage >= 8:
                return "EXCELLENT", "strongly recommend proceeding", "high"
            elif payback_period <= 15 and roi_percentage >= 5:
                return "GOOD", "recommend proceeding", "good"
            elif payback_period <= 20:
                return "MODERATE", "consider proceeding with careful evaluation", "moderate"
            else:
                return "CHALLENGING", "suggest waiting for better conditions", "low"

        def _extract_policy_highlights(self, policy_context: List[str]) -> str:
            """Extract key policy information from context documents"""
            highlights = []

            for doc in policy_context[:3]: # Use top 3 most relevant documents
                if "KfW" in doc or "financing" in doc.lower():
                    highlights.append(f"- {doc.strip()}")
                elif "VAT" in doc or "tax" in doc.lower():
                    highlights.append(f"- {doc.strip()}")
                elif "feed-in" in doc.lower() or "tariff" in doc.lower():
                    highlights.append(f"- {doc.strip()}")

            if not highlights:
                # Default policy information
                highlights = [
                "- Zero VAT on solar installations since 2023",
                "- Feed-in tariff €0.082/kWh for surplus electricity",
                "- KfW financing available up to €50,000"
                ]

                return "\n".join(highlights)

        def generate_fallback_report(self, user_input: Dict, calculations: Dict, error_message: str) -> str:
            """Generate a fallback report when all other methods fail"""
            return f"""
            # Solar Panel Feasibility Report

            ## Analysis Results
            - Location: {user_input.get('location', 'N/A')}
            - Annual Production: {calculations.get('annual_kwh', 0):,.0f} kWh
            - Investment Required: €{calculations.get('total_investment', 0):,.0f}
            - Annual Savings: €{calculations.get('annual_savings', 0):,.0f}
            - Payback Period: {calculations.get('payback_period', 0):.1f} years
            - ROI: {calculations.get('roi_percentage', 0):.1f}%

            ## Status
            Analysis completed with basic template due to system limitations.
            For detailed reports, please contact a solar energy consultant.

            Error details: {error_message}
            """
