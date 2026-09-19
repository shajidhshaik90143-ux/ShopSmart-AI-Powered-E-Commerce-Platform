function updateQuantity(input, max) {
    let value = parseInt(input.value || "1", 10);
    input.value = Math.max(1, Math.min(value, max));
}
