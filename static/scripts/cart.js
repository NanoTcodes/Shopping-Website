function remFromCart(productId) {
	// Make an Ajax request to remove the product from the cart
	$.ajax({
		type: 'POST',  // You can use POST or other appropriate HTTP methods
		url: '/rem_from_cart',  // Specify the Flask route to handle removal
		data: { 'product_id': productId },  // Send the product ID to the server
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