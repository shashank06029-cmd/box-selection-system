# AI-Assisted Box Selection System

A Django-based shipping box recommendation system that selects a suitable shipping box for an order based on product dimensions, product weight, box dimensions, maximum weight capacity, and box cost.

## Features

- Product management through Django Admin
- Shipping box management through Django Admin
- Order creation through REST API
- Product listing API
- Automatic box recommendation
- Product quantity support
- Product rotation support
- Total order weight calculation
- Lowest-cost valid box selection
- Handles orders for which no suitable box exists
- Responsive frontend interface
- Django REST Framework API
- Automated test suite
- Admin panel for managing products, boxes, orders, and order items

## Technology Stack

- Python
- Django 6.1.1
- Django REST Framework 3.18.1
- SQLite
- HTML5
- CSS3
- JavaScript

## Project Structure

box_selection_system/
│
├── boxes/
│   ├── migrations/
│   ├── static/
│   │   └── boxes/
│   │       ├── app.js
│   │       └── style.css
│   │
│   ├── templates/
│   │   └── boxes/
│   │       └── index.html
│   │
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── services.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── manage.py
├── requirements.txt
├── .gitignore
├── README.md
├── AI_USAGE.md
└── TEST_OUTPUT.md

## Data Models

### Product

Stores the products that can be added to an order.

Fields:

- Name
- Length
- Width
- Height
- Weight

### Box

Stores the available shipping boxes.

Fields:

- Name
- Internal Length
- Internal Width
- Internal Height
- Maximum Weight
- Cost

### Order

Represents a customer order.

Fields:

- ID
- Created At

### OrderItem

Connects products with an order and stores the requested quantity.

Fields:

- Order
- Product
- Quantity

## Box Recommendation Logic

The recommendation process follows these steps:

1. Validate the incoming order.
2. Calculate the total order weight.
3. Expand product quantities into individual products.
4. Check all available boxes.
5. Reject boxes that cannot support the total order weight.
6. Check whether the products can fit inside the box.
7. Consider different orientations of each product.
8. Check product positions for overlap.
9. Keep boxes that satisfy the packing requirements.
10. Select the valid box with the lowest cost.
11. Return the selected box through the API.

The packing implementation is a heuristic 3D placement approach. It checks different product orientations and prevents overlapping placements, but it is not an exhaustive mathematical bin-packing solver.

## API Endpoints

### Product List

GET /api/products/

Returns all available products.

Example response:

[
    {
        "id": 1,
        "name": "Laptop",
        "length": "30.00",
        "width": "20.00",
        "height": "5.00",
        "weight": "2.00"
    }
]

### Box Recommendation

POST /api/recommend-box/

Request:

{
    "items": [
        {
            "product": 1,
            "quantity": 1
        }
    ]
}

Successful response:

{
    "success": true,
    "order_id": 1,
    "recommended_box": {
        "id": 2,
        "name": "Medium Box",
        "cost": 50.0,
        "max_weight": 5.0
    },
    "total_weight": 2.0
}

If no suitable box exists:

{
    "success": false,
    "message": "No suitable box found.",
    "total_weight": 20.0
}

## Admin Panel

The Django Admin panel is used to manage:

- Products
- Boxes
- Orders
- Order Items

Open:

http://127.0.0.1:8000/admin/

## Installation

Clone the repository:

git clone <YOUR_GITHUB_REPOSITORY_URL>

Move into the project directory:

cd box_selection_system

Create a virtual environment:

python -m venv venv

Activate the virtual environment on Windows:

.\venv\Scripts\Activate.ps1

Install dependencies:

pip install -r requirements.txt

Run migrations:

python manage.py migrate

Create an admin user:

python manage.py createsuperuser

Start the development server:

python manage.py runserver

Open the application:

http://127.0.0.1:8000/

## Testing

Run the automated test suite:

python manage.py test

Run Django system checks:

python manage.py check

The test suite covers:

- Single product recommendation
- Multiple product recommendation
- Quantity handling
- Multiple quantity recommendation
- Product rotation
- Empty orders
- Invalid products
- Invalid quantities
- Empty item validation
- No suitable box
- Lowest-cost valid box selection

## Example Test Data

### Products

| Product | Dimensions | Weight |
|---|---|---:|
| Laptop | 30 × 20 × 5 | 2 kg |
| Mouse | 10 × 6 × 4 | 0.2 kg |
| Oversized TV | 100 × 100 × 100 | 20 kg |

### Boxes

| Box | Internal Dimensions | Max Weight | Cost |
|---|---|---:|---:|
| Small Box | 25 × 20 × 10 | 3 kg | ₹30 |
| Medium Box | 35 × 25 × 15 | 5 kg | ₹50 |
| Large Box | 50 × 40 × 30 | 10 kg | ₹80 |

## Frontend

The frontend allows users to:

1. Select a product.
2. Enter a quantity.
3. Add the product to the order.
4. View product dimensions and weight.
5. Add multiple products.
6. Remove products.
7. Request a box recommendation.
8. View the recommended box.
9. View total order weight.
10. Handle cases where no suitable box is available.

## Application Flow

User
↓
Select Product
↓
Enter Quantity
↓
Add Product
↓
Create Order
↓
Recommendation API
↓
Calculate Weight
↓
Check Box Dimensions
↓
Check Product Orientation
↓
Check Product Placement
↓
Filter Valid Boxes
↓
Select Lowest-Cost Valid Box
↓
Display Recommendation

## AI Usage

AI assistance was used during development for guidance, implementation suggestions, debugging, code review, and testing support.

Detailed AI usage, prompts, accepted and rejected suggestions, mistakes, and verification steps are documented separately in:

AI_USAGE.md

The AI-assisted development process was manually verified by running the Django system checks, automated tests, API tests, and frontend tests.

## Test Output

The actual test execution output is documented separately in:

TEST_OUTPUT.md

## Limitations

The current packing algorithm uses a heuristic 3D placement approach.

It supports:

- Product rotation
- Product quantities
- Weight constraints
- Box dimension constraints
- Basic three-dimensional placement
- Overlap checking

However, it does not guarantee a mathematically optimal packing arrangement for every possible combination of products.

A production logistics system could use more advanced optimization techniques for complex packing scenarios.

## Security and Validation

The application validates:

- Product existence
- Quantity greater than zero
- At least one product per order
- Maximum box weight
- Product dimensions
- CSRF protection for frontend API requests

## Error Handling

If no suitable box is available, the API returns an appropriate error response instead of creating an invalid order.

Example:

{
    "success": false,
    "message": "No suitable box found.",
    "total_weight": 20.0
}

## Development Commands

Start server:

python manage.py runserver

Run tests:

python manage.py test

Run system check:

python manage.py check

Create migrations:

python manage.py makemigrations

Apply migrations:

python manage.py migrate

Create admin user:

python manage.py createsuperuser

## Future Improvements

Possible future improvements include:

- Advanced 3D bin-packing optimization
- Multiple box recommendations
- Better packing visualization
- Box inventory management
- Authentication and user roles
- PostgreSQL support
- Docker deployment
- Production deployment
- API documentation using Swagger/OpenAPI
- More extensive edge-case testing

## Assignment Deliverables

The final submission should contain:

- GitHub repository
- README.md
- AI_USAGE.md
- TEST_OUTPUT.md
- Exported AI chat transcript
- Source code
- Automated tests
- Test execution output
- Final ZIP archive

## License

This project was developed as a technical assignment.