Little Lemon Capstone - API paths for peer review
==================================================

Setup
-----
1. Create a MySQL database named "reservations" (or set DB_NAME env var).
2. Set DB_USER / DB_PASSWORD / DB_HOST / DB_PORT env vars to match your MySQL setup
   (defaults: root / "" / 127.0.0.1 / 3306).
3. pipenv install
4. python manage.py migrate
5. python manage.py createsuperuser
6. python manage.py runserver

Authentication
---------------
/auth/users/                 POST   - register a new user
/auth/token/login/           POST   - obtain auth token (Djoser, username + password)
/auth/token/logout/          POST   - invalidate auth token
/auth/users/me/              GET    - view the current authenticated user

For authenticated requests, add header:
Authorization: Token <token>

Menu API
--------
/api/menu/                   GET    - list all menu items (no auth required)
/api/menu/                   POST   - create a menu item (auth required)
/api/menu/<id>/               GET    - retrieve a single menu item
/api/menu/<id>/               PUT    - update a menu item (auth required)
/api/menu/<id>/               DELETE - delete a menu item (auth required)

Booking API
-----------
/api/bookings/                GET    - list bookings, optionally filter with ?date=YYYY-MM-DD (auth required)
/api/bookings/                POST   - create a booking (auth required)
/api/bookings/<id>/            GET    - retrieve a single booking (auth required)
/api/bookings/<id>/            PUT    - update a booking (auth required)
/api/bookings/<id>/            DELETE - delete a booking (auth required)

HTML pages (Django templates)
------------------------------
/                              Home page
/about/                        About page
/menu/                         Menu page
/menu_item/<id>/               Menu item detail page
/book/                         Table booking form
/bookings/                     JSON bookings by date (legacy view)

Tests
-----
python manage.py test restaurant
