document.addEventListener('DOMContentLoaded', () => {

    const loginForm =
        document.getElementById('login-form');

    if (loginForm) {
        loginForm.addEventListener(
            'submit',
            loginHandler
        );
    }

    if (
        document.getElementById(
            'places-list'
        )
    ) {

        checkIndexAuthentication();
        setupPriceFilter();
    }

    if (
        document.getElementById(
            'place-details'
        )
    ) {

        loadPlacePage();
    }

    if (
        document.getElementById(
            'review-form'
        ) &&
        window.location.pathname.includes(
            'add_review'
        )
    ) {

        setupReviewPage();
    }
});

/* ==========================
   LOGIN
========================== */

async function loginHandler(event) {

    event.preventDefault();

    const email =
        document.getElementById(
            'email'
        ).value;

    const password =
        document.getElementById(
            'password'
        ).value;

    try {

        const response =
            await fetch(
                'http://127.0.0.1:5000/api/v1/auth/login',
                {
                    method: 'POST',
                    headers: {
                        'Content-Type':
                        'application/json'
                    },
                    body: JSON.stringify({
                        email,
                        password
                    })
                }
            );

        if (response.ok) {

            const data =
                await response.json();

            document.cookie =
                `token=${data.access_token}; path=/`;

            window.location.href =
                'index.html';

        } else {

            alert(
                'Login failed'
            );
        }

    } catch (error) {

        console.error(error);

        alert(
            'Unable to connect to API'
        );
    }
}

/* ==========================
   COOKIES
========================== */

function getCookie(name) {

    const cookies =
        document.cookie.split(';');

    for (let cookie of cookies) {

        cookie = cookie.trim();

        if (
            cookie.startsWith(
                name + '='
            )
        ) {

            return cookie.substring(
                name.length + 1
            );
        }
    }

    return null;
}

/* ==========================
   INDEX PAGE
========================== */

function checkIndexAuthentication() {

    const token =
        getCookie('token');

    const loginLink =
        document.getElementById(
            'login-link'
        );

    if (!token) {

        if (loginLink) {
            loginLink.style.display =
                'block';
        }

    } else {

        if (loginLink) {
            loginLink.style.display =
                'none';
        }

        fetchPlaces(token);
    }
}

let allPlaces = [];

async function fetchPlaces(token) {

    try {

        const response =
            await fetch(
                'http://127.0.0.1:5000/api/v1/places/',
                {
                    headers: {
                        Authorization:
                        `Bearer ${token}`
                    }
                }
            );

        const places =
            await response.json();

        allPlaces = places;

        displayPlaces(allPlaces);

    } catch (error) {

        console.error(error);
    }
}

function displayPlaces(places) {

    const placesList =
        document.getElementById(
            'places-list'
        );

    if (!placesList) {
        return;
    }

    placesList.innerHTML = '';

    places.forEach(place => {

        const card =
            document.createElement(
                'div'
            );

        card.className =
            'place-card';

        card.setAttribute(
            'data-price',
            place.price
        );

        card.innerHTML = `
            <h3>${place.title}</h3>
            <p>Price per night: $${place.price}</p>
            <a href="place.html?id=${place.id}"
               class="details-button">
               View Details
            </a>
        `;

        placesList.appendChild(card);
    });
}

function setupPriceFilter() {

    const filter =
        document.getElementById(
            'price-filter'
        );

    if (!filter) {
        return;
    }

    filter.innerHTML = `
        <option value="all">All</option>
        <option value="10">10</option>
        <option value="50">50</option>
        <option value="100">100</option>
    `;

    filter.addEventListener(
        'change',
        filterPlaces
    );
}

function filterPlaces(event) {

    const selectedPrice =
        event.target.value;

    const cards =
        document.querySelectorAll(
            '.place-card'
        );

    cards.forEach(card => {

        const placePrice =
            Number(
                card.getAttribute(
                    'data-price'
                )
            );

        if (
            selectedPrice === 'all' ||
            placePrice <= Number(selectedPrice)
        ) {

            card.style.display =
                'block';

        } else {

            card.style.display =
                'none';
        }
    });
}

/* ==========================
   PLACE DETAILS
========================== */

function getPlaceIdFromURL() {

    const params =
        new URLSearchParams(
            window.location.search
        );

    return params.get('id');
}

function loadPlacePage() {

    const token =
        getCookie('token');

    const addReviewSection =
        document.getElementById(
            'add-review'
        );

    if (addReviewSection) {

        if (token) {
            addReviewSection.style.display =
                'block';
        } else {
            addReviewSection.style.display =
                'none';
        }
    }

    const placeId =
        getPlaceIdFromURL();

    fetchPlaceDetails(
        token,
        placeId
    );
}

async function fetchPlaceDetails(
    token,
    placeId
) {

    try {

        const headers = {};

        if (token) {
            headers.Authorization =
                `Bearer ${token}`;
        }

        const response =
            await fetch(
                `http://127.0.0.1:5000/api/v1/places/${placeId}`,
                {
                    headers
                }
            );

        const place =
            await response.json();

        displayPlaceDetails(
            place
        );

    } catch (error) {

        console.error(error);
    }
}

function displayPlaceDetails(place) {

    const container =
        document.getElementById(
            'place-details'
        );

    if (!container) {
        return;
    }

    container.innerHTML = `
        <h2>${place.title}</h2>

        <p>
            ${place.description || ''}
        </p>

        <p>
            Price:
            $${place.price}
        </p>
    `;
}

/* ==========================
   ADD REVIEW
========================== */

function setupReviewPage() {

    const token =
        checkReviewAuthentication();

    const placeId =
        getPlaceIdFromURL();

    const placeLabel =
        document.getElementById(
            'place-id-display'
        );

    if (placeLabel) {

        placeLabel.textContent =
            `Place ID: ${placeId}`;
    }

    const reviewForm =
        document.getElementById(
            'review-form'
        );

    reviewForm.addEventListener(
        'submit',
        async (event) => {

            event.preventDefault();

            const reviewText =
                document.getElementById(
                    'review'
                ).value;

            const rating =
                document.getElementById(
                    'rating'
                ).value;

            await submitReview(
                token,
                placeId,
                reviewText,
                rating
            );
        }
    );
}

function checkReviewAuthentication() {

    const token =
        getCookie('token');

    if (!token) {

        window.location.href =
            'index.html';
    }

    return token;
}

async function submitReview(
    token,
    placeId,
    reviewText,
    rating
) {

    try {

        const response =
            await fetch(
                'http://127.0.0.1:5000/api/v1/reviews/',
                {
                    method: 'POST',
                    headers: {
                        'Content-Type':
                        'application/json',
                        Authorization:
                        `Bearer ${token}`
                    },
                    body: JSON.stringify({
                        place_id: placeId,
                        text: reviewText,
                        rating: Number(rating)
                    })
                }
            );

        if (response.ok) {

            alert(
                'Review submitted successfully!'
            );

            document.getElementById(
                'review-form'
            ).reset();

        } else {

            const error =
                await response.json();

            alert(
                error.error ||
                'Failed to submit review'
            );
        }

    } catch (error) {

        console.error(error);

        alert(
            'Unable to submit review'
        );
    }
}
