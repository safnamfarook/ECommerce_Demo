function edit_product(id) {
    console.log("test");
    var product_id = parseInt(id);
    console.log("idididid", product_id + 1)
    var formdata = new FormData();
    title = $('#title').text();
    description = $('#description').text();
    price = parseInt($('#price').text());
    quantity = parseInt($('#quantity').text());
    stats = $('#status').text();
    console.log("hai"+stats)
    formdata.append('id', product_id);
    formdata.append('title', title);
    formdata.append('description', description);
    formdata.append('price', price);
    formdata.append('quantity', quantity);
    formdata.append('status', stats);
    console.log("consoling form data");
    console.log('form data ios',formdata)

   
    $.ajaxSetup({
        headers: {
          "X-CSRFToken": $('[name=csrfmiddlewaretoken]').val()
        }
    })

    $.ajax({
         url: 'http://127.0.0.1:8000/reseller/update-product',
        type: 'POST',
        processData: false,
        contentType: false,
        data: formdata,
        success: function(response) {
            toastr.success(response.msg);
        },

    });
}