// static/realtime.js

document.addEventListener("DOMContentLoaded", () => {
    const canvas = document.getElementById("canvas-mnist");
    const ctx = canvas.getContext("2d");
    const feedbackEl = document.getElementById("prediction-realtime");

    // --- Detectar darkmode ---
    const darkmodeLink = document.getElementById("darkmode-css");
    let isDark = darkmodeLink && !darkmodeLink.disabled;

    function clearCanvas() {
        ctx.fillStyle = isDark ? "#1e1e1e" : "black";
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.beginPath();
    }

    clearCanvas();

    ctx.strokeStyle = isDark ? "white" : "white";
    ctx.lineWidth = 15;
    ctx.lineCap = "round";

    let drawing = false;
    let timeoutId = null;

    canvas.addEventListener("mousedown", () => drawing = true);
    canvas.addEventListener("mouseup", () => drawing = false);
    canvas.addEventListener("mouseout", () => drawing = false);
    canvas.addEventListener("mousemove", drawRealtime);

    function drawRealtime(e) {
        if (!drawing) return;
        const rect = canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        ctx.lineTo(x, y);
        ctx.stroke();
        ctx.beginPath();
        ctx.moveTo(x, y);

        // Debounce 500ms
        if (timeoutId) clearTimeout(timeoutId);
        timeoutId = setTimeout(sendRealtimePrediction, 500);
    }

    async function sendRealtimePrediction() {
        const dataURL = canvas.toDataURL("image/png");
        try {
            const res = await fetch("/predict", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ image: dataURL })
            });
            const json = await res.json();
            if (json.pred !== undefined) {
                feedbackEl.innerText = `Predicción en tiempo real: ${json.pred} (Confianza: ${(json.confidence*100).toFixed(2)}%)`;
            } else {
                feedbackEl.innerText = `Error: ${json.error}`;
            }
        } catch (err) {
            feedbackEl.innerText = `Error conexión: ${err.message}`;
        }
    }

    // Botón para limpiar canvas y feedback
    document.getElementById("clear-canvas").addEventListener("click", () => {
        clearCanvas();
        feedbackEl.innerText = "Predicción en tiempo real: -";
    });

    // --- Actualizar colores si cambia el darkmode dinámicamente ---
    if (darkmodeLink) {
        const observer = new MutationObserver(() => {
            isDark = !darkmodeLink.disabled;
            ctx.strokeStyle = isDark ? "white" : "white";
            clearCanvas();
        });
        observer.observe(darkmodeLink, { attributes: true, attributeFilter: ["disabled"] });
    }
});
