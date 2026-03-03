/**
 * charts.js — Gestión de visualizaciones con paleta Pastel.
 */

// Paleta de Colores Pasteles Suaves
const PASTEL_COLORS = [
    'rgba(108, 142, 242, 0.7)', // Azul suave (Primary)
    'rgba(76, 175, 80, 0.6)',   // Verde menta
    'rgba(255, 183, 77, 0.6)',  // Naranja suave
    'rgba(77, 208, 225, 0.6)',  // Cyan pastel
    'rgba(186, 104, 200, 0.6)', // Lavanda
    'rgba(255, 138, 101, 0.6)', // Coral suave
    'rgba(144, 164, 174, 0.6)', // Gris azulado
];

const BORDER_COLORS = [
    '#6c8ef2', '#4caf50', '#ffb74d', '#4dd0e1', '#ba68c8', '#ff8a65', '#90a4ae'
];

// Configuración Global
Chart.defaults.color = '#64748b';
Chart.defaults.borderColor = '#f1f5f9';
Chart.defaults.font.family = "'Inter', sans-serif";
Chart.defaults.font.size = 12;

let instances = {};

export const Charts = {
    renderAll(stats) {
        this.renderDoughnut('chart-modality', stats.preferred_modality_dist);
        this.renderBar('chart-open-virtual', stats.open_to_virtual_dist, 'horizontal');
        this.renderBar('chart-commitment', stats.commitment_level_dist, 'vertical');
        this.renderBar('chart-equipment', stats.has_equipment_dist, 'vertical');
    },

    renderDoughnut(canvasId, dataset) {
        const labels = dataset.map(d => d.label);
        const values = dataset.map(d => d.count);
        const percentages = dataset.map(d => d.percentage);

        this._initChart(canvasId, {
            type: 'doughnut',
            data: {
                labels,
                datasets: [{
                    data: values,
                    backgroundColor: PASTEL_COLORS,
                    borderColor: '#ffffff',
                    borderWidth: 2,
                    hoverOffset: 10
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: { usePointStyle: true, padding: 20 }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(255, 255, 255, 0.9)',
                        titleColor: '#1e293b',
                        bodyColor: '#475569',
                        borderColor: '#e2e8f0',
                        borderWidth: 1,
                        padding: 12,
                        displayColors: true,
                        callbacks: {
                            label: function(context) {
                                const label = context.label || '';
                                const value = context.parsed || 0;
                                const percentage = percentages[context.dataIndex] || 0;
                                return `${label}: ${value} (${percentage.toFixed(2)}%)`;
                            }
                        }
                    }
                },
                cutout: '70%'
            }
        });
    },

    renderBar(canvasId, dataset, orientation = 'vertical') {
        const labels = dataset.map(d => d.label);
        const values = dataset.map(d => d.count);
        const percentages = dataset.map(d => d.percentage);

        this._initChart(canvasId, {
            type: 'bar',
            data: {
                labels,
                datasets: [{
                    label: 'Respuestas',
                    data: values,
                    backgroundColor: PASTEL_COLORS[0],
                    borderColor: BORDER_COLORS[0],
                    borderWidth: 1,
                    borderRadius: 8,
                    maxBarThickness: 40
                }]
            },
            options: {
                indexAxis: orientation === 'horizontal' ? 'y' : 'x',
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        backgroundColor: 'rgba(255, 255, 255, 0.9)',
                        titleColor: '#1e293b',
                        bodyColor: '#475569',
                        borderColor: '#e2e8f0',
                        borderWidth: 1,
                        padding: 12,
                        callbacks: {
                            label: function(context) {
                                const value = context.parsed || 0;
                                const percentage = percentages[context.dataIndex] || 0;
                                return ` ${value} (${percentage.toFixed(2)}%)`;
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: { display: orientation === 'vertical' },
                        ticks: { stepSize: 1 }
                    },
                    x: {
                        grid: { display: orientation === 'horizontal' },
                        ticks: { stepSize: 1 }
                    }
                }
            }
        });
    },

    _initChart(id, config) {
        const ctx = document.getElementById(id);
        if (!ctx) return;
        if (instances[id]) instances[id].destroy();
        instances[id] = new Chart(ctx, config);
    }
};
