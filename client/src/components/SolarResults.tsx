import React from 'react';
import {
    Card,
    CardContent,
    Typography,
    Box,
    Chip,
    LinearProgress,
    Button,
    useTheme,
    alpha,
} from '@mui/material';
import Grid from '@mui/material/Grid';
import {
    SolarPower,
    TrendingUp,
    CalendarMonth,
    ElectricBolt,
    Home,
    WbSunny,
    Speed,
    ArrowForward,
    ArrowBack,
    Insights
} from '@mui/icons-material';

interface SolarResultsProps {
    data: any;
    results: any;
    onNext: () => void;
    onBack: () => void;
}

const SolarResults: React.FC<SolarResultsProps> = ({ data, results, onNext, onBack }) => {
    const theme = useTheme();

    if (!results) {
        return (
            <Card sx={{ p: 4, textAlign: 'center' }}>
                <CardContent>
                    <SolarPower sx={{ fontSize: 48, color: 'primary.main', mb: 2 }} />
                    <Typography variant="h6">Analyzing your solar potential...</Typography>
                    <LinearProgress sx={{ mt: 2, width: '200px', mx: 'auto' }} />
                </CardContent>
            </Card>
        );
    }

    const monthNames = [
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
    ];

    const formatNumber = (num: number, decimals = 0) => num?.toFixed(decimals);
    const maxProduction = Math.max(...(results.monthly_production || []));

    // Calculate efficiency metrics
    const dailyAverage = results.annual_kwh / 365;
    const systemCapacity = results.system_capacity_kw || (data?.roofArea * 0.15); // Estimate if not provided
    const capacityFactor = ((results.annual_kwh || 0) / (systemCapacity * 8760)) * 100;

    return (
        <Box>
            {/* Header */}
            <Box sx={{ mb: 4 }}>
                <Typography
                    variant="h3"
                    gutterBottom
                    sx={{
                        display: 'flex',
                        alignItems: 'center',
                        fontWeight: 600,
                        color: 'primary.main'
                    }}
                >
                    <WbSunny sx={{ mr: 2, fontSize: 40 }} />
                    Solar Analysis Results
                </Typography>
                <Typography variant="h6" color="text.secondary" sx={{ mb: 3 }}>
                    Comprehensive analysis for your {data?.location} property
                </Typography>
            </Box>

            {/* Key Metrics Cards */}
            <Grid container spacing={3} sx={{ mb: 4 }}>
                <Grid item xs={12} sm={6} md={3}>
                    <Card
                        sx={{
                            p: 3,
                            textAlign: 'center',
                            background: `linear-gradient(135deg, ${theme.palette.primary.main} 0%, ${theme.palette.primary.dark} 100%)`,
                            color: 'white',
                            borderRadius: 3,
                            boxShadow: '0 8px 32px rgba(46, 125, 50, 0.3)'
                        }}
                    >
                        <ElectricBolt sx={{ fontSize: 48, mb: 2, opacity: 0.9 }} />
                        <Typography variant="h3" sx={{ fontWeight: 700, mb: 1 }}>
                            {formatNumber(results.annual_kwh, 0)}
                        </Typography>
                        <Typography variant="h6" sx={{ opacity: 0.9 }}>
                            kWh/year
                        </Typography>
                        <Typography variant="body2" sx={{ mt: 1, opacity: 0.8 }}>
                            Annual Production
                        </Typography>
                    </Card>
                </Grid>

                <Grid item xs={12} sm={6} md={3}>
                    <Card
                        sx={{
                            p: 3,
                            textAlign: 'center',
                            background: `linear-gradient(135deg, ${theme.palette.secondary.main} 0%, ${theme.palette.secondary.dark} 100%)`,
                            color: 'white',
                            borderRadius: 3,
                            boxShadow: '0 8px 32px rgba(255, 167, 38, 0.3)'
                        }}
                    >
                        <Speed sx={{ fontSize: 48, mb: 2, opacity: 0.9 }} />
                        <Typography variant="h3" sx={{ fontWeight: 700, mb: 1 }}>
                            {formatNumber(systemCapacity, 1)}
                        </Typography>
                        <Typography variant="h6" sx={{ opacity: 0.9 }}>
                            kW
                        </Typography>
                        <Typography variant="body2" sx={{ mt: 1, opacity: 0.8 }}>
                            System Capacity
                        </Typography>
                    </Card>
                </Grid>

                <Grid item xs={12} sm={6} md={3}>
                    <Card
                        sx={{
                            p: 3,
                            textAlign: 'center',
                            background: `linear-gradient(135deg, ${theme.palette.success.main} 0%, ${theme.palette.success.dark} 100%)`,
                            color: 'white',
                            borderRadius: 3,
                            boxShadow: '0 8px 32px rgba(76, 175, 80, 0.3)'
                        }}
                    >
                        <TrendingUp sx={{ fontSize: 48, mb: 2, opacity: 0.9 }} />
                        <Typography variant="h3" sx={{ fontWeight: 700, mb: 1 }}>
                            {formatNumber(dailyAverage, 1)}
                        </Typography>
                        <Typography variant="h6" sx={{ opacity: 0.9 }}>
                            kWh/day
                        </Typography>
                        <Typography variant="body2" sx={{ mt: 1, opacity: 0.8 }}>
                            Daily Average
                        </Typography>
                    </Card>
                </Grid>

                <Grid item xs={12} sm={6} md={3}>
                    <Card
                        sx={{
                            p: 3,
                            textAlign: 'center',
                            background: `linear-gradient(135deg, ${theme.palette.info.main} 0%, ${theme.palette.info.dark} 100%)`,
                            color: 'white',
                            borderRadius: 3,
                            boxShadow: '0 8px 32px rgba(33, 150, 243, 0.3)'
                        }}
                    >
                        <Insights sx={{ fontSize: 48, mb: 2, opacity: 0.9 }} />
                        <Typography variant="h3" sx={{ fontWeight: 700, mb: 1 }}>
                            {formatNumber(capacityFactor, 1)}%
                        </Typography>
                        <Typography variant="h6" sx={{ opacity: 0.9 }}>
                            Efficiency
                        </Typography>
                        <Typography variant="body2" sx={{ mt: 1, opacity: 0.8 }}>
                            Capacity Factor
                        </Typography>
                    </Card>
                </Grid>
            </Grid>

            {/* System Overview */}
            <Card sx={{ mb: 4, borderRadius: 3, overflow: 'hidden' }}>
                <CardContent sx={{ p: 0 }}>
                    <Box sx={{
                        p: 3,
                        background: `linear-gradient(90deg, ${alpha(theme.palette.primary.main, 0.1)} 0%, ${alpha(theme.palette.secondary.main, 0.1)} 100%)`,
                        borderBottom: 1,
                        borderColor: 'divider'
                    }}>
                        <Typography variant="h5" sx={{ display: 'flex', alignItems: 'center', fontWeight: 600 }}>
                            <Home sx={{ mr: 1, color: 'primary.main' }} />
                            System Overview
                        </Typography>
                    </Box>
                    <Box sx={{ p: 3 }}>
                        <Grid container spacing={3}>
                            <Grid item xs={12} md={6}>
                                <Box sx={{ mb: 3 }}>
                                    <Typography variant="subtitle1" gutterBottom sx={{ fontWeight: 600, color: 'primary.main' }}>
                                        Installation Details
                                    </Typography>
                                    <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                                        <Typography variant="body2" color="text.secondary">Location:</Typography>
                                        <Typography variant="body2" sx={{ fontWeight: 500 }}>{data?.location}</Typography>
                                    </Box>
                                    <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                                        <Typography variant="body2" color="text.secondary">Roof Area:</Typography>
                                        <Typography variant="body2" sx={{ fontWeight: 500 }}>{data?.roofArea} m²</Typography>
                                    </Box>
                                    <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                                        <Typography variant="body2" color="text.secondary">Orientation:</Typography>
                                        <Typography variant="body2" sx={{ fontWeight: 500 }}>
                                            {data?.orientation?.charAt(0).toUpperCase() + data?.orientation?.slice(1)}
                                        </Typography>
                                    </Box>
                                    <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                                        <Typography variant="body2" color="text.secondary">Weather Analysis:</Typography>
                                        <Chip
                                            label={data?.weatherAnalysis?.charAt(0).toUpperCase() + data?.weatherAnalysis?.slice(1)}
                                            size="small"
                                            color="primary"
                                            variant="outlined"
                                        />
                                    </Box>
                                </Box>
                            </Grid>
                            <Grid item xs={12} md={6}>
                                <Box>
                                    <Typography variant="subtitle1" gutterBottom sx={{ fontWeight: 600, color: 'secondary.main' }}>
                                        Performance Metrics
                                    </Typography>
                                    <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                                        <Typography variant="body2" color="text.secondary">Peak Month:</Typography>
                                        <Typography variant="body2" sx={{ fontWeight: 500 }}>
                                            {formatNumber(results.peak_month_production, 0)} kWh
                                        </Typography>
                                    </Box>
                                    <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                                        <Typography variant="body2" color="text.secondary">Annual Consumption:</Typography>
                                        <Typography variant="body2" sx={{ fontWeight: 500 }}>{data?.annualConsumption} kWh</Typography>
                                    </Box>
                                    <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                                        <Typography variant="body2" color="text.secondary">Coverage:</Typography>
                                        <Typography variant="body2" sx={{ fontWeight: 500 }}>
                                            {formatNumber((results.annual_kwh / data?.annualConsumption) * 100, 1)}%
                                        </Typography>
                                    </Box>
                                    <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                                        <Typography variant="body2" color="text.secondary">Capacity Factor:</Typography>
                                        <Typography variant="body2" sx={{ fontWeight: 500 }}>{formatNumber(capacityFactor, 1)}%</Typography>
                                    </Box>
                                </Box>
                            </Grid>
                        </Grid>
                    </Box>
                </CardContent>
            </Card>

            {/* Monthly Production Breakdown */}
            <Card sx={{ mb: 4, borderRadius: 3, overflow: 'hidden' }}>
                <CardContent sx={{ p: 0 }}>
                    <Box sx={{
                        p: 3,
                        background: `linear-gradient(90deg, ${alpha(theme.palette.success.main, 0.1)} 0%, ${alpha(theme.palette.info.main, 0.1)} 100%)`,
                        borderBottom: 1,
                        borderColor: 'divider'
                    }}>
                        <Typography variant="h5" sx={{ display: 'flex', alignItems: 'center', fontWeight: 600 }}>
                            <CalendarMonth sx={{ mr: 1, color: 'success.main' }} />
                            Monthly Production Breakdown
                        </Typography>
                        <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                            Expected solar energy generation throughout the year
                        </Typography>
                    </Box>
                    <Box sx={{ p: 3 }}>
                        <Grid container spacing={2}>
                            {results.monthly_production?.map((production: number, index: number) => {
                                const percentage = (production / maxProduction) * 100;
                                const isHighProduction = percentage > 70;
                                const isMediumProduction = percentage > 40;

                                return (
                                    <Grid item xs={6} sm={4} md={3} lg={2} key={index}>
                                        <Card
                                            sx={{
                                                p: 2,
                                                textAlign: 'center',
                                                border: 1,
                                                borderColor: isHighProduction ? 'success.main' :
                                                    isMediumProduction ? 'warning.main' : 'grey.300',
                                                bgcolor: isHighProduction ? alpha(theme.palette.success.main, 0.05) :
                                                    isMediumProduction ? alpha(theme.palette.warning.main, 0.05) :
                                                        alpha(theme.palette.grey[500], 0.05),
                                                transition: 'all 0.3s ease',
                                                '&:hover': {
                                                    transform: 'translateY(-4px)',
                                                    boxShadow: 4
                                                }
                                            }}
                                        >
                                            <Typography
                                                variant="subtitle2"
                                                gutterBottom
                                                sx={{
                                                    fontWeight: 600,
                                                    color: isHighProduction ? 'success.main' :
                                                        isMediumProduction ? 'warning.main' : 'text.secondary'
                                                }}
                                            >
                                                {monthNames[index]}
                                            </Typography>
                                            <Typography
                                                variant="h6"
                                                sx={{
                                                    fontWeight: 700,
                                                    color: isHighProduction ? 'success.main' :
                                                        isMediumProduction ? 'warning.main' : 'primary.main'
                                                }}
                                            >
                                                {formatNumber(production, 0)}
                                            </Typography>
                                            <Typography variant="caption" color="text.secondary">
                                                kWh
                                            </Typography>
                                            <LinearProgress
                                                variant="determinate"
                                                value={percentage}
                                                sx={{
                                                    mt: 1,
                                                    height: 4,
                                                    borderRadius: 2,
                                                    bgcolor: alpha(theme.palette.grey[300], 0.3),
                                                    '& .MuiLinearProgress-bar': {
                                                        bgcolor: isHighProduction ? 'success.main' :
                                                            isMediumProduction ? 'warning.main' : 'primary.main'
                                                    }
                                                }}
                                            />
                                        </Card>
                                    </Grid>
                                );
                            })}
                        </Grid>
                    </Box>
                </CardContent>
            </Card>

            {/* Navigation */}
            <Box sx={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                mt: 4,
                p: 3,
                bgcolor: alpha(theme.palette.primary.main, 0.05),
                borderRadius: 2,
                border: 1,
                borderColor: 'divider'
            }}>
                <Button
                    variant="outlined"
                    startIcon={<ArrowBack />}
                    onClick={onBack}
                    size="large"
                    sx={{
                        px: 4,
                        py: 1.5,
                        borderRadius: 2,
                        textTransform: 'none',
                        fontWeight: 600
                    }}
                >
                    Back to Input
                </Button>

                <Box sx={{ textAlign: 'center' }}>
                    <Typography variant="body2" color="text.secondary" gutterBottom>
                        Ready for financial analysis?
                    </Typography>
                    <Typography variant="caption" color="text.secondary">
                        Next: Complete ROI and investment analysis
                    </Typography>
                </Box>

                <Button
                    variant="contained"
                    endIcon={<ArrowForward />}
                    onClick={onNext}
                    size="large"
                    sx={{
                        px: 4,
                        py: 1.5,
                        borderRadius: 2,
                        textTransform: 'none',
                        fontWeight: 600,
                        boxShadow: 3
                    }}
                >
                    Continue to ROI Analysis
                </Button>
            </Box>
        </Box>
    );
};

export default SolarResults;
