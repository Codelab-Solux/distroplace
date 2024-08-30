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

// firebase web setup

firebase.auth().useDeviceLanguage();

window.recaptchaVerifier = new firebase.auth.RecaptchaVerifier(
  "sign-in-button",
  {
    size: "invisible",
    callback: (response) => {
      // reCAPTCHA solved, allow signInWithPhoneNumber.
      onSignInSubmit();
    },
  }
);

window.recaptchaVerifier = new firebase.auth.RecaptchaVerifier(
  "recaptcha-container"
);

window.recaptchaVerifier = new firebase.auth.RecaptchaVerifier(
  "recaptcha-container",
  {
    size: "normal",
    callback: (response) => {
      // reCAPTCHA solved, allow signInWithPhoneNumber.
      // ...
    },
    "expired-callback": () => {
      // Response expired. Ask user to solve reCAPTCHA again.
      // ...
    },
  }
);

recaptchaVerifier.render().then((widgetId) => {
  window.recaptchaWidgetId = widgetId;
});

const recaptchaResponse = grecaptcha.getResponse(recaptchaWidgetId);

const phoneNumber = getPhoneNumberFromUserInput();
const appVerifier = window.recaptchaVerifier;
firebase
  .auth()
  .signInWithPhoneNumber(phoneNumber, appVerifier)
  .then((confirmationResult) => {
    // SMS sent. Prompt user to type the code from the message, then sign the
    // user in with confirmationResult.confirm(code).
    window.confirmationResult = confirmationResult;
    // ...
  })
  .catch((error) => {
    // Error; SMS not sent
    // ...
  });

  grecaptcha.reset(window.recaptchaWidgetId);

  // Or, if you haven't stored the widget ID:
  window.recaptchaVerifier.render().then(function (widgetId) {
    grecaptcha.reset(widgetId);
  });




  // sign in
  const code = getCodeFromUserInput();
  confirmationResult
    .confirm(code)
    .then((result) => {
      // User signed in successfully.
      const user = result.user;
      // ...
    })
    .catch((error) => {
      // User couldn't sign in (bad verification code?)
      // ...
    });

    var credential = firebase.auth.PhoneAuthProvider.credential(
      confirmationResult.verificationId,
      code
    );

    firebase.auth().signInWithCredential(credential);