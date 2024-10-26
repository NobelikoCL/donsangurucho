let carrito = JSON.parse(localStorage.getItem('carrito')) || [];

function agregarAlCarrito(productoId, nombre, precio) {
    fetch('/agregar-al-carrito/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: `producto_id=${productoId}&cantidad=1`
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error en la respuesta del servidor');
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            let item = carrito.find(i => i.id === productoId);
            if (item) {
                item.cantidad += 1;
            } else {
                carrito.push({id: productoId, nombre: nombre, precio: precio, cantidad: 1});
            }
            localStorage.setItem('carrito', JSON.stringify(carrito));
            mostrarPopup(`${nombre} agregado al carrito`);
            actualizarCarrito();
        } else {
            mostrarPopup('Error al agregar al carrito: ' + (data.error || 'Error desconocido'));
        }
    })
    .catch(error => {
        console.error('Error:', error);
        mostrarPopup('Error al agregar al carrito: ' + error.message);
    });
}

function actualizarCarrito() {
    let carritoItems = document.getElementById('carritoItems');
    let carritoContador = document.getElementById('carrito-contador');
    if (carritoItems) {
        carritoItems.innerHTML = '';
        let total = 0;
        let cantidadTotal = 0;
        carrito.forEach(item => {
            let subtotal = item.precio * item.cantidad;
            total += subtotal;
            cantidadTotal += item.cantidad;
            carritoItems.innerHTML += `
                <div class="d-flex justify-content-between align-items-center mb-2">
                    <span>${item.nombre} x ${item.cantidad}</span>
                    <span>$${subtotal}</span>
                </div>
            `;
        });
        carritoItems.innerHTML += `<hr><div class="d-flex justify-content-between"><strong>Total:</strong><strong>$${total}</strong></div>`;
    }
    if (carritoContador) {
        carritoContador.textContent = carrito.reduce((total, item) => total + item.cantidad, 0);
    }
}

function mostrarModal() {
    let myModal = new bootstrap.Modal(document.getElementById('carritoModal'));
    myModal.show();
}

function guardarCarritoEnLocalStorage() {
    localStorage.setItem('carrito', JSON.stringify(carrito));
}

function cargarCarritoDeLocalStorage() {
    let carritoGuardado = localStorage.getItem('carrito');
    if (carritoGuardado) {
        carrito = JSON.parse(carritoGuardado);
        actualizarCarrito();
    }
}

function irACheckout() {
    console.log('Redirigiendo a checkout...');
    window.location.href = '/checkout/';
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function mostrarPopup(mensaje) {
    let popup = document.getElementById('popup');
    if (!popup) {
        popup = document.createElement('div');
        popup.id = 'popup';
        popup.style.position = 'fixed';
        popup.style.top = '20px';
        popup.style.right = '20px';
        popup.style.backgroundColor = '#4CAF50';
        popup.style.color = 'white';
        popup.style.padding = '16px';
        popup.style.borderRadius = '4px';
        popup.style.zIndex = '1000';
        document.body.appendChild(popup);
    }
    popup.textContent = mensaje;
    popup.style.display = 'block';
    setTimeout(() => {
        popup.style.display = 'none';
    }, 3000);
}

function actualizarContadorCarrito() {
    fetch('/obtener-cantidad-carrito/')
        .then(response => response.json())
        .then(data => {
            document.getElementById('carrito-contador').textContent = data.cantidad;
        });
}

// Cargar el carrito cuando se inicia la página
document.addEventListener('DOMContentLoaded', function() {
    actualizarCarrito();
});
