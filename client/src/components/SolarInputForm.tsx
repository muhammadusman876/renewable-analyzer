import React, { useState } from 'react';
import {
    Card,
    CardContent,
    TextField,
    Typography,
    FormControl,
    InputLabel,
    Select,
    MenuItem,
    Box,
    InputAdornment,
    Alert,
    Button,
    CircularProgress,
} from '@mui/material';
import { LocationOn, Home, Navigation, ElectricBolt } from '@mui/icons-material';

interface SolarInputFormProps {
    onCalculate: (data: any) => void;
    loading: boolean;
}

const SolarInputForm: React.FC<SolarInputFormProps> = ({ onCalculate, loading }) => {
    const [formData, setFormData] = useState({
        location: 'Berlin',
        roofArea: '',
        orientation: 'south',
        weatherAnalysis: 'hybrid',
        annualConsumption: '',
        budget: '',
    });

    const [errors, setErrors] = useState<Record<string, string>>({});

    const germanCities = [
        'Berlin', 'Munich', 'Hamburg', 'Cologne', 'Frankfurt', 'Stuttgart',
        'Düsseldorf', 'Dortmund', 'Essen', 'Leipzig', 'Bremen', 'Dresden',
        'Hanover', 'Nuremberg', 'Duisburg', 'Bochum', 'Wuppertal', 'Bonn'
    ];

    const orientations = [
        { value: 'south', label: 'South (Optimal)', factor: '100%' },
        { value: 'southeast', label: 'South-East', factor: '95%' },
        { value: 'southwest', label: 'South-West', factor: '95%' },
        { value: 'east', label: 'East', factor: '85%' },
        { value: 'west', label: 'West', factor: '85%' },
        { value: 'northeast', label: 'North-East', factor: '75%' },
        { value: 'northwest', label: 'North-West', factor: '75%' },
        { value: 'north', label: 'North', factor: '60%' },
    ];

    const weatherAnalysisOptions = [
        {
            value: 'latest',
            label: '⚡ Recent Weather',
            description: 'Last 30 days - quick analysis',
            timeframe: '30 days'
        },
        {
            value: 'historical',
            label: '📊 Long-term Average',
            description: '5+ years - comprehensive analysis',
            timeframe: '5+ years'
        },
        {
            value: 'hybrid',
            label: '🎯 Smart Analysis (Recommended)',
            description: 'Recent + historical - most accurate',
            timeframe: '30 days + 5 years'
        },
    ];

    const handleInputChange = (field: string, value: string) => {
        setFormData(prev => ({
            ...prev,
            [field]: value
        }));
        if (errors[field]) {
            setErrors(prev => ({
                ...prev,
                [field]: ''
            }));
        }
    };

    const validateForm = () => {
        const newErrors: Record<string, string> = {};

        if (!formData.roofArea || parseFloat(formData.roofArea) <= 0) {
            newErrors.roofArea = 'Please enter a valid roof area';
        } else if (parseFloat(formData.roofArea) > 1000) {
            newErrors.roofArea = 'Roof area seems too large (max 1000 m²)';
        }

        if (!formData.annualConsumption || parseFloat(formData.annualConsumption) <= 0) {
            newErrors.annualConsumption = 'Please enter a valid annual consumption';
        } else if (parseFloat(formData.annualConsumption) > 50000) {
            newErrors.annualConsumption = 'Consumption seems too high (max 50,000 kWh)';
        }

        if (!formData.budget || parseFloat(formData.budget) <= 0) {
            newErrors.budget = 'Please enter a valid budget';
        } else if (parseFloat(formData.budget) < 5000) {
            newErrors.budget = 'Budget too low for solar installation (min €5,000)';
        } else if (parseFloat(formData.budget) > 200000) {
            newErrors.budget = 'Budget seems too high (max €200,000)';
        }

        setErrors(newErrors);
        return Object.keys(newErrors).length === 0;
    };

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (validateForm()) {
            onCalculate({
                location: formData.location,
                roofArea: parseFloat(formData.roofArea),
                orientation: formData.orientation,
                weatherAnalysis: formData.weatherAnalysis,
                annualConsumption: parseFloat(formData.annualConsumption),
                budget: parseFloat(formData.budget),
            });
        }
    };

    return (
        <Card sx={{ maxWidth: 800, mx: 'auto' }}>
            <CardContent sx={{ p: 4 }}>
                <Typography variant="h5" gutterBottom sx={{ mb: 3, display: 'flex', alignItems: 'center' }}>
                    <Home sx={{ mr: 1 }} />
                    Property Details
                </Typography>

                <Alert severity="info" sx={{ mb: 3 }}>
                    Choose your weather analysis method: Recent data for current conditions, Historical for long-term patterns, or Smart Analysis (recommended) for the most accurate results.
                </Alert>

                <form onSubmit={handleSubmit}>
                    <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
                        <Box sx={{ display: 'flex', gap: 2 }}>
                            <FormControl sx={{ flex: 1 }}>
                                <InputLabel>Location</InputLabel>
                                <Select
                                    value={formData.location}
                                    label="Location"
                                    onChange={(e) => handleInputChange('location', e.target.value)}
                                    startAdornment={
                                        <InputAdornment position="start">
                                            <LocationOn />
                                        </InputAdornment>
                                    }
                                >
                                    {germanCities.map((city) => (
                                        <MenuItem key={city} value={city}>
                                            {city}
                                        </MenuItem>
                                    ))}
                                </Select>
                            </FormControl>

                            <TextField
                                sx={{ flex: 1 }}
                                label="Available Roof Area"
                                value={formData.roofArea}
                                onChange={(e) => handleInputChange('roofArea', e.target.value)}
                                error={!!errors.roofArea}
                                helperText={errors.roofArea || 'Usable roof space for solar panels'}
                                InputProps={{
                                    startAdornment: (
                                        <InputAdornment position="start">
                                            <Home />
                                        </InputAdornment>
                                    ),
                                    endAdornment: (
                                        <InputAdornment position="end">m²</InputAdornment>
                                    ),
                                }}
                                type="number"
                                inputProps={{ min: 0, max: 1000, step: 0.1 }}
                            />
                        </Box>

                        <FormControl>
                            <InputLabel>Roof Orientation</InputLabel>
                            <Select
                                value={formData.orientation}
                                label="Roof Orientation"
                                onChange={(e) => handleInputChange('orientation', e.target.value)}
                                startAdornment={
                                    <InputAdornment position="start">
                                        <Navigation />
                                    </InputAdornment>
                                }
                            >
                                {orientations.map((orientation) => (
                                    <MenuItem key={orientation.value} value={orientation.value}>
                                        <Box sx={{ display: 'flex', justifyContent: 'space-between', width: '100%' }}>
                                            <span>{orientation.label}</span>
                                            <span style={{ color: 'text.secondary', fontSize: '0.875rem' }}>
                                                {orientation.factor}
                                            </span>
                                        </Box>
                                    </MenuItem>
                                ))}
                            </Select>
                        </FormControl>

                        <FormControl>
                            <InputLabel>Weather Analysis Method</InputLabel>
                            <Select
                                value={formData.weatherAnalysis}
                                label="Weather Analysis Method"
                                onChange={(e) => handleInputChange('weatherAnalysis', e.target.value)}
                                startAdornment={
                                    <InputAdornment position="start">
                                        🌤️
                                    </InputAdornment>
                                }
                            >
                                {weatherAnalysisOptions.map((option) => (
                                    <MenuItem key={option.value} value={option.value}>
                                        <Box sx={{ display: 'flex', flexDirection: 'column', width: '100%' }}>
                                            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                                                <span>{option.label}</span>
                                                <span style={{ color: 'text.secondary', fontSize: '0.75rem' }}>
                                                    {option.timeframe}
                                                </span>
                                            </Box>
                                            <Typography variant="caption" color="text.secondary" sx={{ mt: 0.5 }}>
                                                {option.description}
                                            </Typography>
                                        </Box>
                                    </MenuItem>
                                ))}
                            </Select>
                        </FormControl>

                        <TextField
                            label="Annual Electricity Consumption"
                            value={formData.annualConsumption}
                            onChange={(e) => handleInputChange('annualConsumption', e.target.value)}
                            error={!!errors.annualConsumption}
                            helperText={errors.annualConsumption || 'Your yearly electricity usage (typical German household: 2,500-4,000 kWh)'}
                            InputProps={{
                                startAdornment: (
                                    <InputAdornment position="start">
                                        <ElectricBolt />
                                    </InputAdornment>
                                ),
                                endAdornment: (
                                    <InputAdornment position="end">kWh/year</InputAdornment>
                                ),
                            }}
                            type="number"
                            inputProps={{ min: 0, max: 50000, step: 100 }}
                        />

                        <TextField
                            label="Budget for Solar Installation"
                            value={formData.budget}
                            onChange={(e) => handleInputChange('budget', e.target.value)}
                            error={!!errors.budget}
                            helperText={errors.budget || 'Available budget for solar panels and installation (typical range: €15,000-€50,000)'}
                            InputProps={{
                                startAdornment: (
                                    <InputAdornment position="start">
                                        €
                                    </InputAdornment>
                                ),
                                endAdornment: (
                                    <InputAdornment position="end">EUR</InputAdornment>
                                ),
                            }}
                            type="number"
                            inputProps={{ min: 5000, max: 200000, step: 1000 }}
                        />

                        <Box sx={{ display: 'flex', justifyContent: 'center', mt: 2 }}>
                            <Button
                                type="submit"
                                variant="contained"
                                size="large"
                                disabled={loading}
                                startIcon={loading ? <CircularProgress size={20} /> : <ElectricBolt />}
                                sx={{ px: 4, py: 1.5 }}
                            >
                                {loading ? 'Calculating...' : 'Calculate Solar Potential'}
                            </Button>
                        </Box>
                    </Box>
                </form>
            </CardContent>
        </Card>
    );
};

export default SolarInputForm;
