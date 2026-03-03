/**
 * ai_panel.js — Lógica para IA con interfaz Bootstrap Light.
 */
import { API } from './api.js';

export const AIPanel = {
    init() {
        const btns = document.querySelectorAll('.btn-ai-analyze');
        btns.forEach(btn => {
            btn.onclick = (e) => {
                e.stopPropagation(); // Evitar colapso del accordion al hacer clic
                this.handleAnalyze(e);
            };
        });
    },

    async handleAnalyze(event) {
        const btn = event.target.closest('.btn-ai-analyze');
        const columnKey = btn.dataset.col;
        const resultContainer = document.getElementById(`content-${columnKey}`);

        // Configuración por defecto (usando Groq cloud - más rápido y preciso)
        const provider = 'groq';
        const model = 'llama-3.1-8b-instant';

        // UI: Loading
        const originalHTML = btn.innerHTML;
        btn.disabled = true;
        btn.innerHTML = '<span class="spinner-border spinner-border-sm me-1"></span> Procesando...';

        resultContainer.innerHTML = `
            <div class="text-center py-5">
                <div class="spinner-grow text-primary-soft mb-3" style="width: 3rem; height: 3rem;"></div>
                <p class="text-muted">La IA está analizando las respuestas de los estudiantes...</p>
            </div>
        `;

        try {
            const result = await API.analyzeAI(columnKey, provider, '', model);
            this.renderResult(result, resultContainer);
        } catch (err) {
            console.error(err);
            resultContainer.innerHTML = `
                <div class="alert alert-danger border-0 shadow-sm rounded-4 d-flex align-items-center">
                    <i class="bi bi-exclamation-triangle-fill me-3 fs-3"></i>
                    <div>
                        <strong>Error en el análisis:</strong><br>
                        ${err.message}
                    </div>
                </div>
            `;
        } finally {
            btn.disabled = false;
            btn.innerHTML = originalHTML;
        }
    },

    renderResult(data, container) {
        const getSentimentClass = (s) => {
            if (s === 'positive') return 'dot-positive';
            if (s === 'negative') return 'dot-negative';
            return 'dot-neutral';
        };

        container.innerHTML = `
            <div class="ai-result-body animate-in">
                <div class="mb-4">
                    <h6 class="text-uppercase small fw-bold text-muted mb-2">Resumen Ejecutivo</h6>
                    <div class="p-3 bg-light rounded-3 border-start border-4 border-primary-soft">
                        ${data.summary}
                    </div>
                </div>

                <div class="row g-4 mb-4">
                    <div class="col-md-6">
                        <h6 class="text-uppercase small fw-bold text-muted mb-2">Sentimiento General</h6>
                        <div class="d-flex align-items-center">
                            <span class="sentiment-dot ${getSentimentClass(data.sentiment)}"></span>
                            <span class="text-capitalize fw-semibold">${data.sentiment}</span>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <h6 class="text-uppercase small fw-bold text-muted mb-2">Palabras Clave</h6>
                        <div class="d-flex flex-wrap gap-1">
                            ${data.keywords.map(kw => `<span class="pill-soft">${kw}</span>`).join('')}
                        </div>
                    </div>
                </div>

                <hr class="my-4 border-soft">

                <div class="mb-4">
                    <h6 class="text-uppercase small fw-bold text-muted mb-3">Temas Relevantes</h6>
                    <div class="list-group list-group-flush">
                        ${data.themes.map(t => `
                            <div class="list-group-item bg-transparent px-0 border-soft">
                                <div class="d-flex justify-content-between align-items-start mb-1">
                                    <span class="fw-bold">${t.name}</span>
                                    <span class="badge rounded-pill bg-primary-soft-bg text-primary-soft">${t.count} menciones</span>
                                </div>
                                <p class="small text-muted mb-0">${t.description}</p>
                            </div>
                        `).join('')}
                    </div>
                </div>

                <div class="p-3 bg-pastel-blue rounded-4">
                    <h6 class="fw-bold mb-2"><i class="bi bi-lightbulb me-2 text-primary-soft"></i>Recomendaciones Académicas</h6>
                    <ul class="mb-0 small ps-3">
                        ${data.recommendations.map(r => `<li class="mb-1">${r}</li>`).join('')}
                    </ul>
                </div>

                <div class="mt-4 pt-3 border-top border-soft d-flex justify-content-between text-muted x-small">
                    <span>${data.total_analyzed} respuestas analizadas</span>
                    <span>IA: ${data.model_used} (${data.provider_used})</span>
                </div>
            </div>
        `;
    }
};
