// Fetch Firebase configuration from the server and initialize Firebase
fetch("/accounts/firebase-config/")
  .then((response) => response.json())
  .then((config) => {
    firebase.initializeApp(config);
  })
  .catch((error) => console.error("Error loading Firebase config:", error));

// Sign in with phone number using Firebase
function signInWithPhoneNumber(phoneNumber) {
  const appVerifier = new firebase.auth.RecaptchaVerifier(
    "recaptcha-container"
  );

  firebase
    .auth()
    .signInWithPhoneNumber(phoneNumber, appVerifier)
    .then(function (confirmationResult) {
      // SMS sent. Ask the user for the verification code.
      const code = prompt("Enter the OTP");
      return confirmationResult.confirm(code);
    })
    .then(function (result) {
      // User signed in successfully.
      const user = result.user;
      // Send the user data to your backend
      sendUserToBackend(user);
    })
    .catch(function (error) {
      console.error("Error during sign-in:", error);
    });
}

// Send authenticated user data to the backend
function sendUserToBackend(user) {
  user.getIdToken().then((idToken) => {
    fetch("/accounts/firebase-auth/", {
      method: "POST",
      body: JSON.stringify({ idToken: idToken }),
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrftoken,
      },
    })
      .then((response) => response.json())
      .then((data) => console.log(data))
      .catch((error) => console.error("Error sending user to backend:", error));
  });
}
