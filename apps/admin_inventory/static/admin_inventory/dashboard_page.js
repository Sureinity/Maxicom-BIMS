function fetchDashboardData() {
    fetch("/admin/dashboard/", {
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        document.getElementById("bookCount").textContent = data.bookCount || 0;
        document.getElementById("bookScanned").textContent = data.bookScanned || 0;
        document.getElementById("bookUnscanned").textContent = data.bookUnscanned || 0;
        document.getElementById("totalUsers").textContent = data.totalUsers || 0;
      // Inventory
        document.getElementById("goodCondition").textContent = data.goodCondition || 0;
        document.getElementById("noBarcodeTag").textContent = data.noBarcodeTag|| 0;
        document.getElementById("forRepair").textContent = data.forRepair|| 0;
        document.getElementById("forDisposal").textContent = data.forDisposal|| 0;
    })
    .catch(error => {
        console.error('Error fetching book count:', error);
        document.getElementById("bookCount").textContent = '0';
        document.getElementById("bookScanned").textContent = '0';
        document.getElementById("bookUnscanned").textContent = '0';
        document.getElementById("totalUsers").textContent = '0';
      // Inventory
        document.getElementById("goodCondition").textContent = '0';
        document.getElementById("noBarcodeTag").textContent = '0';
        document.getElementById("forRepair").textContent = '0';
        document.getElementById("forDisposal").textContent = '0';

    });
}

// Initial load
document.addEventListener('DOMContentLoaded', () => {
    fetchDashboardData();
    
    // Add click event listener to dashboard link
    const dashboardLink = document.querySelector('a[href="/admin/dashboard/"]');
    if (dashboardLink) {
        dashboardLink.addEventListener('click', (e) => {
            e.preventDefault();
            fetchDashboardData();
        });
    }
});
