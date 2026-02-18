"""Test suite for AdverseEventProcessor."""

import os
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
        "severity": "Mild",
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
        "severity": "Invalid",
    }
    is_valid, errors = processor.validate_event(event)
    assert is_valid is False


def test_validate_missing_required_fields(processor):
    """Test validation with missing required fields."""
    event = {"event_id": "AE001", "severity": "Mild"}
    is_valid, errors = processor.validate_event(event)
    assert is_valid is False
    assert len(errors) > 0


def test_load_events_valid_file(processor):
    """Test loading events from valid CSV file."""
    test_file = "test_data/adverse_events_test.csv"
    if os.path.exists(test_file):
        df = processor.load_events(test_file)
        assert not df.empty
        assert all(col in df.columns for col in processor.REQUIRED_COLUMNS)


def test_load_events_missing_columns(processor):
    """Test loading events with missing required columns."""
    import tempfile

    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write("event_id,description\n")
        f.write("AE001,Headache\n")
        temp_file = f.name

    try:
        with pytest.raises(ValueError, match="Missing required columns"):
            processor.load_events(temp_file)
    finally:
        os.unlink(temp_file)


def test_categorize_by_severity(processor):
    """Test categorizing events by severity."""
    df = pd.DataFrame(
        {
            "event_id": ["AE001", "AE002", "AE003"],
            "patient_id": ["PAT001", "PAT002", "PAT003"],
            "event_date": ["2024-01-20", "2024-01-21", "2024-01-22"],
            "description": ["Headache", "Nausea", "Dizziness"],
            "severity": ["Mild", "Moderate", "Mild"],
        }
    )
    result = processor.categorize_by_severity(df)
    assert result["Mild"] == 2
    assert result["Moderate"] == 1
