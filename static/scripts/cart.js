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
