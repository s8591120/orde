// orderSystem.js

// 取得菜單
function getMenu() {
    $.get('/get_menu', function(data) {
        // 在這裡處理菜單項目數據
        const menuList = $('#menu-list');
        menuList.empty();
        data.forEach(item => {
            // 在每個菜單項目後添加一個 checkbox 供用戶選擇
            menuList.append(`
                <li>
                    <input type="checkbox" name="menu-item" value="${item.id}">
                    ${item.name} - $${item.price}
                </li>
            `);
        });
    });
}

// 將訂單信息發送到後台
function sendOrderToBackend(orderData) {
    $.ajax({
        type: 'POST',
        url: '/order',
        contentType: 'application/json;charset=UTF-8',
        data: JSON.stringify({ selectedItems: orderData }),
        success: function(response) {
            console.log(response);
            alert('Order completed successfully! Total Price: $' + response.total_price);
            // 可以在這裡進行其他處理，例如刷新頁面或跳轉
        },
        error: function(error) {
            console.error(error);
            alert('Failed to complete order. Please try again.');
        }
    });
}

// 將訂單項目顯示在頁面上
function displayOrder(order) {
    const orderList = $('#order-list');
    orderList.empty();
    order.forEach(item => {
        orderList.append(`<li>${item.name} - $${item.price}</li>`);
    });
}

// 頁面加載完成後執行
$(document).ready(function() {
    getMenu(); // 取得菜單

    // 完成訂單按鈕點擊事件
    $('#complete-order').click(function() {
        // 在這裡獲取用戶選擇的訂單項目
        const selectedItems = [];
        $('input[name="menu-item"]:checked').each(function() {
            selectedItems.push(parseInt($(this).val()));
        });

        // 將訂單數據發送到後台
        sendOrderToBackend(selectedItems);
    });
});
