function remFromCart(productId) {
	// Create a data object to send as JSON
	const data = { product_id: productId };

	// Define the options for the fetch request
	const options = {
		method: 'POST',  // You can use other HTTP methods as needed
		body: JSON.stringify(data),
		headers: {
			'Content-Type': 'application/json'
		}
	};

	fetch('/rem_from_cart', options)
		.then(response => {
			if (response.ok) {
				console.log('Sent');
				// You can add code here to handle the response if needed
			} else {
				console.error('Error:', response.status);
				// Handle the error if the request is not successful
			}
		})
		.catch(error => {
			console.error('Fetch Error:', error);
			// Handle errors that occur during the fetch request
		});
}

    // Function to handle the "Add to Cart" button click
    document.querySelectorAll('.addToCartButton').forEach(function(button) {
        button.addEventListener('click', function() {
            var productId = button.getAttribute('data-product-id');
            addToCart(productId);
        });
    });

    // Function to send an AJAX request to add the product to the cart
    function addToCart(productId) {
        // Send an AJAX request to the server to add the product to the cart
        // You can use JavaScript libraries like Axios or the native Fetch API to send the request.
        // Here's an example using the Fetch API:
        fetch('/add_to_cart', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                product_id: productId,
                quantity: 1, // You can allow users to specify the quantity if needed
            }),
        })
            .then(function(response) {
                return response.json();
            })
            .then(function(data) {
                if (data.success) {
                    alert('Product added to the cart.');
                } else {
                    alert('Failed to add the product to the cart.');
                }
            })
            .catch(function(error) {
                console.error('Error:', error);
            });
    }