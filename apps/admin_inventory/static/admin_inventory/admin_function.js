const hamBurger = document.querySelector(".toggle-btn");

hamBurger.addEventListener("click", function () {
  document.querySelector("#sidebar").classList.toggle("expand");
});

document.querySelectorAll(".sidebar-link").forEach((link) => {
  link.addEventListener("click", function (e) {
    e.preventDefault();
    const page = this.getAttribute("href");
    loadPage(page);
  });
});

function loadPage(page) {
  const container = document.getElementById("content-container");
  fetch(page)
    .then((response) => {
      if (!response.ok) {
        throw new Error(`Could not load ${page}`);
      }
      return response.text();
    })
    .then((html) => {
      container.innerHTML = html;
    })
    .catch((error) => {
      container.innerHTML = `<p>Error loading page: ${error.message}</p>`;
    });
}

// First page to load
loadPage("/admin/dashboard/");

document.querySelectorAll("tr[data-href]").forEach((row) => {
  row.addEventListener("click", () => {
    window.location.href = row.dataset.href;
  });
});

document.querySelector(".sidebar-link[href='{% url 'admin_dashboard' %}']").addEventListener("click", function (e) {
    e.preventDefault();
    const page = this.getAttribute("href");
    loadPage(page);
    fetchBookCount();
});
