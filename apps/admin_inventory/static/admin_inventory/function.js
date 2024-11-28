//DOUBLE-U IN DA SCHAATTT

const html = document.getElementById("htmlPage");
const check = document.getElementById("switch-check");
const label = document.querySelector('label[for="switch-check"]');

function loadTheme() {
  const savedTheme = localStorage.getItem("theme");
  if (savedTheme === "dark") {
    html.setAttribute("data-bs-theme", "dark");
    check.checked = true;
    label.textContent = "Dark mode";
  } else {
    html.setAttribute("data-bs-theme", "light");
    check.checked = false;
    label.textContent = "Light mode";
  }
}

function updateLabel() {
  if (!check.checked) {
    html.setAttribute("data-bs-theme", "light");
    label.textContent = "Light mode";
    localStorage.setItem("theme", "light");
  } else {
    html.setAttribute("data-bs-theme", "dark");
    label.textContent = "Dark mode";
    localStorage.setItem("theme", "dark");
  }
}

loadTheme();

check.addEventListener("change", updateLabel);

