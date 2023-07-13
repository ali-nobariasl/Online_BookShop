



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
                alert(response);
            }
        })
     })
});