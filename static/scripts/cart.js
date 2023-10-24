function remFromCart(productId) {
	// Make an Ajax request to remove the product from the cart
	$.ajax({
		type: 'POST',  // You can use POST or other appropriate HTTP methods
		url: '/rem_from_cart',  // Specify the Flask route to handle removal
		data: { 'product_id': productId },  // Send the product ID to the server
	});
}
