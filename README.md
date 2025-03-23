## Maxicom - Book Inventory Management System (BIMS)
Maxicom-BIMS is a Book Inventory Management System developed for UM Digos City - LIC. The purpose of this system is to streamline and enhance the inventory process for library staff, providing a more efficient and user-friendly solution for managing books and their statuses.



## Features


- **Barcode Scanning**: Scan barcodes to quickly input book details and conditions.
- **Book Condition and Remarks**: Submit the state of books during inventory.
- **Book Management**:
  - Add, edit, and delete books.
  - View the conditions of books.
  - Track counts of registered and unregistered books.
- **Inventory Insights**:
  - Monitor the condition of scanned books.
  - View "Found" and "Not Found" book statuses during periodic inventories.
- **Reporting**:
  - Export data to Excel for documentation.
  - Render detailed book information into PDF format.
- **User Management**:
  - Manage system users and permissions.

## Technologies Used

- **Backend**: Django  
- **Database**: PostgreSQL  
- **Frontend**: Bootstrap  
- **Barcode Scanning**: QuaggaJS  
- **Deployment**: Nginx + Gunicorn  

## Installation Guide

**Prerequisites**
- Python 3.x  
- PostgreSQL  
- HTTPS setup (required for QuaggaJS camera access)  

**Installation Steps**

1. Clone the repository:

   ```bash
   git clone <repository_url>
   cd maxicom-bims
2. Install dependencies:
    ```bash 
    pip install django-extensions==3.2.3 pyOpenSSL==24.2.1 Werkzeug==3.1.2
3. Add django-extensions to INSTALLED_APPS in your project settings:
    ```python
    INSTALLED_APPS = [
    # other apps
    'django_extensions',
    ]
4. Run the development server with HTTPS:
    ```bash
    ./manage.py runserver_plus --cert-file cert.crt 0.0.0.0:8000 
## Usage

**Users**:
   - Create an account by signing up.
   - Log in to the system.
   - Scan or input barcode numbers to submit book conditions and remarks during inventory.

**Admins**:
   - Manage book entries (add, edit, delete).
   - Monitor inventory and book statuses.
   - Export data for reporting and documentation.
   - Generate PDFs of book details.
