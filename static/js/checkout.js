document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form");
    if (form && location.pathname.includes("checkout")) {
        form.addEventListener("submit", () => {
            const button = form.querySelector("button");
            if (button) {
                button.disabled = true;
                button.textContent = "Processing...";
            }
        });
    }
});
