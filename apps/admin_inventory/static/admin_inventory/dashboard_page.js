function fetchBookCount() {
    document.addEventListener('DOMContentLoaded', function() {
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
});
}

fetchBookCount();