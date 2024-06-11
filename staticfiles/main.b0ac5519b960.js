document.getElementById("back-button").addEventListener("click", function (event) {
    console.log('going back')
    event.preventDefault();
    window.history.go(-1);
  });

  
  //  accordions control ----------------------------------------------------------------------------------------------------
  function toggleAccordion(div_id) {
    var active_accordion = document.getElementById(div_id);
    var active_caret = document.getElementById(`${div_id}_caret`);

    // alert(div_id);

    if (active_accordion.classList.contains("hidden")) {
      
      for (let element of document.getElementsByClassName("accordion")) {
        element.classList.remove("block");
        element.classList.add("hidden");
      }
      for (let element of document.getElementsByClassName("fa-caret-down")) {
        element.classList.remove("rotate-180");
      }
      active_accordion.classList.remove("hidden");
      active_accordion.classList.add("block");
      active_caret.classList.add("rotate-180");
    } else {
      
      for (let element of document.getElementsByClassName("accordion")) {
        element.classList.remove("block");
        element.classList.add("hidden");
      }
      active_caret.classList.remove("rotate-180");
      active_accordion.classList.remove("block");
      active_accordion.classList.add("hidden");
    }
  }

