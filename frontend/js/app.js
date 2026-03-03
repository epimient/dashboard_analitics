/**
 * app.js — Orquestador principal (Dashboard Limpio).
 */
import { API } from './api.js';
import { Charts } from './charts.js';
import { AIPanel } from './ai_panel.js';

const App = {
    async init() {
        console.log("Dashboard iniciado...");
        this.bindEvents();
        await this.refreshData();
        AIPanel.init();
    },

    bindEvents() {
        // Refresh manual
        const btnRefresh = document.getElementById('btn-refresh');
        if (btnRefresh) {
            btnRefresh.onclick = () => this.refreshData();
        }

        // Refresh data desde sidebar
        const btnRefreshData = document.getElementById('btn-refresh-data');
        if (btnRefreshData) {
            btnRefreshData.onclick = async () => {
                const statusEl = document.getElementById('data-status');
                statusEl.textContent = 'Actualizando...';
                statusEl.classList.add('text-muted');

                try {
                    await this.refreshData();
                    statusEl.textContent = '✓ Sincronizado';
                    statusEl.classList.remove('text-muted');
                    statusEl.classList.add('text-success');
                    setTimeout(() => {
                        statusEl.classList.remove('text-success');
                        statusEl.classList.add('text-muted');
                    }, 2000);
                } catch (err) {
                    console.error(err);
                    statusEl.textContent = '✗ Error al actualizar';
                    statusEl.classList.remove('text-muted');
                    statusEl.classList.add('text-danger');
                    alert('Error al actualizar datos: ' + err.message);
                }
            };
        }

        // Export (Print)
        document.getElementById('btn-export').onclick = () => {
            window.print();
        };

        // Smooth Scroll para navegación sidebar
        document.querySelectorAll('.sidebar-modern .nav-link').forEach(link => {
            link.onclick = (e) => {
                const targetId = link.getAttribute('href').replace('#', '');
                const section = document.getElementById(targetId);
                if (section) {
                    e.preventDefault();
                    section.scrollIntoView({ behavior: 'smooth' });

                    // Activar link
                    document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
                    link.classList.add('active');
                }
            };
        });
    },

    async refreshData() {
        try {
            const stats = await API.getStats();
            this.updateKPIs(stats);
            Charts.renderAll(stats);
        } catch (err) {
            console.error("Error al cargar datos:", err);
            throw err;
        }
    },

    updateKPIs(stats) {
        document.getElementById('kpi-total').textContent = stats.total_responses;
        document.getElementById('kpi-presencial-ok').textContent = `${stats.pct_attends_ok.toFixed(2)}%`;
        document.getElementById('kpi-virtual-pref').textContent = `${(stats.pct_virtual + stats.pct_hibrida).toFixed(2)}%`;
        document.getElementById('kpi-internet').textContent = `${stats.pct_stable_internet.toFixed(2)}%`;
    }
};

window.addEventListener('DOMContentLoaded', () => App.init());
