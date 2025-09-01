import json
import random

import app


def test_schema_shuffles_order():
    with open('data/fields.json') as f:
        all_fields = json.load(f)

    random.seed(0)
    expected = list(all_fields)
    random.shuffle(expected)
    expected_names = [f['name'] for f in expected]

    client = app.app.test_client()
    random.seed(0)
    res = client.get('/schema')
    assert res.status_code == 200
    data = res.get_json()
    names = [f['name'] for f in data]
    assert names == expected_names
