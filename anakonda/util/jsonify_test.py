import pytest

from .jsonify import jsonify


@pytest.mark.order(1)
def test_jsonify():
    result = jsonify()
    assert type(result) is tuple
    assert len(result) == 3
    assert type(result[0]) is dict
    assert type(result[1]) is int
    assert type(result[2]) is dict
    assert "result" in result[0]
    assert "metadata" in result[0]
    assert "status" in result[0]
    assert "code" in result[0]["status"]
    assert "message" in result[0]["status"]
    assert result[1] == 200
    assert result[2] == {}
