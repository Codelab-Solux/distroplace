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
      document.getElementById("cart_counter").textContent = json.cart_count;

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
      console.log(json.cart_count); // Ensure the key matches the JSON response key
      document.getElementById("cart_counter").textContent = json.cart_count;
    },
    error: function (xhr, errmsg, err) {
      console.error(errmsg); // Log error message to console
    },
  });
}