import json
import random
import re
from io import BytesIO
from flask import Flask, jsonify, render_template, request, send_file
from reportlab.pdfgen import canvas

app = Flask(__name__)

with open('data/fields.json') as f:
    ALL_FIELDS = json.load(f)


@app.route('/schema')
def schema():
    fields = ALL_FIELDS[:]
    random.shuffle(fields)
    count = random.randint(1, len(fields))
    return jsonify(fields[:count])


@app.route('/')
def index():
    return render_template('index.html')


def within_length(value, max_len=15):
    return len(value) <= max_len


def is_valid_phone(value):
    digits = re.sub(r"\D", "", value)
    return bool(re.fullmatch(r"\d{10}", digits))


def is_valid_ssn(value):
    return bool(re.fullmatch(r"\d{3}-\d{2}-\d{4}", value))


def validate_data(data):
    errors = {}
    for field in ALL_FIELDS:
        name = field["name"]
        rules = field.get("validation", {})
        value = data.get(name)

        if isinstance(value, str):
            value_stripped = value.strip()
        else:
            value_stripped = value

        field_errors = []

        if rules.get("required") and (value_stripped is None or value_stripped == ""):
            field_errors.append(f"{name} is required")

        if isinstance(value_stripped, str) and value_stripped:
            if not within_length(value_stripped):
                field_errors.append(f"{name} must be at most 15 characters")

            lname = name.lower()
            if "phone" in lname and not is_valid_phone(value_stripped):
                field_errors.append("Phone number must be 10 digits")

            if "ssn" in lname and not is_valid_ssn(value_stripped):
                field_errors.append("SSN must match ###-##-####")

            min_len = rules.get("minLength")
            if min_len and len(value_stripped) < min_len:
                field_errors.append(f"{name} must be at least {min_len} characters")

        if value_stripped not in (None, ""):
            try:
                numeric_val = float(value_stripped)
            except (TypeError, ValueError):
                numeric_val = None

            if numeric_val is not None:
                if rules.get("min") is not None and numeric_val < rules["min"]:
                    field_errors.append(f"{name} must be at least {rules['min']}")
                if rules.get("max") is not None and numeric_val > rules["max"]:
                    field_errors.append(f"{name} must be at most {rules['max']}")

        if field_errors:
            errors[name] = field_errors

    return errors


def generate_pdf(data):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)
    y = 800
    for field in ALL_FIELDS:
        name = field["name"]
        label = field.get("label", name)
        value = data.get(name, "")
        pdf.drawString(72, y, f"{label}: {value}")
        y -= 20
    pdf.save()
    buffer.seek(0)
    return buffer


@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json() or {}
    errors = validate_data(data)
    if errors:
        return jsonify({"errors": errors}), 400

    pdf_buffer = generate_pdf(data)
    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name="submission.pdf",
        mimetype="application/pdf",
    )


if __name__ == '__main__':
    app.run(debug=True)
