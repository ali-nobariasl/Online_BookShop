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

                $('#id_latitude').val(latitude);
                $('#id_longitude').val(longitude);
                $('#id_address').val(address);
            }
        });
        //loop through the address components and assign them to the fields
        for(var i = 0; i<place.address_components.length; i++){
            for(var j = 0; j <place.address_components[i].types.length;j++){
                if(place.address_components[i].types[j] == 'country'){
                    $('#id_country').val(place.address_components[i].long_name);
                }
                // get state
                if(place.address_components[i].types[j] == 'administrative_area_level_1'){
                    $('#id_state').val(place.address_components[i].long_name);
                }
                // get city
                if(place.address_components[i].types[j] == 'locality'){
                    $('#id_city').val(place.address_components[i].long_name);
                }
                //get pin code
                if(place.address_components[i].types[j] == 'postal_code'){
                    $('#id_pin_code').val(place.address_components[i].long_name);
                }else{
                    $('#id_pin_code').val("");
                }
            }
        }

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

     
     $('.add_hour').on('click',function(e){
        e.preventDefault();
        var day = document.getElementById('id_day').value
        var from_hour = document.getElementById('id_from_hour').value
        var to_hour = document.getElementById('id_to_hour').value
        var is_closed = document.getElementById('id_is_closed').checked
        var csrf_token = $('input[name=csrfmiddlewaretoken]').val()
        var url = document.getElementById('add_hour_url').value

        if(is_closed){
            is_closed ='True'
            condition = "day != ''"
        }else{
            is_closed ='False'
            condition = "day != '' && from_hour != '' && to_hour != ''"
        }

        if (eval(condition)){
            $.ajax({
                type: 'POST',
                url:url,
                data:{
                    'day':day,
                    'from_hour':from_hour,
                    'to_hour':to_hour,
                    'is_closed':is_closed,
                    'csrfmiddlewaretoken':csrf_token,
                },
                success: function(response){
                    if(response.status =='success'){
                        if(response.is_closed=='closed'){
                            html = '<tr><td><b>'+response.day+'</b></td><td>Closed</td><td><a >Remove</a></td></tr>'
                        }else{
                            html = '<tr><td><b>'+response.day+'</b></td><td>'+response.from_hour+' b- '+response.to_hour+'</td><td><a >Remove</a></td></tr>'
                        }
                        $(".opening_hours").append(html)
                        document.getElementById("open_hours").reset();
                    }else{ 
                        swal(response.message,'',"error")
                    }
            }})
        }else{
            swal('Please fill all fields','','info')
        }
     })
     // document ready close

});

