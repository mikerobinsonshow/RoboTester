import app





def test_generate_pdf_uses_manual_wkhtmltopdf_path(monkeypatch):
    called = {}

    def fake_configuration(wkhtmltopdf):
        called["path"] = wkhtmltopdf
        return "cfg"

    def fake_from_string(html, path, configuration=None):
        assert configuration == "cfg"

    monkeypatch.setenv("WKHTMLTOPDF_CMD", "custom-path")
    monkeypatch.setattr(app.pdfkit, "configuration", fake_configuration)
    monkeypatch.setattr(app.pdfkit, "from_string", fake_from_string)
    with app.app.test_request_context():
        result = app.generate_pdf({})
    assert called["path"] == "custom-path"
    assert isinstance(result, tuple)

