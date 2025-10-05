// static/darkmode.js
document.addEventListener("DOMContentLoaded", () => {
    const toggleBtn = document.getElementById("toggle-darkmode-navbar");
    const darkmodeLink = document.getElementById("darkmode-css");

    if (!toggleBtn) return console.error("No se encontró el botón de darkmode!");
    if (!darkmodeLink) return console.error("No se encontró el link de darkmode!");

    // Función para actualizar el estado del botón y guardar preferencia
    const setDarkMode = (enabled) => {
        darkmodeLink.disabled = !enabled;
        toggleBtn.textContent = enabled ? "🌞 Modo Claro" : "🌙 Modo Oscuro";
        localStorage.setItem("darkmode", enabled ? "on" : "off");
        console.log("Darkmode activo:", enabled);
    };

    // Revisar preferencia guardada
    const savedPreference = localStorage.getItem("darkmode");
    if (savedPreference) {
        setDarkMode(savedPreference === "on");
    }

    // Escuchar click del botón
    toggleBtn.addEventListener("click", () => {
        setDarkMode(darkmodeLink.disabled);
    });
});
