import app


def test_validate_only_submitted_fields():
    errors = app.validate_data({"first_name": "John"})
    assert "email" not in errors


def test_validate_required_field_present_but_empty():
    errors = app.validate_data({"email": ""})
    assert "email" in errors


def test_validate_ssn_format():
    errors = app.validate_data({"ssn": "123456789"})
    assert "ssn" in errors


def test_validate_date_format():
    errors = app.validate_data({"date_of_birth": "01/01/1990"})
    assert "date_of_birth" in errors


def test_validate_zip_format():
    errors = app.validate_data({"zip_code": "1234"})
    assert "zip_code" in errors


def test_validate_state_format():
    errors = app.validate_data({"state": "California"})
    assert "state" in errors
