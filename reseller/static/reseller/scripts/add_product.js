var submenu = {
    Gadgets: ["Phone", "laptops", "headset", "speaker"],
    Clothes: ["Shirt", "Pants", "T-shirt", "Kurta", "shirt dress"],
    Footwear: ["Sports shoes", "Flats", "Heels", "Boots"]
}

function makeSubmenu(value) {
   
    if (value.length == 0) {
        document.getElementById("subcategory").innerHTML = "<option></option>";
    } else {
        var citiesOptions = "";
        for (categoryId in submenu[value]) {
            citiesOptions += "<option>" + submenu[value][categoryId] + "</option>";
        }
        document.getElementById("subcategory").innerHTML = citiesOptions;
    }
}



function resetSelection() {
    document.getElementById("category").selectedIndex = 0;
    document.getElementById("subcategory").selectedIndex = 0;
}


(function() {
    'use strict';

    window.addEventListener('load', function() {
        // Fetch all the forms we want to apply custom Bootstrap validation styles to
        var forms = document.getElementsByClassName('needs-validation');

        // Loop over them and prevent submission
        var validation = Array.prototype.filter.call(forms, function(form) {
            form.addEventListener('submit', function(event) {
                if (form.checkValidity() === false) {
                    event.preventDefault();
                    event.stopPropagation();

                } else {
                    event.preventDefault();
                    event.stopPropagation();
                    add_products();
                }
                form.classList.add('was-validated');
            }, false);
        });
    }, false);
})();

function add_products() {

    var formdata = new FormData();
    var image = $('#customFile')[0].files[0];
    title = $('#title').val();
    regproductid = $('#regproductid').val();
    description = $('#description').val();
    price = $('#price').val();
    quantity = $('#quantity').val();
    weight = $('#weight').val();
    weightunit = $('#weightunit').val();
    category = $('#category').val();
    subcategory = $('#subcategory').val();
    vendor = $('#brand').val();
    status = $('#status').val();
    formdata.append('image', image);
    formdata.append('title', title);
    formdata.append('regproductid', regproductid);
    formdata.append('description', description);
    formdata.append('price', price);
    formdata.append('quantity', quantity);
    formdata.append('weight', weight);
    formdata.append('weightunit', weightunit);
    formdata.append('category', category);
    formdata.append('subcategory', subcategory);
    formdata.append('vendor', vendor);
    formdata.append('status', status);

    $.ajaxSetup({
        headers: {
          "X-CSRFToken": $('[name=csrfmiddlewaretoken]').val()
        }
    })
    $.ajax({
        
     
         url: 'http://127.0.0.1:8000/reseller/add-product',
        type: 'POST',

        processData: false,
        contentType: false,
        data: formdata,
        success: function(response) {
            if(response.res==true) 
            toastr.success('Product Added Succesfully')

            else 
                toastr.error('Product Reg ID already Added');
             
        },
    });
}