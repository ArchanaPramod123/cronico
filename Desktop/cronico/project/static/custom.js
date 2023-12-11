$(document).ready(function(){
    $("#addtocart").on('click',function(){
        var _vm=$(this);
        var _qty=$("#productQty").val();
        var _pid=$(".product-id").val();
        var _image = $(".product-image").val();
        var _name=$(".title-detail").text(); 
        var _price = $("#hidden-updated-price").val();
        console.log(_qty,_pid,_name,_price)
        //ajax
        $.ajax({
            url:'/add-to-cart',
            data:{
                'id':_pid,
                'image': _image,
                'qty':_qty,
                'name':_name,
                'price':_price
            },
            dataType:'json',
            beforeSend:function(){
                _vm.attr('disabled',true);
            },
            success:function(res){
                $(".cart-list").text(res.totalitems);
                _vm.attr('disabled',false);
                location.reload(true);
            }

        });
        //end
    });
    //delete item from cart
    $(document).on('click','.delete-item',function(){
        var _pId=$(this).attr('data-item');
        var _vm=$(this);
        $.ajax({
            url:'/delete-from-cart',
            data:{
                'id':_pId,
            },
            dataType:'json',
            beforeSend:function(){
                _vm.attr('disabled',true);
            },
            success:function(res){
                
                $(".cart-list").text(res.totalitems);
                updateCartView(res.data, res.total_amt);
                _vm.attr('disabled',false);
                location.reload();
            },
            error: function() {
                // Handle error if needed
                _vm.attr('disabled', false);
            }

        });
        });
        
});
function updateCartView(cartData, totalAmt) {
    $('.cart-table tbody').html(''); // Clear the table body
    for (var productId in cartData) {
        var item = cartData[productId];

    }
    $('.total-amount').text('$' + totalAmt);
}