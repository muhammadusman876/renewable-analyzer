import React from 'react';
import { Card, CardContent, Typography, Box, useTheme } from '@mui/material';
import { XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Area, AreaChart } from 'recharts';
import { TrendingUp } from '@mui/icons-material';

interface SolarChartProps {
    monthlyProduction: number[];
}

const monthNames = [
    'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
    'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
];

const SolarChart: React.FC<SolarChartProps> = ({ monthlyProduction }) => {
    const theme = useTheme();

    const data = monthNames.map((month, i) => ({
        month,
        kWh: Math.round(monthlyProduction[i] || 0),
        kWhLabel: `${Math.round(monthlyProduction[i] || 0)} kWh`
    }));

    const totalProduction = data.reduce((sum, item) => sum + item.kWh, 0);
    const averageProduction = Math.round(totalProduction / 12);
    const peakMonth = data.reduce((max, item) => item.kWh > max.kWh ? item : max, data[0]);

    const CustomTooltip = ({ active, payload, label }: any) => {
        if (active && payload && payload.length) {
            return (
                <Box
                    sx={{
                        bgcolor: 'background.paper',
                        p: 2,
                        border: 1,
                        borderColor: 'divider',
                        borderRadius: 1,
                        boxShadow: 2,
                    }}
                >
                    <Typography variant="subtitle2" color="primary">
                        {label}
                    </Typography>
                    <Typography variant="body2">
                        Production: <strong>{payload[0].value} kWh</strong>
                    </Typography>
                </Box>
            );
        }
        return null;
    };

    return (
        <Card
            sx={{
                mb: 3,
                borderRadius: 2,
                boxShadow: '0 4px 12px rgba(0,0,0,0.1)',
                '&:hover': {
                    boxShadow: '0 6px 16px rgba(0,0,0,0.15)',
                },
                transition: 'box-shadow 0.3s ease-in-out'
            }}
        >
            <CardContent sx={{ p: 3 }}>
                {/* Header Section */}
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
                    <TrendingUp sx={{ mr: 1, color: 'primary.main' }} />
                    <Typography variant="h5" component="h2" sx={{ fontWeight: 600 }}>
                        Monthly Solar Production
                    </Typography>
                </Box>

                {/* Summary Statistics */}
                <Box sx={{
                    display: 'flex',
                    gap: 3,
                    mb: 3,
                    p: 2,
                    bgcolor: 'grey.50',
                    borderRadius: 1
                }}>
                    <Box sx={{ textAlign: 'center' }}>
                        <Typography variant="h6" color="primary.main" sx={{ fontWeight: 600 }}>
                            {totalProduction.toLocaleString()}
                        </Typography>
                        <Typography variant="caption" color="text.secondary">
                            Total Annual (kWh)
                        </Typography>
                    </Box>
                    <Box sx={{ textAlign: 'center' }}>
                        <Typography variant="h6" color="secondary.main" sx={{ fontWeight: 600 }}>
                            {averageProduction.toLocaleString()}
                        </Typography>
                        <Typography variant="caption" color="text.secondary">
                            Monthly Average (kWh)
                        </Typography>
                    </Box>
                    <Box sx={{ textAlign: 'center' }}>
                        <Typography variant="h6" color="success.main" sx={{ fontWeight: 600 }}>
                            {peakMonth.month}
                        </Typography>
                        <Typography variant="caption" color="text.secondary">
                            Peak Month ({peakMonth.kWh} kWh)
                        </Typography>
                    </Box>
                </Box>

                {/* Chart */}
                <Box sx={{ mt: 2 }}>
                    <ResponsiveContainer width="100%" height={350}>
                        <AreaChart
                            data={data}
                            margin={{
                                top: 20,
                                right: 30,
                                left: 20,
                                bottom: 20
                            }}
                        >
                            <defs>
                                <linearGradient id="colorProduction" x1="0" y1="0" x2="0" y2="1">
                                    <stop offset="5%" stopColor={theme.palette.primary.main} stopOpacity={0.8} />
                                    <stop offset="95%" stopColor={theme.palette.primary.main} stopOpacity={0.1} />
                                </linearGradient>
                            </defs>
                            <CartesianGrid
                                strokeDasharray="3 3"
                                stroke={theme.palette.divider}
                                opacity={0.5}
                            />
                            <XAxis
                                dataKey="month"
                                axisLine={false}
                                tickLine={false}
                                style={{
                                    fontSize: '12px',
                                    fill: theme.palette.text.secondary
                                }}
                            />
                            <YAxis
                                axisLine={false}
                                tickLine={false}
                                style={{
                                    fontSize: '12px',
                                    fill: theme.palette.text.secondary
                                }}
                                label={{
                                    value: 'kWh',
                                    angle: -90,
                                    position: 'insideLeft',
                                    style: { textAnchor: 'middle' }
                                }}
                            />
                            <Tooltip content={<CustomTooltip />} />
                            <Area
                                type="monotone"
                                dataKey="kWh"
                                stroke={theme.palette.primary.main}
                                strokeWidth={3}
                                fill="url(#colorProduction)"
                                dot={{
                                    fill: theme.palette.primary.main,
                                    strokeWidth: 2,
                                    stroke: '#fff',
                                    r: 5
                                }}
                                activeDot={{
                                    r: 7,
                                    stroke: theme.palette.primary.main,
                                    strokeWidth: 2,
                                    fill: '#fff'
                                }}
                            />
                        </AreaChart>
                    </ResponsiveContainer>
                </Box>

                {/* Footer Note */}
                <Typography
                    variant="caption"
                    color="text.secondary"
                    sx={{
                        display: 'block',
                        textAlign: 'center',
                        mt: 2,
                        fontStyle: 'italic'
                    }}
                >
                    Production varies by season • Peak summer months typically yield 40-60% more energy
                </Typography>
            </CardContent>
        </Card>
    );
};

export default SolarChart;
