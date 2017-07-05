$(document).ready(function(){
    //load the orders and diplay them in the array
    loadOrders();
});

/*
        Loading orders into the array
 */
function loadOrders() {
    $("#order_table tbody").empty();
    $.ajax({
        url: "http://localhost:8000/orders",
        type: "GET",
        success: function (response) {
            if (response.error) {
                $("#table_container").append('<div class="alert alert-danger" role="alert">Une erreur s\'est produite</div>')
            } else {
                var orders = response.data;
                if (orders.length === 0) {
                    $("#table_container").append('<div class="alert alert-info" role="alert">Aucune commande</div>')
                }
                orders.forEach(function (order) {
                    var newTr = $("<tr>");
                    newTr.attr("data-id", order.id);
                    newTr.append("<td>" + order.order_id + "</td>");
                    newTr.append("<td>" + order.customer_first_name + "</td>");
                    newTr.append("<td>" + order.marketplace + "</td>");
                    newTr.append("<td>" + order.mp_order_status + "</td>");
                    newTr.append("<td>" + order.lg_order_status + "</td>");
                    newTr.append("<td>" + order.order_amount + "</td>");

                    $("#order_table tbody").append(newTr);
                });
                console.log(response);
            }
        }
    })
}