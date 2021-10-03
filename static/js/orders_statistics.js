"use strict";

let orderItemNum, deltaQuantity, orderItemQuantity, deltaCost;
let productPrices = [];
let quantityArray = [];
let priceArray = [];

let totalForms;
let orderTotalQuantity;
let orderTotalCost;

let $orderTotalQuantityDOM;
let $orderTotalCost;
let $orderForm;


function parseOrderForm() {
    for (let i = 0; i < totalForms; i++) {
        let quantity = parseInt($('input[name="order_items-' + i + '-quantity"]').val());
        let price = parseFloat($('.order_items-' + i + '-price').text().replace(',', '.'));
        quantityArray[i] = quantity;
        priceArray[i] = (price) ? price : 0;
    }
}

function renderSummary(orderTotalQuantity, orderTotalCost) {
    $orderTotalQuantityDOM.html(orderTotalQuantity.toString());
    $orderTotalCost.html(Number(orderTotalCost.toFixed(2)).toString().replace('.', ','));
}

function updateTotalQuantity() {
    orderTotalQuantity = 0;
    orderTotalCost = 0;
    for (let i = 0; i < totalForms; i++) {
        orderTotalQuantity += quantityArray[i];
        orderTotalCost += quantityArray[i] * priceArray[i];
    }
    renderSummary(orderTotalQuantity, orderTotalCost);
}

function orderSummaryUpdate(orderItemPrice, deltaQuantity) {
    orderTotalQuantity += deltaQuantity;
    deltaCost = orderItemPrice * deltaQuantity;
    orderTotalCost += deltaCost;
    renderSummary(orderTotalQuantity, orderTotalCost);
}

function deleteOrderItem(row) {
    let targetName = row[0].querySelector('input[type="number"]').name;
    orderItemNum = parseInt(targetName.replace('order_items-', '').replace('-quantity', ''));
    deltaQuantity = -quantityArray[orderItemNum];
    orderSummaryUpdate(priceArray[orderItemNum], deltaQuantity);
}

window.onload = function () {
    totalForms = parseInt($('input[name="order_items-TOTAL_FORMS"]').val());

    $orderTotalQuantityDOM = $('.order_total_quantity');
    orderTotalQuantity = parseInt($orderTotalQuantityDOM.text()) || 0;

    $orderTotalCost = $('.order_total_cost');
    orderTotalCost = parseFloat($orderTotalCost.text().replace(',', '.')) || 0;

    parseOrderForm();

    if (!orderTotalQuantity) {
        updateTotalQuantity();
    }

    $orderForm = $('.order_form');
    $orderForm.on('change', 'input[type="number"]', function (event) {
        orderItemNum = parseInt(event.target.name.replace('order_items-', '').replace('-quantity', ''));
        if (priceArray[orderItemNum]) {
            orderItemQuantity = parseInt(event.target.value);
            deltaQuantity = orderItemQuantity - quantityArray[orderItemNum];
            quantityArray[orderItemNum] = orderItemQuantity;
            orderSummaryUpdate(priceArray[orderItemNum], deltaQuantity);
        }
    });

    $orderForm.on('change', 'input[type="checkbox"]', function (event) {
        orderItemNum = parseInt(event.target.name.replace('order_items-', '').replace('-DELETE', ''));
        if (event.target.checked) {
            deltaQuantity = -quantityArray[orderItemNum];
        } else {
            deltaQuantity = quantityArray[orderItemNum];
        }
        orderSummaryUpdate(priceArray[orderItemNum], deltaQuantity);
    });

    $('.formset_row').formset({
        addText: 'добавить продукт',
        deleteText: 'удалить',
        prefix: 'order_items',
        removed: deleteOrderItem
    });

    $orderForm.on('change', 'select', function (event) {
        let target = event.target;
        let orderItemNum = parseInt(
            target.name.replace('order_items-', '').replace('-product', '')
        );
        let orderItemProductPk = target.options[target.selectedIndex].value;

        if (orderItemProductPk) {
            $.ajax({
                url: "/product/" + orderItemProductPk + "/price/",
                success: function (data) {
                    if (data.price) {
                        priceArray[orderItemNum] = parseFloat(data.price);
                        if (isNaN(quantityArray[orderItemNum])) {
                            quantityArray[orderItemNum] = 0;
                        }
                        let priceHtml = '<span>' +
                            data.price.toString().replace('.', ',') +
                            '</span> руб';
                        let currentTR = $('.order_form table').find('tr:eq(' + (orderItemNum + 1) + ')');
                        currentTR.find('td:eq(2)').html(priceHtml);
                        let $productQuantity = currentTR.find('input[type="number"]');
                        if (!$productQuantity.val() || isNaN($productQuantity.val())) {
                            $productQuantity.val(0);
                        }
                        orderSummaryUpdate(quantityArray[orderItemNum],
                            parseInt($productQuantity.val()));
                    }
                },
            });
        }
    });
}
