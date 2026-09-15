import pytest
import logging

@pytest.fixture
def logger():
    return logging.getLogger("test_logger")