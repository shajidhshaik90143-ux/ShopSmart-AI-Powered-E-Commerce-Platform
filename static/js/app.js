document.addEventListener("DOMContentLoaded", () => {
    setTimeout(() => {
        document.querySelectorAll(".flash").forEach(el => {
            el.style.opacity = "0.85";
        });
    }, 2500);
});
