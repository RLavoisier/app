//Config Object
var config = {
    ORDERS_INDEX_API_URL      : "http://localhost:8000/api/orders/",
    ORDERS_SHOW_API_URL       : "http://localhost:8000/api/orders/",
    ORDERS_SEARCH_API_URL     : "http://localhost:8000/api/orders/search",
    ORDERS_SHOW_URL           : "http://localhost:8000/orders/",
    ORDERS_NEW_URL            : "http://localhost:8000/orders/new"
}

//Pages list
var pages = {
    ORDERS_INDEX    : "orders-index",
    ORDER_DETAIL    : "order-detail",
    NEW_ORDER       : "new-order"
}

function getDetailLinkFromEvent(event) {
    //getting the id from the element
    orderId = $(event.currentTarget).attr("data-id");
    //returns the url for
    return config.ORDERS_SHOW_URL + orderId;
}

function getDetaiApilLinkFromEvent(event) {
    //getting the id from the element
    orderId = $(event.currentTarget).attr("data-id");
    //returns the url for
    return config.ORDERS_SHOW_API_URL + orderId;
}

/*
        Showing a loader on top of the table
        enterLoading
 */
function enterLoading(){
    //showing the loader
    $(".loader").fadeIn(500);
    //disabling the button
    $(".loading-action").toggleClass("disabled");
}
/*
        Showing a loader on top of the table
        enterLoading
 */
function exitLoading(){
    $(".loader").fadeOut(500);
    $(".loading-action").toggleClass("disabled");
}

/*
        HELPER FUNCTION TE SERIALIZE FORM TO JSON

 */
$.fn.serializeObject = function()
{
   var o = {};
   var a = this.serializeArray();
   $.each(a, function() {
       if (o[this.name]) {
           if (!o[this.name].push) {
               o[this.name] = [o[this.name]];
           }
           o[this.name].push(this.value || '');
       } else {
           o[this.name] = this.value || '';
       }
   });
   return o;
};

/****************************
 *
        ORDER INDEX PAGE

 *****************************/
if($("#page").data("page") === pages.ORDERS_INDEX) {
    $(document).ready(function () {

        //load the orders and diplay them in the array
        loadOrders();

        //event for click on a order element in the list
        $("#order_table tbody").on("click", "tr", function (event) {
            detailLink = getDetailLinkFromEvent(event);
            window.location.href = detailLink;
        });

        //event for refresh button click
        $("#reload_xml").on("click", reinitOrderFromXMLApi);

        //event for new order button click
        $("#new_order").on("click", function(){
            window.location.href = config.ORDERS_NEW_URL;
        });


    });

    /*
        Loading orders into the array
     */
    function loadOrders() {
        $.ajax({
            url     : config.ORDERS_INDEX_API_URL,
            type    : "GET",
            success : function (response) {
                if (response.error) {
                    $("#table_container").append('<div class="alert alert-danger" role="alert">Une erreur s\'est produite</div>')
                } else {
                    $("#order_table tbody").empty();
                    refreshOrderTable(response.data);
                }
            }
        })
    }

    /*

            Refresh the order table with data
     */
    function refreshOrderTable(orders){

        //emptying the table
        $("#order_table tbody").empty();
        $(".alert").remove();

        if (orders.length === 0) {
            $("#table_container").append('<div class="alert alert-info no-order" role="alert">Aucune commande</div>')
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
    }
    /*

            Loading Orders FROM XML
     */
    function reinitOrderFromXMLApi(){
        $.ajax({
            url         : config.ORDERS_INDEX_API_URL,
            type        : "PUT",
            beforeSend  : function(){
                enterLoading();
            },
            success     : function(response){
                refreshOrderTable(response.data);
                //hide all message on the screen
                $(".alert").hide();
                //success message
                $("#table_container").append('<div class="alert alert-success" role="alert">Commandes récupérées avec succès</div>')
            },
            complete    : function(){
                exitLoading();
            }
        });
    }

    //event for search controls
    $(".search-control").on("keyup", function(event){
        searchOrder(event);
    });

    function searchOrder(event){

        //getting the parameters;
        var params = {};
        $("#order_id_search").val() ?               params.order_id = $("#order_id_search").val() : null;
        $("#customer_first_name_search").val() ?    params.customer_first_name = $("#customer_first_name_search").val() : null;
        $("#marketplace_search").val() ?            params.marketplace = $("#marketplace_search").val() : null;

        if(!$.isEmptyObject(params)) {
            $.ajax({
                url         : config.ORDERS_SEARCH_API_URL,
                type        : "GET",
                data        : params,
                success: function (response) {
                    refreshOrderTable(response.data)
                }
            });
        }else{
            loadOrders();
        }
    }
}

/****************************
 *
        ORDER DETAIL PAGE

 *****************************/

if($("#page").data("page") === pages.ORDER_DETAIL){
    $(document).ready(function(){

        //Event for delete form
        $("#delete_form").on("submit", function(event){
            event.preventDefault();

            var id = $(event.currentTarget).attr("data-id");

            $.ajax({
                url         : getDetaiApilLinkFromEvent(event),
                type        : "DELETE",
                headers     : { 'X_METHODOVERRIDE': 'DELETE' },
                success     : function(response){
                    if(!response.error){
                        alert("Order deleted");
                        window.location.href = "/orders";
                    }
                }
            })

        })

    })
}

/****************************
 *
        NEW ORDER PAGE

 *****************************/

if($("#page").data("page") === pages.NEW_ORDER){
    $(document).ready(function(){
        //getting a group of control for a product for future replication
        var product_form_group = $(".product").clone();

        //listener for add new product button
        $("#new_product_btn").on("click", function(){
            $("#products_list").append(product_form_group.clone());
        });

        //listener
        $("#products_list").on("click", "a.delete-btn", function(event){
            $(event.currentTarget).closest(".product").remove();
        });

        /*

                    Submitting the Form
                    2 request :
                        Create the order then get the id back from the server
                        Create the lines for the order


         */
        $("#new_order_form").on("submit", function(event){
            //stop the default
            event.preventDefault();

            //getting a form data object
            var formData = $(this).serializeObject();

            //looping through all the products and buil a json object
            var products = [];
            var amount = 0;

            //Getting the value of the product inputs
            $(".product").each(function(){
               var sku      = $(this).find("#sku").val();
               var quantity = $(this).find("#quantity").val();
               var price    = $(this).find("#price").val();

               //getting the order amount
               amount += quantity * price;

               //pushing the values of current product in the products array
               products.push({
                   product: {
                       sku          : sku,
                       title        : "non",
                       category     : "non",
                       image_url    : "non"
                   },
                   order: "order",
                   quantity: quantity,
                   price_unit: price
               });
            });

            //Filling the FormData Object
            formData.order_amount       = amount;
            formData.lg_order_status    = "Pending";
            formData.mp_order_status    = "Pending";

            //adding the products to the form data

            //sending the request
            $.ajax({
                url         : config.ORDERS_INDEX_API_URL,
                type        : "POST",
                data        : JSON.stringify(formData),
                contentType : "application/json",
                processData : false,
                beforeSend  : function(){
                    enterLoading();
                },
                success     : function(response){
                    console.log(response);
                    //Handling the orderlines
                    insertOrderLines(response, products);
                }
            });
        });

        /*
                Insert Order Lines
         */
        function insertOrderLines(response, products){
            var order = response.data;
            var url = config.ORDERS_SHOW_API_URL + order.id + "/add_details"

            newProducts = [];
            for(var p of products){
                p.order = order.id;
            }

            $.ajax({
                url         : url,
                type        : "POST",
                data        : JSON.stringify(products),
                contentType : "application/json",
                processData : false,
                success     : function(response){
                    console.log(response);
                },
                complete    : function(){
                    exitLoading();
                    window.location.href = "/orders";
                }
            });
        }
    })
}