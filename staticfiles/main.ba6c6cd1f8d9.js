//  go back button ----------------------------------------------------------------------------------------------------
document
  .getElementById("back-button")
  .addEventListener("click", function (event) {
    event.preventDefault(); // Prevent the default anchor behavior
    window.history.go(-1); // Go back two pages
  });

// logout confirmation --------------------------------------------------------
document
  .getElementById("logout-link")
  .addEventListener("click", function (event) {
    event.preventDefault();
    if (confirm("Voulez vous vraiment vous deconnecter?")) {
      window.location.href = this.href;
    }
  });

//  form handlers ----------------------------------------------------------------------------------------------------
function clearForm(div_id) {
  var form = document.getElementById(div_id);
  form.reset();
}

//  selectfield dashes remover ------------
$(document).ready(function () {
  // Add a placeholder option to the select element
  elements = document.getElementsByClassName("input_selector");
  elements.forEach((e) => {
    e.children().first().remove();
    $(".input_selector").prepend(
      '<option value="" disabled selected></option>'
    );
  });
});

//  tabs controller ----------------------------------------------------------------------------------------------------
document.getElementById("defaultTab").click();
function openTab(event, tabName) {
  var i, tabcontent, tabBtn;
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }
  tabBtn = document.getElementsByClassName("tabBtn");
  for (i = 0; i < tabBtn.length; i++) {
    tabBtn[i].className = tabBtn[i].className.replace(" active", "");
  }
  document.getElementById(tabName).style.display = "block";
  event.currentTarget.className += " active";
  var minitabs = document.getElementsByClassName("minitabcontent");
  if (minitabs.length != 0) {
    minitabs = tabcontent.children;
  }
}

//  commentbox controller ----------------------------------------------------------------------------------------------------
function toggleCommentBox() {
  var box = document.querySelector(`.comment_box`);
  if (box.classList.contains("hidden")) {
    box.classList.remove("hidden");
    box.classList.add("block");
  } else {
    box.classList.remove("block");
    box.classList.add("hidden");
  }
}

//  accordions controller ----------------------------------------------------------------------------------------------------
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

// nav mechanism ----------------------------------------------------------------------------------------------------
function toggleNav(e) {
  e.name === "nav"
    ? ((e.name = "close"), navlinks.classList.remove("hidden"))
    : ((e.name = "nav"), navlinks.classList.add("hidden"));
}

//  dropdown controllers ----------------------------------------------------------------------------------------------------
function toggleDropdown(e) {
  e.name === "dropdownBtn"
    ? ((e.name = "close"), dropdownMenu.classList.remove("hidden"))
    : ((e.name = "dropdownBtn"), dropdownMenu.classList.add("hidden"));
}

function toggleMenu(e, obj_id) {
  activeMenu = document.getElementById(obj_id);
  e.name === `sentry`
    ? ((e.name = "close"), activeMenu.classList.remove("hidden"))
    : ((e.name = `sentry`), activeMenu.classList.add("hidden"));
}

window.addEventListener("mouseup", function (event) {
  if (
    !activeMenu.contains(event.target) &&
    !document.getElementById("sentry").contains(event.target)
  ) {
    activeMenu.classList.add("hidden");
    document.getElementById("sentry").name = "sentry";
  }

  if (
    !dropdownMenu.contains(event.target) &&
    !document.getElementById("dropdownBtn").contains(event.target)
  ) {
    dropdownMenu.classList.add("hidden");
    document.getElementById("dropdownBtn").name = "dropdownBtn";
  }

  if (
    !navlinks.contains(event.target) &&
    !document.querySelector('[name="nav"]').contains(event.target)
  ) {
    navlinks.classList.add("hidden");
    document.querySelector('[name="nav"]').name = "nav";
  }
});

// PDF exporter --------------------------------------------------------
function exportPDF(div_id) {
  var element = document.getElementById(div_id);
  var opt = {
    margin: 0.5,
    filename: `${div_id}.pdf`,
    image: { type: "jpeg", quality: 0.98 },
    html2canvas: { scale: 2 },
    jsPDF: {
      unit: "in",
      // format: [80 / 25.4, 297 / 25.4],
      // orientation: "portrait",
      orientation: "landscape",
    },
  };
  html2pdf().from(element).set(opt).save();
}

// ----------------------------appointments exporter-------------------------------
function extractXLS(div_id) {
  document.getElementById(div_id);
  // Hide the "more_visits" row
  const moreRows = document.getElementById(`more${div_id}`);
  if (moreRows) {
    moreRows.style.display = "none";
  }
  // Create a new Excel workbook
  const wb = XLSX.utils.book_new();

  // Create a new worksheet
  const ws = XLSX.utils.table_to_sheet(document.getElementById(div_id));
  // Add the worksheet to the workbook
  XLSX.utils.book_append_sheet(wb, ws, "Datasheet");

  // Save the workbook as an Excel file
  XLSX.writeFile(wb, "datasheet.xlsx");
}
