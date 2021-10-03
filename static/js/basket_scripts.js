"use strict";



window.onload = function () {
    console.log('DOM ready');
    $('.basket_record').on('change', "input[type='number']", function (event){
        let quantity = event.target.value;
        let basketElementPk = event.target.name;
        console.log(basketElementPk, quantity);
        $.ajax({
            url: "/basket/update/" + basketElementPk + "/" + quantity + "/",
            success: function (data) {
                // console.log(data);
                if (data.status) {
                    $('.basket_summary').html(data.basket_summary);
                }
            },
        });

    });
}