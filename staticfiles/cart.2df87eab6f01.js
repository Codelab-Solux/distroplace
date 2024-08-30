// console.log('hello cart')

function update_cart(obj_id, action) {
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
      counter_span = document.getElementById("cart_counter")
      counter_span.textContent = json.cart_count;
      if (json.cart_count > 0) {
        counter_span.classList.remove("bg-gray-200 text-black");
        counter_span.classList.add("bg-red-600 text-white");
      } else{
        counter_span.classList.remove("bg-red-600 text-white");
        counter_span.classList.add("bg-gray-200 text-black ");
      }


      // Reload the cart content
      $("#my_cart").load(location.href + " #my_cart");
    },
    error: function (xhr, errmsg, err) {
      console.error(errmsg);
    },
  });
}


function clear_cart(obj_id) {
  // Retrieve the CSRF token from the hidden input
  const csrfToken = document.getElementById("csrf_token").value;

  $.ajax({
    type: "POST",
    url: 'clear_cart/',
    data: {
      product_id: obj_id,
      csrfmiddlewaretoken: csrfToken,
      action: "post",
    },
    success: function (json) {
      counter_span = document.getElementById("cart_counter");
      counter_span.textContent = json.cart_count;
      counter_span.classList.remove("bg-red-600 text-white");
      counter_span.classList.add("bg-gray-200 text-black ");
    },
    error: function (xhr, errmsg, err) {
      console.error(errmsg); // Log error message to console
    },
  });
}