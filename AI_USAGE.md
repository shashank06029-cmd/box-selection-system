# AI Usage

## AI Tool Used

ChatGPT was used as a development assistant during this project.

I used AI mainly for reference, implementation suggestions, debugging, and reviewing different approaches while building the application.

## My Development Approach

The project was developed using Python, Django, Django REST Framework, HTML, CSS, and JavaScript.

I worked with the Django project structure, models, relationships, REST APIs, validation, frontend integration, and testing as part of the implementation.

AI suggestions were used where they helped speed up development or provided an alternative approach. The suggestions were reviewed and adapted according to the requirements of the assignment.

## Areas Where AI Assisted

AI was used for:

- Django project and application structure
- Model design suggestions
- Django REST Framework implementation
- Serializer and API validation
- Box recommendation logic
- Product rotation and basic packing logic
- Test case ideas
- Frontend HTML, CSS, and JavaScript
- Debugging syntax and implementation issues
- Code review and improvement suggestions

## Example of AI-Assisted Development

For the box recommendation feature, AI helped with ideas for checking:

- Total order weight
- Box maximum weight
- Product dimensions
- Different product orientations
- Product placement
- Overlapping products
- Selecting the lowest-cost valid box

The final implementation was tested with the project's actual products and boxes.

## Changes During Development

Some approaches were changed after testing.

For example, an early frontend approach was changed to use a dedicated `/api/products/` endpoint instead of depending on Django Admin data.

There was also a development mistake where JavaScript code was accidentally placed inside `apps.py`. This produced Python/Pylance errors. The file was corrected and the project was checked again.

## Verification

AI suggestions were not considered final without testing.

The project was verified using:

- `python manage.py check`
- `python -m pip check`
- `python manage.py test`
- Manual API testing
- Manual frontend testing

The final automated test run completed successfully:

- 11 tests
- 11 passed
- 0 failed
- 0 errors

Django system check also completed successfully with no issues.

## AI Limitations

The packing algorithm implemented in this project is a heuristic approach. It handles product orientations, dimensions, weight limits, and basic placement and overlap checks, but it is not an exhaustive mathematical bin-packing solver.

The implementation was therefore tested against the defined assignment scenarios rather than being treated as guaranteed optimal for every possible combination.

## Final Note

AI was used as a development assistant, not as a replacement for understanding or verification.

The code was reviewed, adapted to the project requirements, executed locally, and tested before being included in the final submission.