"""Test suite for PatientValidator."""

import pytest
from src.clinical.patient_validator import PatientValidator


@pytest.fixture
def validator():
    """Fixture providing PatientValidator instance."""
    return PatientValidator()


@pytest.fixture
def valid_patient():
    """Fixture providing valid patient data."""
    return {
        "patient_id": "PAT000001",
        "age": 45,
        "gender": "F",
        "enrollment_date": "2024-01-15",
        "site_id": "SITE001",
        "consent_signed": True
    }


def test_valid_patient(validator, valid_patient):
    """Test validation of valid patient data."""
    is_valid, errors = validator.validate(valid_patient)
    assert is_valid is True
    assert errors == []


def test_invalid_patient_id(validator, valid_patient):
    """Test invalid patient ID format."""
    valid_patient["patient_id"] = "INVALID"
    is_valid, errors = validator.validate(valid_patient)
    assert is_valid is False
    assert any("patient_id" in error for error in errors)


def test_age_below_minimum(validator, valid_patient):
    """Test age below minimum threshold."""
    valid_patient["age"] = 15
    is_valid, errors = validator.validate(valid_patient)
    assert is_valid is False


def test_unsigned_consent(validator, valid_patient):
    """Test unsigned consent."""
    valid_patient["consent_signed"] = False
    is_valid, errors = validator.validate(valid_patient)
    assert is_valid is False
