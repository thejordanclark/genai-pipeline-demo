"""Test suite for AdverseEventProcessor."""

import pytest
import pandas as pd
from src.clinical.adverse_event_processor import AdverseEventProcessor


@pytest.fixture
def processor():
    """Fixture providing AdverseEventProcessor instance."""
    return AdverseEventProcessor()


def test_validate_valid_event(processor):
    """Test validation of valid adverse event."""
    event = {
        "event_id": "AE001",
        "patient_id": "PAT000001",
        "event_date": "2024-01-20",
        "description": "Headache",
        "severity": "Mild"
    }
    is_valid, errors = processor.validate_event(event)
    assert is_valid is True
    assert errors == []


def test_validate_invalid_severity(processor):
    """Test validation with invalid severity."""
    event = {
        "event_id": "AE001",
        "patient_id": "PAT000001",
        "event_date": "2024-01-20",
        "description": "Headache",
        "severity": "Invalid"
    }
    is_valid, errors = processor.validate_event(event)
    assert is_valid is False
