import app


def test_generate_pdf_returns_error_on_failure(monkeypatch):
    def fake_from_string(html, path):
        raise OSError("wkhtmltopdf missing")
    monkeypatch.setattr(app.pdfkit, "from_string", fake_from_string)
    with app.app.test_request_context():
        result = app.generate_pdf({})
    assert "error" in result
    assert "PDF generation failed" in result["error"]
