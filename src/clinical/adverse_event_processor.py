"""Adverse event data processor for clinical trials."""

import pandas as pd
from typing import Dict, List, Tuple


class AdverseEventProcessor:
    """Processes and categorizes adverse event data."""

    SEVERITY_LEVELS = ["Mild", "Moderate", "Severe", "Life-threatening", "Fatal"]
    REQUIRED_COLUMNS = [
        "event_id",
        "patient_id",
        "event_date",
        "description",
        "severity",
    ]

    def load_events(self, file_path: str) -> pd.DataFrame:
        """Load adverse events from CSV file."""
        df = pd.read_csv(file_path)

        missing_cols = set(self.REQUIRED_COLUMNS) - set(df.columns)
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")

        return df

    def validate_event(self, event: Dict) -> Tuple[bool, List[str]]:
        """Validate a single adverse event."""
        errors = []

        for field in self.REQUIRED_COLUMNS:
            if field not in event or event[field] is None or event[field] == "":
                errors.append(f"Missing required field: {field}")

        if "severity" in event and event["severity"] not in self.SEVERITY_LEVELS:
            errors.append(f"Invalid severity: {event['severity']}")

        return len(errors) == 0, errors

    def categorize_by_severity(self, df: pd.DataFrame) -> Dict[str, int]:
        """Categorize events by severity level."""
        return df["severity"].value_counts().to_dict()
