console.log("hello cart");

function update_cart(obj_id, action) {
  // alert('mod')
  const csrfToken = document.getElementById("csrf_token").value;
  
  $.ajax({
    type: "POST",
    url: `${action}/`,
    data: {
      product_id: obj_id,
      csrfmiddlewaretoken: csrfToken,
      action: "post",
    },
    success: function (json) {
      let counter_span = document.getElementById("cart_counter");
      counter_span.textContent = json.cart_count;

      // Convert cart_count to an integer and check the condition
      if (parseInt(json.cart_count) > 0) {
        counter_span.classList.remove("bg-gray-200");
        counter_span.classList.add("bg-yellow-400");
      } else {
        counter_span.classList.remove("bg-yellow-400");
        counter_span.classList.add("bg-gray-200");
      }

      // Reload the cart content
      $("#my_cart").load(location.href + " #my_cart");
    },
    error: function (xhr, errmsg, err) {
      console.error(errmsg);
    },
  });
}

// function clear_cart() {
//   alert('mod')
//   // Retrieve the CSRF token from the hidden input
//   const csrfToken = document.getElementById("csrf_token").value;

//   $.ajax({
//     type: "POST",
//     url: "clear_cart/",
//     data: {
//       csrfmiddlewaretoken: csrfToken,
//       action: "post",
//     },
//     success: function (json) {
//       // console.log(json.cart_count); // Ensure the key matches the JSON response key
//       // document.getElementById("cart_counter").textContent = json.cart_count;

//       counter_span = document.getElementById("cart_counter");
//       counter_span.textContent = json.cart_count;
//       counter_span.classList.remove("bg-red-600 text-white");
//       counter_span.classList.add("bg-gray-200 text-black ");
//     },
//     error: function (xhr, errmsg, err) {
//       console.error(errmsg); // Log error message to console
//     },
//   });
// }
