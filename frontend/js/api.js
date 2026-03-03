/**
 * api.js — Wrapper para llamadas al backend FastAPI.
 */

const BASE_URL = ''; // En producción se sirve del mismo dominio

export const API = {
    /**
     * Obtiene estadísticas y KPIs
     */
    async getStats(filters = {}) {
        const query = new URLSearchParams(filters).toString();
        const url = `${BASE_URL}/api/survey/stats?${query}`;
        const resp = await fetch(url);
        if (!resp.ok) throw new Error('Error al cargar estadísticas');
        return await resp.json();
    },

    /**
     * Obtiene todas las respuestas
     */
    async getResponses(filters = {}) {
        const query = new URLSearchParams(filters).toString();
        const url = `${BASE_URL}/api/survey/responses?${query}`;
        const resp = await fetch(url);
        if (!resp.ok) throw new Error('Error al cargar respuestas');
        return await resp.json();
    },

    /**
     * Analiza texto con IA
     */
    async analyzeAI(columnKey, provider, apiKey, model) {
        const payload = {
            column_key: columnKey,
            provider: provider,
            model: model || undefined,
            responses: [] // El backend las sacará de memoria si va vacío
        };

        if (provider === 'groq' && apiKey) {
            payload.api_key = apiKey;
        }

        const resp = await fetch(`${BASE_URL}/api/ai/analyze`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (!resp.ok) {
            const err = await resp.json();
            throw new Error(err.detail || 'Error en análisis IA');
        }
        return await resp.json();
    }
};
