// Fetch Firebase configuration from the server and initialize Firebase
fetch("/accounts/firebase-config/")
  .then((response) => response.json())
  .then((config) => {
    firebase.initializeApp(config);
  })
  .catch((error) => console.error("Error loading Firebase config:", error));

// Sign in with phone number using Firebase
function phoneAuth() {
  var phoneNumber = document.getElementById("phone").value;
  var appVerifier = new firebase.auth.RecaptchaVerifier("recaptcha-container");
  firebase
    .auth()
    .signInWithPhoneNumber(phoneNumber, appVerifier)
    .then(function (confirmationResult) {
      var code = prompt("Enter the OTP");
      return confirmationResult.confirm(code);
    })
    .then(function (result) {
      return result.user.getIdToken();
    })
    .then(function (firebaseToken) {
      fetch("/firebase-login/", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: "firebase_token=" + firebaseToken,
      }).then(function (response) {
        if (response.ok) {
          alert("Login successful!");
          window.location.href = "/";
        } else {
          alert("Login failed!");
        }
      });
    })
    .catch(function (error) {
      console.error(error);
      alert("Something went wrong!");
    });
}
