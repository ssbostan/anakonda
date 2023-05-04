import pytest

from anakonda.config import Config

from .datetime import now


@pytest.mark.order(1)
def test_now():
    result = now()
    assert result.tzinfo.zone == Config.TIMEZONE
