import json
from unittest.mock import mock_open
from src.utils import load_json_data

fake_data = [{"id": 1, "name": "Item 1"}, {"id": 2, "name": "Item 2"}]

def test_read_json_successfully(mocker):
    mocker.patch("src.utils.open", mock_open(read_data=json.dumps(fake_data)))

    result = load_json_data("path/to/file.json")

    assert result == fake_data

def test_read_json_fails_on_exception(mocker):
    mocker.patch("src.utils.open", mock_open())

    mocker.patch("json.load", side_effect=Exception("JSON decoding error"))

    result = load_json_data("path/to/file.json")

    assert result == []

def test_read_json_empty_file(mocker):
    mocker.patch("src.utils.open", mock_open(read_data=""))

    result = load_json_data("path/to/file.json")

    assert result == []