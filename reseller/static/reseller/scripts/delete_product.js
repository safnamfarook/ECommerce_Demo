function delete_product(id) {
    var del_id = id;
    
    $.ajax({
        url: 'product-del',
        type: 'GET',
        // processData: false,
        // contentType: false,
        data: {
            'id': del_id
        },

        success: function(response) {

            
            window.location.href='http://127.0.0.1:8000/reseller/all-products'

        },
        error: function(response) {

            toastr.success(response.msg);


        }

    });
}