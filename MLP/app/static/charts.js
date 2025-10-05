// static/charts.js

document.addEventListener("DOMContentLoaded", () => {
    // --- Configuración de gráficas ---
    const ctxLoss = document.getElementById("loss-chart")?.getContext("2d");
    const ctxAcc = document.getElementById("accuracy-chart")?.getContext("2d");

    if (!ctxLoss || !ctxAcc) {
        console.warn("Los canvas de estadísticas no existen en esta página.");
        return; // Evitar errores si los canvas no existen
    }

    const lossChart = new Chart(ctxLoss, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Pérdida (Loss)',
                data: [],
                borderColor: 'rgba(255, 99, 132, 1)',
                backgroundColor: 'rgba(230, 104, 131, 0.2)',
                fill: true,
                tension: 0.3
            }]
        },
        options: {
            responsive: true,
            plugins: { legend: { display: true } },
            scales: { y: { beginAtZero: true } }
        }
    });

    const accChart = new Chart(ctxAcc, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Precisión (Accuracy)',
                data: [],
                borderColor: 'rgba(54, 162, 235, 1)',
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                fill: true,
                tension: 0.3
            }]
        },
        options: {
            responsive: true,
            plugins: { legend: { display: true } },
            scales: { y: { min: 0, max: 1 } }
        }
    });

    // --- Función para actualizar gráficas dinámicamente ---
    async function updateCharts() {
        try {
            const res = await fetch("/history?limit=50");
            if (!res.ok) {
                console.warn("No se pudo obtener historial de predicciones:", res.status);
                return;
            }

            const data = await res.json();
            if (!Array.isArray(data) || data.length === 0) {
                console.info("No hay datos de historial disponibles para las gráficas.");
                return;
            }

            const labels = data.map((_, i) => i + 1);
            const accData = data.map(d => typeof d.confidence === "number" ? d.confidence : 0);
            const lossData = data.map(d => 1 - (typeof d.confidence === "number" ? d.confidence : 0));

            accChart.data.labels = labels;
            accChart.data.datasets[0].data = accData;
            accChart.update();

            lossChart.data.labels = labels;
            lossChart.data.datasets[0].data = lossData;
            lossChart.update();
        } catch (err) {
            console.error("Error actualizando gráficas:", err);
        }
    }

    updateCharts();
    setInterval(updateCharts, 5000); // Refrescar cada 5 segundos
});
