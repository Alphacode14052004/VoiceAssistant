document.addEventListener('DOMContentLoaded', function() {
    const jsonFilePath = 'data.json';  // Adjusted path for accessing JSON data
    const imageDirectory = 'imgs/';    // Directory for images
    const cart = [];
    const cartCountElement = document.querySelector('.cart-count');
    const cartOverlay = document.getElementById('cart-overlay');
    const cartItemsElement = document.getElementById('cart-items');
    const cartButton = document.querySelector('.cart');
    const closeCartButton = document.getElementById('close-cart');
    const notification = document.getElementById('notification');

    fetch(jsonFilePath)
        .then(response => response.json())
        .then(data => {
            const menuData = data["KFC MENU CHENNAI"];
            const menuDiv = document.getElementById('menu');

            menuData.forEach(item => {
                const menuItemDiv = document.createElement('div');
                menuItemDiv.classList.add('menu-item');

                const itemImage = document.createElement('img');
                itemImage.src = imageDirectory + item.image;
                itemImage.alt = item.Deal;

                const itemName = document.createElement('h3');
                itemName.textContent = item.Deal;

                const itemDescription = document.createElement('p');
                itemDescription.textContent = item.Description;

                const itemSavings = document.createElement('p');
                itemSavings.classList.add('savings');
                itemSavings.textContent = item.Savings;

                const itemPrice = document.createElement('p');
                itemPrice.classList.add('price');
                itemPrice.textContent = `Price: Rs. ${item["Price (in Rs.)"]}`;

                const addToCartButton = document.createElement('button');
                addToCartButton.classList.add('add-to-cart');
                addToCartButton.textContent = 'Add to Cart';
                addToCartButton.addEventListener('click', () => addToCart(item));

                menuItemDiv.appendChild(itemImage);
                menuItemDiv.appendChild(itemName);
                menuItemDiv.appendChild(itemDescription);
                menuItemDiv.appendChild(itemSavings);
                menuItemDiv.appendChild(itemPrice);
                menuItemDiv.appendChild(addToCartButton);

                menuDiv.appendChild(menuItemDiv);
            });
        })
        .catch(error => console.error('Error fetching JSON data:', error));

    function addToCart(item) {
        cart.push(item);
        updateCartCount();
        showNotification();
    }

    function updateCartCount() {
        cartCountElement.textContent = cart.length;
    }

    cartButton.addEventListener('click', () => {
        cartOverlay.classList.add('active');
        displayCartItems();
    });

    closeCartButton.addEventListener('click', () => {
        cartOverlay.classList.remove('active');
    });

    function displayCartItems() {
        cartItemsElement.innerHTML = '';
        cart.forEach(item => {
            const cartItemDiv = document.createElement('div');
            cartItemDiv.classList.add('cart-item');

            const itemImage = document.createElement('img');
            itemImage.src = imageDirectory + item.image;
            itemImage.alt = item.Deal;

            const itemDetails = document.createElement('div');
            const itemName = document.createElement('p');
            itemName.textContent = item.Deal;

            const itemPrice = document.createElement('p');
            itemPrice.textContent = `Price: Rs. ${item["Price (in Rs.)"]}`;

            itemDetails.appendChild(itemName);
            itemDetails.appendChild(itemPrice);

            cartItemDiv.appendChild(itemImage);
            cartItemDiv.appendChild(itemDetails);

            cartItemsElement.appendChild(cartItemDiv);
        });
    }

    function showNotification() {
        notification.classList.add('show');
        setTimeout(() => {
            notification.classList.remove('show');
        }, 2000);
    }

    function proceedToPayment() {
        const name = "John Doe"; // Replace with actual user input
        const mobile = "1234567890"; // Replace with actual user input
        const cartDetails = JSON.stringify(cart); // Convert cart array to JSON string

        fetch('http://127.0.0.1:5000/submit_order', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name: name,
                mobile: mobile,
                cart_details: cartDetails
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                alert(data.message);
                window.location.href = "payment.html"; // Replace with your payment page URL
            } else {
                alert('Failed to submit order');
            }
        })
        .catch(error => console.error('Error:', error));
    }

    document.getElementById('proceed-to-pay').addEventListener('click', proceedToPayment);

});
