function calculateTotal() {
    const checkboxes = document.querySelectorAll('.item-checkbox');
    const selectedItems = Array.from(checkboxes)
        .filter(checkbox => checkbox.checked)
        .map(checkbox => parseInt(checkbox.value));

    fetch('/order', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ selectedItems: selectedItems }),
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('totalPrice').innerText = `總價: $${data.total_price.toFixed(2)}`;
    });
}

function submitOrder() {
    alert('訂單已提交！');
}
