INSERT INTO users (
    id,
    first_name,
    last_name,
    email,
    password,
    is_admin
)
VALUES (
    '00000000-0000-0000-0000-000000000001',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$wzW6G6zAo0jP6R5Wx7H3XOc3C7Y4jL6Hg5uZ3I3e4mR6f9s8Q2VbW',
    TRUE
);

INSERT INTO amenities (
    id,
    name
)
VALUES
(
    '10000000-0000-0000-0000-000000000001',
    'Wi-Fi'
),
(
    '10000000-0000-0000-0000-000000000002',
    'Swimming Pool'
),
(
    '10000000-0000-0000-0000-000000000003',
    'Air Conditioning'
),
(
    '10000000-0000-0000-0000-000000000004',
    'Parking'
);
