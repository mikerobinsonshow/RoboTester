import app


def test_validate_only_submitted_fields():
    errors = app.validate_data({"first_name": "John"})
    assert "email" not in errors


def test_validate_required_field_present_but_empty():
    errors = app.validate_data({"email": ""})
    assert "email" in errors
