import json
import os
import random
import re
import uuid
from datetime import datetime

from flask import (
    Flask,
    jsonify,
    render_template,
    request,
    send_from_directory,
    url_for,
)

import pdfkit

app = Flask(__name__)

with open("data/fields.json") as f:
    ALL_FIELDS = json.load(f)

PDF_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pdf")
os.makedirs(PDF_DIR, exist_ok=True)


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
    html = render_template("pdf_template.html", data=data, fields=ALL_FIELDS)
    filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex}.pdf"
    path = os.path.join(PDF_DIR, filename)
    try:
        pdfkit.from_string(html, path)
    except (OSError, pdfkit.PDFKitError) as e:
        app.logger.error("PDF generation failed: %s", e)
        return {"error": f"PDF generation failed: {e}"}
    return path, filename


@app.route("/submit", methods=["POST"])
def submit():
    data = request.get_json() or {}
    errors = validate_data(data)
    if errors:
        return jsonify({"errors": errors}), 400

    result = generate_pdf(data)
    if isinstance(result, dict) and result.get("error"):
        return jsonify(result), 500

    path, filename = result
    return jsonify(
        {
            "message": "PDF generated",
            "pdf_path": path,
            "pdf_url": url_for("get_pdf", filename=filename),
        }
    )


@app.route("/pdf/<path:filename>")
def get_pdf(filename):
    return send_from_directory(PDF_DIR, filename)


if __name__ == '__main__':
    app.run(debug=True)
