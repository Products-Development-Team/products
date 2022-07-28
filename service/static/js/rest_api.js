$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#product_id").val(res.id);
        $("#product_name").val(res.name);
        $("#product_category").val(res.category);
        $("#product_description").val(res.description);
        $("#product_available").val(res.available);
        $("#product_price").val(res.price);
        $("#product_rating").val(res.rating);
        $("#product_num_rating").val(res.no_of_users_rated);
    }

    /// Clears all form fields
    function clear_form_data() {
        $("#product_name").val("");
        $("#product_category").val("");
        $("#product_description").val("");
        $("#product_available").val("");
        $("#product_price").val("");
        $("#product_rating").val("");
        $("#product_num_rating").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    // ****************************************
    // Create a Product
    // ****************************************

    $("#create-btn").click(function () {

        let name = $("#product_name").val();
        let category = $("#product_category").val();
        let description = $("#product_description").val();
        let available = Boolean($("#product_available").val() == "true");
        let price = $("#product_price").val();
        let rating = $("#product_rating").val();
        let num_rating = $("#product_num_rating").val();

        let data = {
            "name": name,
            "category": category,
            "description": description,
            "available": available,
            "price": parseFloat(price),
            "rating": parseFloat(rating),
            "no_of_users_rated": parseInt(num_rating)
        };

        $("#flash_message").empty();
        
        let ajax = $.ajax({
            type: "POST",
            url: "/products",
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });


    // ****************************************
    // Update a Product
    // ****************************************

    $("#update-btn").click(function () {

        let product_id = $("#product_id").val();
        let name = $("#product_name").val();
        let category = $("#product_category").val();
        let description = $("#product_description").val();
        let available = $("#product_available").val();
        let price = $("#product_price").val();
        let rating = $("#product_rating").val();
        let num_rating = $("#product_num_rating").val();
        
        // if (available == "UNKNOWN") {
        //     available = ""
        // } else {
        //     available = Boolean(available == "true")
        // }
        
        let data = {}
        if (name) {
            data["name"] = name;
        }
        if (category) {
            data["category"] = category;
        }
        if (description) {
            data["description"] = description;
        }
        if (available != "UNKNOWN") {
            data["available"] = Boolean(available == "true");
        }
        if (price) {
            data["price"] = parseFloat(price);
        }
        if (rating) {
            data["rating"] = parseFloat(rating);
        }
        if (num_rating) {
            data["no_of_users_rated"] = parseInt(num_rating);
        }

        $("#flash_message").empty();

        let ajax = $.ajax({
                type: "PUT",
                url: `/products/${product_id}`,
                contentType: "application/json",
                data: JSON.stringify(data)
            })

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Retrieve a Product
    // ****************************************

    $("#retrieve-btn").click(function () {

        let product_id = $("#product_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/products/${product_id}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Delete a Product
    // ****************************************

    $("#delete-btn").click(function () {

        let product_id = $("#product_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "DELETE",
            url: `/products/${product_id}`,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function(res){
            clear_form_data()
            flash_message("Product has been Deleted!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        $("#product_id").val("");
        $("#flash_message").empty();
        clear_form_data()
    });

    // ****************************************
    // Search for a Product
    // ****************************************

    $("#search-btn").click(function () {

        // let name = $("#product_name").val();
        let category = $("#product_category").val();
        let available = $("#product_available").val();
        let price = $("#product_price").val();
        let rating = $("#product_rating").val();

        let queryString = ""

        // if (name) {
        //     queryString += 'name=' + name
        // }
        if (category) {
            if (queryString.length > 0) {
                queryString += '&category=' + category
            } else {
                queryString += 'category=' + category
            }
        }
        if (available == "true") {
            if (queryString.length > 0) {
                queryString += '&available=True'
            } else {
                queryString += 'available=True'
            }
        }
        if (available == "false") {
            if (queryString.length > 0) {
                queryString += '&available=False'
            } else {
                queryString += 'available=False'
            }
        }
        if (price) {
            if (queryString.length > 0) {
                queryString += '&price=' + price
            } else {
                queryString += 'price=' + price
            }
        }
        if (rating) {
            if (queryString.length > 0) {
                queryString += '&rating=' + rating
            } else {
                queryString += 'rating=' + rating
            }
        }

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/products?${queryString}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            $("#search_results").empty();
            let table = '<table class="table table-striped" cellpadding="10">'
            table += '<thead><tr>'            
            table += '<th class="col-md-2">ID</th>'
            table += '<th class="col-md-2">Name</th>'
            table += '<th class="col-md-2">Category</th>'
            table += '<th class="col-md-2">Description</th>'
            table += '<th class="col-md-2">Available</th>'
            table += '<th class="col-md-2">Price</th>'
            table += '<th class="col-md-2">Rating</th>'
            table += '<th class="col-md-2">Number of rating</th>'
            table += '</tr></thead><tbody>'

            let firstProduct = "";
            for(let i = 0; i < res.length; i++) {
                let product = res[i];
                table +=  `<tr id="row_${i}"><td>${product.id}</td><td>${product.name}</td><td>${product.category}</td><td>${product.description}</td><td>${product.available}</td><td>${product.price}</td><td>${product.rating}</td><td>${product.no_of_users_rated}</td></tr>`;
                if (i == 0) {
                    firstProduct = product;
                }
            }
            table += '</tbody></table>';
            $("#search_results").append(table);

            // copy the first result to the form
            if (firstProduct != "") {
                update_form_data(firstProduct)
            }

            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Add a rating to Product
    // ****************************************

    $("#add-rating-btn").click(function () {

        let product_id = $("#add_product_id").val();
        let rating = $("#add_product_rating").val();

        $("#flash_message").empty();

        let data = {"rating": parseInt(rating)}

        let ajax = $.ajax({
            type: "PUT",
            url: `/products/${product_id}/rating`,
            contentType: "application/json",
            data: JSON.stringify(data),
        })

        ajax.done(function(res){
            clear_form_data()
            flash_message("Rating has been submitted!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });

})
