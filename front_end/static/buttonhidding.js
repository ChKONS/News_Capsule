function myFunction() {
  var button = document.getElementById("button");
  var isToggled = 0;
  var inputElements = document.getElementsByName("topic");
  for (var i = 0; i < inputElements.length; i++) {
    if (inputElements[i].type != "checkbox") {
      continue;
    }
    if (inputElements[i].checked) {
      isToggled += 1;
    }
  }
  if (isToggled > 0) {
    button.style.display = "block";
  } else {
    button.style.display = "none";
  }
}

