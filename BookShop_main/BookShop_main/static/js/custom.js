let autocomplete;

function initAutoComplete(){
    autocomplete = new google.maps.places.AutoComplete(
        document.getElementById('id_address'),
        {
            types: ['geocode','establishment'],  // geocod is for address //establishment is for business address
            // defaul in this app is "Tr". add your own country
            componentRestrictions:{'country':['tr']},
        })
    // functionto specify what should happen when the predicate is clicked
    autocomplete.addListener('place_changed', onPlaceChanged )
}


function onPlaceChanged(){
        var place = autocomplete.getPlace();

        // USer did not select the prediction. Reset the input field or alert
        if(!place.geometry){
            document.getElementById('id_address').placeholder ='Start typing ...'; 
        }
        else{
           // console.log('place name=>', place.name)
        }
        // get the address components and assign them to the fields.

        var geocoder = new google.maps.Geocoder()
        var address = document.getElementById('id_address').value
        geocoder.geocode({'address': address}, function(result, status){

            if(status == google.maps.GeocoderStatus.ok){
                var latitude = result[0].geometry.location.lat();
                var longitude = result[1].geometry.location.lng();

                $('id_latitude').val(latitude);
                $('id_longitude').val(longitude);
                $('id_address').val(address);
            }
        });
        //loop through the address components and assign them to the fields
        
}




$(document).ready(function(){
    // add cart
     $('.add_to_cart').on('click', function(e){
        e.preventDefault();
        
        book_id = $(this).attr('data-id');
        url = $(this).attr('data-url');
        $.ajax({
            type:'GET',
            url:url,
            success: function(response){
                console.log(response);
                if(response.status=='login_required'){
                    swal(response.message,'','info').then(function(){
                        window.location='/accounts/login/';
                    })
                }if(response.status=='failed'){
                    swal(response.message,'','error')
                }else{
                    $('#cart_counter').html(response.cart_counter['cart_count']);
                    $('#qty-'+book_id).html(response.qty);

                    // subtotal tax and grand total
                    appplyCartAmuounts(
                        response.cart_amount['subtotal'],
                        response.cart_amount['tax'],
                        response.cart_amount['grand_total'],

                    )
                }
            }
        })
     })

     // place the cart quantity on load
     $('.item_qty').each(function(){
        var the_id = $(this).attr('id')
        var qty = $(this).attr('data-qty')
        $('#'+the_id).html(qty)
     })


     // decrease cart
     $('.decrease_cart').on('click', function(e){
        e.preventDefault();
        
        book_id = $(this).attr('data-id');
        url = $(this).attr('data-url');
        cart_id = $(this).attr('id');

        $.ajax({
            type:'GET',
            url:url,
            success: function(response){
                console.log(response);
                if(response.status=='login_required'){
                    swal(response.message,'','info').then(function(){
                        window.location='/accounts/login/';
                    })
                }if(response.status=='failed'){
                    swal(response.message,'','error')
                }else{
                    $('#cart_counter').html(response.cart_counter['cart_count']);
                    $('#qty-'+book_id).html(response.qty);
                                        // subtotal tax and grand total
                    appplyCartAmuounts(
                                        response.cart_amount['subtotal'],
                                        response.cart_amount['tax'],
                                        response.cart_amount['grand_total'])
                    if(window.location.pathname =='/cart'){
                        removeCartItem(response.qty, cart_id )
                        checkEmptyCart();
                        }
                   
                }
            }
        })
     })

     // delete cart
     $('.delete_cart').on('click', function(e){
        e.preventDefault();
        
        cart_id = $(this).attr('data-id');
        url = $(this).attr('data-url');
        $.ajax({
            type:'GET',
            url:url,
            success: function(response){
                console.log(response);
                if(response.status=='failed'){
                    swal(response.message,'','error')
                }else{
                    $('#cart_counter').html(response.cart_counter['cart_count']);
                    swal(response.message,'','success')
                    appplyCartAmuounts(
                        response.cart_amount['subtotal'],
                        response.cart_amount['tax'],
                        response.cart_amount['grand_total'])
                    removeCartItem(0, cart_id);
                    checkEmptyCart();
                }
            }
        })
     })



     // delete the cart elemet
     function removeCartItem(cartItemQty,cart_id){
        if(cartItemQty <= 0){
            // remove the cart item element
            document.getElementById("cart-item-"+cart_id).remove();
     }}


     // check if the cart is empty
     function checkEmptyCart(){
        var cart_counter = document.getElementById('cart_counter').innerHTML
        if( cart_counter==0){
            document.getElementById("empty-cart").style.display = "block";
        }
     }


     // appply cart amuounts
     function appplyCartAmuounts(subtotal,grand_total, tax){

        if(window.location.pathname=='/cart'){
            $('#subtotal').html(subtotal);
            $('#tax').html(tax);
            $('#total').html(grand_total);
        }
     }
});

