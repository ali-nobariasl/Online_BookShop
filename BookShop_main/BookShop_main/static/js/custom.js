



$(document).ready(function(){
     $('.add_to_cart').on('click', function(e){
        e.preventDefault();
        
        book_id = $(this).attr('data-id');
        url = $(this).attr('data-url');
        data = {
            bood_id: book_id,
        }

        $.ajax({
            type:'GET',
            url:url,
            data:data,
            success: function(response){
                console.log(response);
            }
        })
     })

     // pace the cart quantity on load
     $('.item_qty').each(function(){
        var the_id = $(this).attr('id')
        var qty = $(this).attr('data-qty')
        console.log(qty)
     })
});

