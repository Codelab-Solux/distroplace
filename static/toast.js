//  show and hide snackbar ----------------------------------------------------------------------------------------------------
function showSnackbar(message, type) {
  const snackbar = document.getElementById("snackbar");
  const snackbarMessage = document.getElementById("snackbar-message");

  snackbarMessage.textContent = message;
  snackbar.className = `fixed top-4 right-4 p-4 rounded w-80 flex items-center justify-between transition-transform duration-500 ${type} show`;

  setTimeout(hideSnackbar, 3000);
}

function hideSnackbar() {
  const snackbar = document.getElementById("snackbar");
  snackbar.classList.remove("show");
  setTimeout(() => {
    snackbar.style.top = "-100px";
  }, 500);
}

// Snackbar logic-------------------------------------------------
document.addEventListener("htmx:configRequest", function (event) {
  // If necessary, you can configure htmx request headers here
});

document.addEventListener("htmx:afterOnLoad", function (event) {
  if (event.detail.xhr.status === 403) {
    showSnackbar("Access denied!", "denial");
  } else if (event.detail.xhr.status === 404) {
    showSnackbar("Resource missing!", "info");
  } else if (event.detail.xhr.status === 204) {
    showSnackbar("Operation successful!", "success");
  } else if (event.detail.xhr.status === 500) {
    showSnackbar("Server error occurred!", "alert");
  }
});

document.addEventListener("access-denied", function () {
  showSnackbar("Access denied!", "denial");
});

document.addEventListener("server-error", function () {
  showSnackbar("Error encountered!", "alert");
});

document.addEventListener("resource-error", function () {
  showSnackbar("Error encountered!", "info");
});

document.addEventListener("db_changed", function () {
  showSnackbar("Database updated successfully.", "success");
});
