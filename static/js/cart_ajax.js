

// $('button.add-to-cart').click(function (){
//
//     let product_id = $(this).attr("data-field");
//     let cart_notification_number = $("#cart-notifications").text();
//     let product_input_quantity = $("input[name='quant" + product_id +"']").val();
//     let product_chosen_size = $("input[name='chosen-size" + product_id + "']:checked").val();
//
//     if (!product_chosen_size) {
//         alert("plz choose a size")
//     }
//     else {
//         $.ajax({
//             // url: '{% url "cart_app:cart_add" %}',
//             url: '/cart/add/',
//             type: "POST",
//             data: {
//                 'product_id': product_id,
//                 'quantity': product_input_quantity,
//                 'size': product_chosen_size
//             },
//             success: function (data){
//                 localStorage.setItem("cart_length", data.length);
//                 $(".cart-notifications").html(localStorage.getItem("cart_length"))
//                 console.log(data.length);
//             }
//         })
//     }
// })

// $('button.plus-minus-btn').click(function (){
//
//             let product_id = $(this).attr("data-id");
//             let cart_notification_number = $("#cart-notifications").text();
//             let product_input_quantity = $("input[name='quant" + product_id +"']").val();
//             let product_chosen_size = $("input[name='chosen-size" + product_id + "']:checked").val();
//
//             $.ajax({
//                 // url: '{% url "cart_app:cart_add" %}',
//                 url: '/cart/add/',
//                 type: "POST",
//                 data: {
//                     'product_id': product_id,
//                     'quantity': product_input_quantity,
//                     // 'size': product_chosen_size
//                 },
//                 success: function (data){
//                     localStorage.setItem("cart_length", data.length);
//                     $(".cart-notifications").html(localStorage.getItem("cart_length"))
//                     console.log(data.length);
//                 }
//             })
//         })