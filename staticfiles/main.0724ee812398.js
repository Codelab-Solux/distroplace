document.getElementById("back-button").addEventListener("click", function (event) {
    console.log('going back')
    event.preventDefault();
    window.history.go(-1);
  });

  