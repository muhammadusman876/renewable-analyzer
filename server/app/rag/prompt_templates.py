"""
LangChain Prompt Templates for Solar Analysis
"""

# Solar Analysis Template
SOLAR_ANALYSIS_TEMPLATE = """
You are an expert solar energy consultant specializing in the German renewable energy market.

Context Information:
{context}

Analysis Request:
Location: {location}
Roof Area: {roof_area} square meters
Orientation: {orientation}
Budget: €{budget}
Annual Consumption: {consumption} kWh
Weather Analysis Type: {weather_analysis}

Please provide a comprehensive analysis including:
1. Solar potential assessment for this specific location
2. Financial feasibility and ROI calculation
3. Payback period estimation
4. Specific recommendations for German market conditions
5. Consideration of local regulations and incentives

Keep the analysis practical, data-driven, and specific to German solar market conditions.

Analysis:
"""

# Weather Impact Template
WEATHER_ANALYSIS_TEMPLATE = """
Analyze the weather impact on solar energy potential:

Weather Data Summary:
{weather_data}

Location: {location}
Analysis Type: {analysis_type}

Provide insights on:
1. Solar irradiance potential based on weather patterns
2. Seasonal variations and their impact
3. Expected energy production variations
4. Optimal installation recommendations

Weather Impact Analysis:
"""

# ROI Calculation Template
ROI_CALCULATION_TEMPLATE = """
Calculate detailed Return on Investment for this solar installation in Germany:

Investment Parameters:
- Total Budget: €{budget}
- System Size: {system_size} kWp
- Annual Production: {annual_production} kWh
- Current Electricity Price: €{electricity_price}/kWh
- Feed-in Tariff: €{feed_in_tariff}/kWh
- Annual Consumption: {consumption} kWh

Calculate and explain:
1. Annual electricity cost savings
2. Feed-in tariff revenue
3. Total annual financial benefit
4. Simple payback period
5. 20-year net present value
6. German tax benefits and incentives

Provide detailed financial breakdown with clear calculations.

ROI Analysis:
"""

# Policy and Regulations Template
POLICY_ANALYSIS_TEMPLATE = """
Analyze German renewable energy policies and regulations relevant to this solar installation:

Installation Details:
- Location: {location}
- System Size: {system_size} kWp
- Installation Type: Residential/Commercial

Policy Context:
{policy_context}

Analyze:
1. Current German feed-in tariff rates
2. Net metering regulations
3. Local building permits and requirements
4. Available subsidies and incentives
5. Tax implications and benefits
6. Grid connection requirements

Policy Recommendations:
"""

# Feasibility Report Template
FEASIBILITY_REPORT_TEMPLATE = """
Generate a comprehensive feasibility report for this solar installation project:

Project Overview:
- Location: {location}
- System Size: {system_size} kWp
- Total Investment: €{budget}
- Roof Area: {roof_area} m²
- Annual Consumption: {consumption} kWh

Technical Analysis:
{technical_analysis}

Financial Analysis:
{financial_analysis}

Create a structured report with:
1. Executive Summary
2. Technical Feasibility Assessment
3. Financial Analysis and ROI
4. Risk Assessment
5. Implementation Timeline
6. Recommendations

Format as a professional feasibility study suitable for investment decision-making.

Feasibility Report:
"""
