const html = document.getElementById("htmlPage");
const check = document.getElementById("switch-check");
const label = document.querySelector('label[for="switch-check"]');

function updateLabel() {
  if (!check.checked) {
    html.setAttribute("data-bs-theme", "light");
    label.textContent = "Light mode";
  } else {
    html.setAttribute("data-bs-theme", "dark");
    label.textContent = "Dark mode";
  }
}

updateLabel();

check.addEventListener("change", updateLabel);
