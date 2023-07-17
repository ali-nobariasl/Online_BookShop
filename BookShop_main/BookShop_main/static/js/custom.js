




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
                    removeCartItem(0, cart_id)
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
});

