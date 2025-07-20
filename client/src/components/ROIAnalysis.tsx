import React, { useRef, useState } from 'react';
import {
    Card,
    CardContent,
    Typography,
    Box,
    Button,
    Paper,
    Modal,
    IconButton,
    useTheme,
    alpha,
    Fade,
    Backdrop,
} from '@mui/material';
import { Grid } from '@mui/material';
import {
    Euro,
    ArrowBack,
    Print,
    TrendingUp,
    Schedule,
    ElectricBolt,
    Assignment,
    WbSunny,
    AttachMoney,
    Nature,
    Close,
    Article,
    Star
} from '@mui/icons-material';
import { useReactToPrint } from 'react-to-print';

interface ROIAnalysisProps {
    data: any;
    solarResults: any;
    roiResults: any;
    onBack: () => void;
}

const ROIAnalysis: React.FC<ROIAnalysisProps> = ({ data, solarResults, roiResults, onBack }) => {
    const printRef = useRef<HTMLDivElement>(null);
    const [modalOpen, setModalOpen] = useState(false);
    const theme = useTheme();

    const handlePrint = useReactToPrint({
        contentRef: printRef,
        documentTitle: `Solar Investment Report - ${data?.location || 'Analysis'}`,
    });

    if (!roiResults || !solarResults) {
        return (
            <Card>
                <CardContent>
                    <Typography>Loading comprehensive analysis...</Typography>
                </CardContent>
            </Card>
        );
    }

    const formatCurrency = (amount: number) => `€${amount?.toLocaleString('de-DE', { minimumFractionDigits: 2 })}`;
    const formatNumber = (num: number, decimals = 1) => num?.toFixed(decimals);

    const modalStyle = {
        position: 'absolute' as 'absolute',
        top: '50%',
        left: '50%',
        transform: 'translate(-50%, -50%)',
        width: '90vw',
        maxWidth: '1000px',
        height: '80vh',
        bgcolor: 'background.paper',
        borderRadius: 3,
        boxShadow: 24,
        p: 0,
        overflow: 'hidden',
    };

    return (
        <Box>
            {/* Header Actions */}
            <Box className="no-print" sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
                <Typography variant="h4" sx={{ display: 'flex', alignItems: 'center' }}>
                    <Euro sx={{ mr: 2, color: 'primary.main' }} />
                    Investment Analysis Report
                </Typography>
                <Box sx={{ display: 'flex', gap: 2 }}>
                    <Button
                        variant="contained"
                        startIcon={<Print />}
                        onClick={handlePrint}
                        sx={{ px: 3 }}
                    >
                        Print Report
                    </Button>
                    <Button
                        variant="outlined"
                        startIcon={<ArrowBack />}
                        onClick={onBack}
                    >
                        Back to Analysis
                    </Button>
                </Box>
            </Box>

            {/* Printable Content */}
            <div ref={printRef}>
                {/* Report Header */}
                <Paper sx={{ p: 3, mb: 3, bgcolor: 'primary.main', color: 'white', borderRadius: 2 }}>
                    <Typography variant="h4" gutterBottom>
                        Solar Investment Analysis Report
                    </Typography>
                    <Typography variant="h6">
                        Location: {data?.location} • Analysis Date: {new Date().toLocaleDateString('de-DE')}
                    </Typography>
                </Paper>

                {/* Executive Summary */}
                <Card sx={{ mb: 3, borderRadius: 2 }}>
                    <CardContent>
                        <Typography variant="h5" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
                            <Assignment sx={{ mr: 1, color: 'primary.main' }} />
                            Executive Summary
                        </Typography>
                        <Grid container spacing={3}>
                            <Grid item xs={12} md={6}>
                                <Box sx={{ p: 3, bgcolor: 'success.light', borderRadius: 2, color: 'white' }}>
                                    <Typography variant="h6" gutterBottom>Investment Recommendation</Typography>
                                    <Typography variant="h4" sx={{ fontWeight: 600, mb: 1 }}>
                                        HIGHLY RECOMMENDED
                                    </Typography>
                                    <Typography variant="body2">
                                        ROI: {formatNumber(roiResults.roi_percentage)}% over system lifetime
                                    </Typography>
                                </Box>
                            </Grid>
                            <Grid item xs={12} md={6}>
                                <Box sx={{ p: 3, bgcolor: 'info.light', borderRadius: 2, color: 'white' }}>
                                    <Typography variant="h6" gutterBottom>Payback Period</Typography>
                                    <Typography variant="h4" sx={{ fontWeight: 600, mb: 1 }}>
                                        {formatNumber(roiResults.payback_period)} Years
                                    </Typography>
                                    <Typography variant="body2">
                                        Excellent return timeline for solar investment
                                    </Typography>
                                </Box>
                            </Grid>
                        </Grid>
                    </CardContent>
                </Card>

                {/* Professional Recommendations - Moved to prominent position */}
                {roiResults.recommendations && (
                    <Card sx={{ mb: 3, borderRadius: 2, border: 2, borderColor: 'success.main' }}>
                        <CardContent>
                            <Typography variant="h5" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
                                <Star sx={{ mr: 1, color: 'warning.main' }} />
                                Professional Recommendations
                            </Typography>
                            <Grid container spacing={2}>
                                {roiResults.recommendations.map((recommendation: string, index: number) => {
                                    const cleanRecommendation = recommendation.replace(/^[✅🌞💰🌱]\s*/, '');
                                    const emoji = recommendation.match(/^[✅🌞💰🌱]/)?.[0] || '✅';

                                    return (
                                        <Grid item xs={12} sm={6} key={index}>
                                            <Box sx={{
                                                p: 2,
                                                bgcolor: alpha(theme.palette.success.main, 0.1),
                                                borderRadius: 2,
                                                border: 1,
                                                borderColor: 'success.light',
                                                display: 'flex',
                                                alignItems: 'center'
                                            }}>
                                                <Typography variant="h6" sx={{ mr: 2 }}>
                                                    {emoji}
                                                </Typography>
                                                <Typography variant="body1" sx={{ fontWeight: 500 }}>
                                                    {cleanRecommendation}
                                                </Typography>
                                            </Box>
                                        </Grid>
                                    );
                                })}
                            </Grid>
                        </CardContent>
                    </Card>
                )}

                {/* Key Financial Metrics */}
                <Card sx={{ mb: 3, borderRadius: 2 }}>
                    <CardContent>
                        <Typography variant="h5" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
                            <TrendingUp sx={{ mr: 1, color: 'primary.main' }} />
                            Financial Analysis
                        </Typography>
                        <Grid container spacing={3}>
                            <Grid item xs={12} sm={6} md={3}>
                                <Box sx={{ textAlign: 'center', p: 2 }}>
                                    <AttachMoney sx={{ fontSize: 40, color: 'primary.main', mb: 1 }} />
                                    <Typography variant="h5" color="primary.main" sx={{ fontWeight: 600 }}>
                                        {formatCurrency(roiResults.total_investment)}
                                    </Typography>
                                    <Typography variant="body2" color="text.secondary">
                                        Total Investment
                                    </Typography>
                                </Box>
                            </Grid>
                            <Grid item xs={12} sm={6} md={3}>
                                <Box sx={{ textAlign: 'center', p: 2 }}>
                                    <Euro sx={{ fontSize: 40, color: 'success.main', mb: 1 }} />
                                    <Typography variant="h5" color="success.main" sx={{ fontWeight: 600 }}>
                                        {formatCurrency(roiResults.annual_savings)}
                                    </Typography>
                                    <Typography variant="body2" color="text.secondary">
                                        Annual Savings
                                    </Typography>
                                </Box>
                            </Grid>
                            <Grid item xs={12} sm={6} md={3}>
                                <Box sx={{ textAlign: 'center', p: 2 }}>
                                    <Schedule sx={{ fontSize: 40, color: 'warning.main', mb: 1 }} />
                                    <Typography variant="h5" color="warning.main" sx={{ fontWeight: 600 }}>
                                        {formatNumber(roiResults.payback_period)}
                                    </Typography>
                                    <Typography variant="body2" color="text.secondary">
                                        Payback Years
                                    </Typography>
                                </Box>
                            </Grid>
                            <Grid item xs={12} sm={6} md={3}>
                                <Box sx={{ textAlign: 'center', p: 2 }}>
                                    <TrendingUp sx={{ fontSize: 40, color: 'secondary.main', mb: 1 }} />
                                    <Typography variant="h5" color="secondary.main" sx={{ fontWeight: 600 }}>
                                        {formatNumber(roiResults.roi_percentage)}%
                                    </Typography>
                                    <Typography variant="body2" color="text.secondary">
                                        Total ROI
                                    </Typography>
                                </Box>
                            </Grid>
                        </Grid>
                    </CardContent>
                </Card>

                {/* Solar Production Details */}
                <Card sx={{ mb: 3, borderRadius: 2 }}>
                    <CardContent>
                        <Typography variant="h5" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
                            <WbSunny sx={{ mr: 1, color: 'primary.main' }} />
                            Solar Production Summary
                        </Typography>
                        <Grid container spacing={3}>
                            <Grid item xs={12} md={4}>
                                <Box sx={{ textAlign: 'center', p: 2, bgcolor: 'grey.50', borderRadius: 1 }}>
                                    <ElectricBolt sx={{ fontSize: 40, color: 'primary.main', mb: 1 }} />
                                    <Typography variant="h5" color="primary.main" sx={{ fontWeight: 600 }}>
                                        {formatNumber(solarResults.annual_kwh, 0)} kWh
                                    </Typography>
                                    <Typography variant="body2" color="text.secondary">
                                        Annual Production
                                    </Typography>
                                </Box>
                            </Grid>
                            <Grid item xs={12} md={4}>
                                <Box sx={{ textAlign: 'center', p: 2, bgcolor: 'grey.50', borderRadius: 1 }}>
                                    <WbSunny sx={{ fontSize: 40, color: 'secondary.main', mb: 1 }} />
                                    <Typography variant="h5" color="secondary.main" sx={{ fontWeight: 600 }}>
                                        {formatNumber(solarResults.daily_average)} kWh
                                    </Typography>
                                    <Typography variant="body2" color="text.secondary">
                                        Daily Average
                                    </Typography>
                                </Box>
                            </Grid>
                            <Grid item xs={12} md={4}>
                                <Box sx={{ textAlign: 'center', p: 2, bgcolor: 'grey.50', borderRadius: 1 }}>
                                    <TrendingUp sx={{ fontSize: 40, color: 'success.main', mb: 1 }} />
                                    <Typography variant="h5" color="success.main" sx={{ fontWeight: 600 }}>
                                        {formatNumber(solarResults.peak_month_production, 0)} kWh
                                    </Typography>
                                    <Typography variant="body2" color="text.secondary">
                                        Peak Month Production
                                    </Typography>
                                </Box>
                            </Grid>
                        </Grid>
                    </CardContent>
                </Card>

                {/* Environmental Impact */}
                <Card sx={{ mb: 3, borderRadius: 2 }}>
                    <CardContent>
                        <Typography variant="h5" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
                            <Nature sx={{ mr: 1, color: 'success.main' }} />
                            Environmental Impact
                        </Typography>
                        <Box sx={{ p: 3, bgcolor: 'success.light', borderRadius: 2, color: 'white' }}>
                            <Grid container spacing={3} alignItems="center">
                                <Grid item xs={12} md={8}>
                                    <Typography variant="h6" gutterBottom>
                                        Annual CO₂ Reduction
                                    </Typography>
                                    <Typography variant="body1">
                                        Your solar installation will prevent approximately{' '}
                                        <strong>{formatNumber(roiResults.co2_reduction)} tons</strong> of CO₂
                                        emissions annually, equivalent to planting{' '}
                                        <strong>{Math.round(roiResults.co2_reduction * 16)}</strong> trees per year.
                                    </Typography>
                                </Grid>
                                <Grid item xs={12} md={4} sx={{ textAlign: 'center' }}>
                                    <Nature sx={{ fontSize: 60, mb: 1 }} />
                                    <Typography variant="h4" sx={{ fontWeight: 600 }}>
                                        {formatNumber(roiResults.co2_reduction)} t
                                    </Typography>
                                    <Typography variant="body2">
                                        CO₂ Reduction/Year
                                    </Typography>
                                </Grid>
                            </Grid>
                        </Box>
                    </CardContent>
                </Card>

                {/* System Specifications */}
                <Card sx={{ mb: 3, borderRadius: 2 }}>
                    <CardContent>
                        <Typography variant="h5" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
                            <Assignment sx={{ mr: 1, color: 'primary.main' }} />
                            System Specifications
                        </Typography>
                        <Grid container spacing={2}>
                            <Grid item xs={12} md={6}>
                                <Typography variant="subtitle1" gutterBottom sx={{ fontWeight: 600 }}>
                                    Installation Details:
                                </Typography>
                                <Typography variant="body2" sx={{ mb: 1 }}>
                                    <strong>Location:</strong> {data?.location}
                                </Typography>
                                <Typography variant="body2" sx={{ mb: 1 }}>
                                    <strong>Roof Area:</strong> {data?.roofArea} m²
                                </Typography>
                                <Typography variant="body2" sx={{ mb: 1 }}>
                                    <strong>Orientation:</strong> {data?.orientation?.charAt(0).toUpperCase() + data?.orientation?.slice(1)}
                                </Typography>
                                <Typography variant="body2" sx={{ mb: 1 }}>
                                    <strong>Weather Analysis:</strong> {data?.weatherAnalysis?.charAt(0).toUpperCase() + data?.weatherAnalysis?.slice(1)}
                                </Typography>
                            </Grid>
                            <Grid item xs={12} md={6}>
                                <Typography variant="subtitle1" gutterBottom sx={{ fontWeight: 600 }}>
                                    Consumption Details:
                                </Typography>
                                <Typography variant="body2" sx={{ mb: 1 }}>
                                    <strong>Annual Consumption:</strong> {data?.annualConsumption} kWh
                                </Typography>
                                <Typography variant="body2" sx={{ mb: 1 }}>
                                    <strong>Expected Production:</strong> {formatNumber(solarResults.annual_kwh, 0)} kWh
                                </Typography>
                                <Typography variant="body2" sx={{ mb: 1 }}>
                                    <strong>Production Coverage:</strong> {formatNumber((solarResults.annual_kwh / data?.annualConsumption) * 100)}%
                                </Typography>
                            </Grid>
                        </Grid>
                    </CardContent>
                </Card>

                {/* Detailed Report Button */}
                {roiResults.feasibility_report && (
                    <Card sx={{ mb: 3, borderRadius: 2 }}>
                        <CardContent sx={{ textAlign: 'center' }}>
                            <Typography variant="h5" gutterBottom sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                                <Article sx={{ mr: 1, color: 'primary.main' }} />
                                Detailed Feasibility Report
                            </Typography>
                            <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
                                Access comprehensive technical analysis, financing options, and regulatory information
                            </Typography>
                            <Button
                                variant="contained"
                                size="large"
                                startIcon={<Article />}
                                onClick={() => setModalOpen(true)}
                                sx={{ px: 4, py: 1.5 }}
                            >
                                View Detailed Report
                            </Button>
                        </CardContent>
                    </Card>
                )}

                {/* Footer */}
                <Paper sx={{ p: 2, mt: 3, bgcolor: 'grey.100', textAlign: 'center', borderRadius: 2 }}>
                    <Typography variant="body2" color="text.secondary">
                        Report generated on {new Date().toLocaleString('de-DE')} •
                        Renewable Energy Investment Analyzer •
                        Based on real German EDA data (2012-2017)
                    </Typography>
                </Paper>
            </div>

            {/* Detailed Report Modal */}
            <Modal
                open={modalOpen}
                onClose={() => setModalOpen(false)}
                closeAfterTransition
                slots={{ backdrop: Backdrop }}
                slotProps={{
                    backdrop: {
                        timeout: 500,
                    },
                }}
            >
                <Fade in={modalOpen}>
                    <Box sx={modalStyle}>
                        {/* Modal Header */}
                        <Box sx={{
                            p: 3,
                            bgcolor: 'primary.main',
                            color: 'white',
                            display: 'flex',
                            justifyContent: 'space-between',
                            alignItems: 'center'
                        }}>
                            <Typography variant="h5">
                                Detailed Feasibility Report
                            </Typography>
                            <IconButton
                                onClick={() => setModalOpen(false)}
                                sx={{ color: 'white' }}
                            >
                                <Close />
                            </IconButton>
                        </Box>

                        {/* Modal Content */}
                        <Box sx={{
                            p: 3,
                            height: 'calc(100% - 80px)',
                            overflowY: 'auto',
                            fontFamily: '"Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'
                        }}>
                            <Typography
                                variant="body1"
                                sx={{
                                    whiteSpace: 'pre-line',
                                    lineHeight: 1.7,
                                    fontSize: '1rem',
                                    color: 'text.primary',
                                    '& strong': {
                                        fontWeight: 600,
                                        color: 'primary.main'
                                    }
                                }}
                            >
                                {roiResults.feasibility_report
                                    ?.replace(/\*\*(.*?)\*\*/g, '$1')
                                    ?.replace(/\*(.*?)\*/g, '• $1')
                                }
                            </Typography>
                        </Box>
                    </Box>
                </Fade>
            </Modal>
        </Box>
    );
};

export default ROIAnalysis;
