const snackbar = document.getElementById("snackbar");

function showSnackbar(message, type) {
  const snackbarMessage = document.getElementById("snackbar-message");

  snackbarMessage.textContent = message;
  snackbar.className = `fixed top-4 right-4 p-4 rounded w-80 flex items-center justify-between ${type} show`;

  setTimeout(hideSnackbar, 3000);
}

function hideSnackbar() {
  snackbar.classList.add("slide-up");
}

document.addEventListener("htmx:afterOnLoad", function (event) {
  const status = event.detail.xhr.status;
  if (status === 403) {
    showSnackbar("Access denied!", "denial");
  } else if (status === 404) {
    showSnackbar("Resource missing!", "info");
  } else if (status === 204) {
    showSnackbar("Operation successful!", "success");
  } else if (status === 500) {
    showSnackbar("Server error occurred!", "alert");
  }
});

function handleAlerts() {
  const alerts = document.querySelectorAll(".alert");

  alerts.forEach((alert) => {
    // Auto-dismiss after 3 seconds
    setTimeout(() => {
      alert.classList.add("slide-up");
    }, 3000); // 3000ms = 3 seconds

    // Remove the element from the DOM after the slide-up animation
    alert.addEventListener("animationend", (e) => {
      if (e.animationName === "slideUp") {
        alert.remove();
      }
    });
  });
}

// Call handleAlerts function when the DOM is fully loaded
document.addEventListener("DOMContentLoaded", handleAlerts);

// If using HTMX or dynamically generating alerts, make sure to call handleAlerts when alerts are added to the DOM
document.addEventListener("htmx:afterOnLoad", handleAlerts);
