function loadBooks(pageNumber) {
    fetch(`/admin/list-books?page=${pageNumber}`, {
        method: 'GET',
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        const booksContainer = document.getElementById('books-container');
        booksContainer.innerHTML = ""; // Clear existing rows

        data.books.forEach(book => {
            // Create a table row
            const row = document.createElement('tr');
            row.setAttribute('data-bs-toggle', 'modal');
            row.setAttribute('data-bs-target', `#modal_bookdetails_${book.id}`);

            // Populate each cell
            const itypeCell = document.createElement('td');
            itypeCell.textContent = book.itype;
            itypeCell.classList.add('text-truncate');
            itypeCell.style.maxWidth = '150px';
            row.appendChild(itypeCell);

            const cCodeCell = document.createElement('td');
            cCodeCell.textContent = book.col_code;
            cCodeCell.classList.add('text-truncate');
            cCodeCell.style.maxWidth = '150px';
            row.appendChild(cCodeCell);

            const titleCell = document.createElement('td');
            titleCell.textContent = book.title;
            titleCell.classList.add('text-truncate');
            titleCell.style.maxWidth = '150px';
            row.appendChild(titleCell);

            const authorCell = document.createElement('td');
            authorCell.textContent = book.author;
            authorCell.classList.add('text-truncate');
            authorCell.style.maxWidth = '150px';
            row.appendChild(authorCell);

            const publisherCell = document.createElement('td');
            publisherCell.textContent = book.publisher_code;
            publisherCell.classList.add('text-truncate');
            publisherCell.style.maxWidth = '150px';
            row.appendChild(publisherCell);

            const barcodeCell = document.createElement('td');
            barcodeCell.textContent = book.barcode;
            barcodeCell.classList.add('text-truncate');
            barcodeCell.style.maxWidth = '150px';
            row.appendChild(barcodeCell);

            const isbnCell = document.createElement('td');
            isbnCell.textContent = book.isbn;
            isbnCell.classList.add('text-truncate');
            isbnCell.style.maxWidth = '150px';
            row.appendChild(isbnCell);

            const copyNumCell = document.createElement('td');
            copyNumCell.textContent = book.copy_num;
            copyNumCell.classList.add('text-truncate');
            copyNumCell.style.maxWidth = '150px';
            row.appendChild(copyNumCell);

            const volumeCell = document.createElement('td');
            volumeCell.textContent = book.volume;
            volumeCell.classList.add('text-truncate');
            volumeCell.style.maxWidth = '150px';
            row.appendChild(volumeCell);

            // Append the row to the container
            booksContainer.appendChild(row);
        });
    })
    .catch(error => console.error('Error loading books:', error));
}

document.addEventListener('DOMContentLoaded', () => {
    loadBooks();
    
    // Add click event listener to dashboard link
    const dashboardLink = document.querySelector('a[href="/admin/list-books/"]');
    if (dashboardLink) {
        dashboardLink.addEventListener('click', (e) => {
            e.preventDefault();
            loadBooks();
        });
    }
});