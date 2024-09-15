 // JavaScript function to handle form submission via AJAX
 function registerCustomer(event) {
    event.preventDefault(); // Prevent the form from submitting the traditional way

    const formData = {
        name: document.getElementById('customer_name').value,
        email: document.getElementById('customer_email').value,
        phone: document.getElementById('customer_contact').value,
        city: document.getElementById('customer_city').value,
        address: document.getElementById('customer_address').value,
        password: document.getElementById('inputPassword').value
    };

    fetch('/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
    })
    .then(response => {
        if (response.redirected) {
            window.location.href = response.url;  // Redirect to login
        }
        return response.json();
    })
    .then(data => {
        if (!data.success) {
            alert('Registration failed: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// JavaScript function to handle logout
document.getElementById('logoutBtn').addEventListener('click', function () {
    fetch('/logout')
    .then(response => response.redirected ? window.location.href = response.url : null)
    .catch(error => console.error('Error:', error));
});


function registerAgency(event) {
    event.preventDefault(); // Prevent the form from submitting the traditional way

    const formData = {
        name: document.getElementById('agent_name').value,
        email: document.getElementById('agent_email').value,
        phone: document.getElementById('agent_contact').value,
        city: document.getElementById('agent_city').value,
        address: document.getElementById('agent_address').value,
        password: document.getElementById('inputPassword').value
    };

    fetch('/registerAgency', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Registration successful!');
        } else {
            alert('Registration failed: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function registerDriver(event) {
    event.preventDefault(); // Prevent the form from submitting the traditional way

    const formData = {
        name: document.getElementById('driver_name').value,
        email: document.getElementById('driver_email').value,
        phone: document.getElementById('driver_contact').value,
        city: document.getElementById('driver_city').value,
        address: document.getElementById('driver_address').value,
        password: document.getElementById('inputPassword').value
    };

    fetch('/registerDriver', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Registration successful!');
        } else {
            alert('Registration failed: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
