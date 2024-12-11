function printPage(url) {
    // This uses the Djangourl from the print button
    var printUrl = url;
    
    fetch(printUrl)
        .then(response => response.text())
        .then(content => {
            const iframe = document.createElement('iframe');
            iframe.style.display = 'none';
            document.body.appendChild(iframe);
            
            iframe.contentWindow.document.write(content);
            iframe.contentWindow.document.close();
            
            iframe.contentWindow.onload = function() {
                iframe.contentWindow.print();
                document.body.removeChild(iframe);
            };
        })
        .catch(error => {
            console.error('Error fetching print content:', error);
        });
}