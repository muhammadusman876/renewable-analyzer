import React, { useState } from 'react';
import {
    Container,
    Typography,
    Box,
    Card,
    CardContent,
    Stepper,
    Step,
    StepLabel,
} from '@mui/material';
import { SolarPower, Analytics, Euro } from '@mui/icons-material';

import SolarInputForm from './SolarInputForm';
import SolarResults from './SolarResults';
import ROIAnalysis from './ROIAnalysis';
import SolarChart from './SolarChart';

interface SolarData {
    location: string;
    roofArea: number;
    orientation: string;
    weatherAnalysis: string;
    annualConsumption: number;
    budget: number;
}

interface CalculationResults {
    solar: any;
    roi: any;
}

const steps = ['Property Details', 'Solar Analysis', 'Investment Analysis'];

const Home: React.FC = () => {
    const [activeStep, setActiveStep] = useState(0);
    const [solarData, setSolarData] = useState<SolarData | null>(null);
    const [results, setResults] = useState<CalculationResults | null>(null);
    const [loading, setLoading] = useState(false);

    const handleCalculate = async (data: SolarData) => {
        setLoading(true);
        setSolarData(data);
        try {
            // Call backend for solar calculation with new weather_analysis parameter
            const res = await fetch('/api/analyze', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    location: data.location,
                    roof_area: data.roofArea,
                    orientation: data.orientation,
                    weather_analysis: data.weatherAnalysis,
                    budget: data.budget,
                }),
            });

            if (!res.ok) {
                throw new Error(`API error: ${res.status}`);
            }

            const result = await res.json();
            setResults({
                solar: result.solar_potential,
                roi: {
                    ...result.financial_analysis,
                    feasibility_report: result.feasibility_report,
                    recommendations: result.recommendations
                },
            });
            setActiveStep(1);
        } catch (error) {
            console.error('Calculation failed:', error);
            alert('Calculation failed. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    const handleNext = () => setActiveStep((s) => s + 1);
    const handleBack = () => setActiveStep((s) => s - 1);

    return (
        <Container maxWidth="lg" sx={{ py: 4 }}>
            <Box sx={{ mb: 4 }}>
                <Typography variant="h2" align="center" gutterBottom>
                    Solar Investment Calculator
                </Typography>
                <Typography variant="h6" align="center" color="text.secondary" sx={{ mb: 4 }}>
                    Analyze your solar potential with smart weather analysis: recent trends, historical patterns, or hybrid approach
                </Typography>

                <Stepper activeStep={activeStep} alternativeLabel sx={{ mb: 4 }}>
                    {steps.map((label, index) => (
                        <Step key={label}>
                            <StepLabel
                                StepIconComponent={({ active, completed }) => (
                                    <Box
                                        sx={{
                                            width: 40,
                                            height: 40,
                                            borderRadius: '50%',
                                            display: 'flex',
                                            alignItems: 'center',
                                            justifyContent: 'center',
                                            bgcolor: active || completed ? 'primary.main' : 'grey.300',
                                            color: active || completed ? 'white' : 'grey.600',
                                        }}
                                    >
                                        {index === 0 && <SolarPower />}
                                        {index === 1 && <Analytics />}
                                        {index === 2 && <Euro />}
                                    </Box>
                                )}
                            >
                                {label}
                            </StepLabel>
                        </Step>
                    ))}
                </Stepper>
            </Box>

            {activeStep === 0 && (
                <>
                    <SolarInputForm
                        onCalculate={handleCalculate}
                        loading={loading}
                    />

                    {/* Features Overview */}
                    <Box sx={{ display: 'flex', gap: 4, mt: 4 }}>
                        <Card sx={{ flex: 1 }}>
                            <CardContent sx={{ textAlign: 'center' }}>
                                <SolarPower sx={{ fontSize: 48, color: 'primary.main', mb: 2 }} />
                                <Typography variant="h6" gutterBottom>
                                    Real EDA Data
                                </Typography>
                                <Typography variant="body2" color="text.secondary">
                                    Calculations based on 12 years of German renewable energy data
                                </Typography>
                            </CardContent>
                        </Card>

                        <Card sx={{ flex: 1 }}>
                            <CardContent sx={{ textAlign: 'center' }}>
                                <Analytics sx={{ fontSize: 48, color: 'primary.main', mb: 2 }} />
                                <Typography variant="h6" gutterBottom>
                                    Smart Weather Analysis
                                </Typography>
                                <Typography variant="body2" color="text.secondary">
                                    Choose from recent trends, historical patterns, or hybrid analysis
                                </Typography>
                            </CardContent>
                        </Card>

                        <Card sx={{ flex: 1 }}>
                            <CardContent sx={{ textAlign: 'center' }}>
                                <Euro sx={{ fontSize: 48, color: 'primary.main', mb: 2 }} />
                                <Typography variant="h6" gutterBottom>
                                    Financial ROI
                                </Typography>
                                <Typography variant="body2" color="text.secondary">
                                    Complete investment analysis with German market rates
                                </Typography>
                            </CardContent>
                        </Card>
                    </Box>
                </>
            )}

            {activeStep === 1 && results && (
                <Box>
                    <SolarResults
                        data={solarData}
                        results={results.solar}
                        onNext={handleNext}
                        onBack={handleBack}
                    />
                    <SolarChart monthlyProduction={results.solar.monthly_production} />
                </Box>
            )}

            {activeStep === 2 && results && (
                <ROIAnalysis
                    data={solarData}
                    solarResults={results.solar}
                    roiResults={results.roi}
                    onBack={handleBack}
                />
            )}
        </Container>
    );
};

export default Home;
