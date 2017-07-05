//Config Object
var config = {
    ORDERS_INDEX_API_URL      : "http://localhost:8000/api/orders",
    ORDERS_SHOW_API_URL       : "http://localhost:8000/api/orders/",
    ORDERS_SHOW_URL           : "http://localhost:8000/orders/"
}

$(document).ready(function(){
    //load the orders and diplay them in the array
    loadOrders();
    //event for click on a order element in the list
    $("#order_table").on("click", "tr", function(event){
        detailLink = getDetailLinkFromClickEvent(event);
        window.location.href = detailLink;
    });
});

function getDetailLinkFromClickEvent(event){
    //getting the id from the element
    orderId = $(event.currentTarget).attr("data-id");
    //returns the url for
    return config.ORDERS_SHOW_URL + orderId;
}

/*
        Loading orders into the array
 */
function loadOrders() {
    $("#order_table tbody").empty();
    $.ajax({
        url: config.ORDERS_INDEX_API_URL,
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