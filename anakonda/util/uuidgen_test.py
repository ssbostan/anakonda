from uuid import UUID

import pytest

from .uuidgen import uuidgen


@pytest.mark.order(1)
def test_uuidgen():
    result = uuidgen()
    assert type(result) is str
    assert len(result) == 32
    assert result.isalnum() is True
    assert UUID(result)
