function fetchBookCount() {
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
    })
    .catch(error => {
        console.error('Error fetching book count:', error);
        document.getElementById("bookCount").textContent = '0';
    });
}

// Initial load
document.addEventListener('DOMContentLoaded', () => {
    fetchBookCount();
    
    // Add click event listener to dashboard link
    const dashboardLink = document.querySelector('a[href="/admin/dashboard/"]');
    if (dashboardLink) {
        dashboardLink.addEventListener('click', (e) => {
            e.preventDefault();
            fetchBookCount();
        });
    }
});