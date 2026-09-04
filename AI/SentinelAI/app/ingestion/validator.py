"""
SentinelAI - Security Event Data Validator.

Validates raw security event data before it enters
the feature engineering and ML pipeline.
"""

from __future__ import annotations

import ipaddress
from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = {
    "timestamp",
    "user_id",
    "source_ip",
    "event_type",
    "resource",
    "status",
    "response_time_ms",
    "bytes_transferred",
    "is_suspicious",
}

VALID_EVENT_TYPES = {
    "login",
    "failed_login",
    "file_access",
    "api_request",
    "password_change",
    "logout",
    "privilege_change",
}

VALID_STATUSES = {
    "success",
    "failure",
}

NUMERIC_COLUMNS = {
    "response_time_ms",
    "bytes_transferred",
    "is_suspicious",
}


def validate_ip(value: object) -> bool:
    """Return True when value is a valid IPv4 or IPv6 address."""

    try:
        ipaddress.ip_address(str(value))
        return True
    except ValueError:
        return False


def validate_events(dataframe: pd.DataFrame) -> dict:
    """
    Validate a security-event DataFrame.

    Returns a structured validation report instead of modifying
    the input DataFrame.
    """

    report = {
        "valid": True,
        "errors": [],
        "warnings": [],
        "statistics": {},
    }

    # ------------------------------------------------------------------
    # Schema validation
    # ------------------------------------------------------------------

    actual_columns = set(dataframe.columns)

    missing_columns = REQUIRED_COLUMNS - actual_columns

    if missing_columns:
        report["valid"] = False
        report["errors"].append(
            f"Missing required columns: {sorted(missing_columns)}"
        )

    # Stop deeper validation if the required schema is incomplete.
    if missing_columns:
        report["statistics"]["rows"] = len(dataframe)
        report["statistics"]["columns"] = len(dataframe.columns)
        return report

    # ------------------------------------------------------------------
    # Missing values
    # ------------------------------------------------------------------

    missing_values = dataframe[list(REQUIRED_COLUMNS)].isna().sum()

    missing_columns_with_values = {
        column: int(count)
        for column, count in missing_values.items()
        if count > 0
    }

    if missing_columns_with_values:
        report["valid"] = False
        report["errors"].append(
            f"Missing values detected: {missing_columns_with_values}"
        )

    # ------------------------------------------------------------------
    # Duplicate events
    # ------------------------------------------------------------------

    duplicate_count = int(dataframe.duplicated().sum())

    if duplicate_count > 0:
        report["warnings"].append(
            f"Found {duplicate_count} duplicate rows."
        )

    # ------------------------------------------------------------------
    # Timestamp validation
    # ------------------------------------------------------------------

    timestamps = pd.to_datetime(
        dataframe["timestamp"],
        errors="coerce",
    )

    invalid_timestamps = int(timestamps.isna().sum())

    if invalid_timestamps > 0:
        report["valid"] = False
        report["errors"].append(
            f"Found {invalid_timestamps} invalid timestamps."
        )

    # ------------------------------------------------------------------
    # IP validation
    # ------------------------------------------------------------------

    invalid_ips = int(
        (~dataframe["source_ip"].apply(validate_ip)).sum()
    )

    if invalid_ips > 0:
        report["valid"] = False
        report["errors"].append(
            f"Found {invalid_ips} invalid IP addresses."
        )

    # ------------------------------------------------------------------
    # Event type validation
    # ------------------------------------------------------------------

    invalid_event_types = sorted(
        set(dataframe["event_type"].dropna())
        - VALID_EVENT_TYPES
    )

    if invalid_event_types:
        report["valid"] = False
        report["errors"].append(
            f"Invalid event types: {invalid_event_types}"
        )

    # ------------------------------------------------------------------
    # Status validation
    # ------------------------------------------------------------------

    invalid_statuses = sorted(
        set(dataframe["status"].dropna())
        - VALID_STATUSES
    )

    if invalid_statuses:
        report["valid"] = False
        report["errors"].append(
            f"Invalid statuses: {invalid_statuses}"
        )

    # ------------------------------------------------------------------
    # Numeric validation
    # ------------------------------------------------------------------

    for column in NUMERIC_COLUMNS:
        numeric_values = pd.to_numeric(
            dataframe[column],
            errors="coerce",
        )

        invalid_count = int(numeric_values.isna().sum())

        if invalid_count > 0:
            report["valid"] = False
            report["errors"].append(
                f"Column '{column}' contains "
                f"{invalid_count} non-numeric values."
            )

    # ------------------------------------------------------------------
    # Value-range validation
    # ------------------------------------------------------------------

    if (dataframe["response_time_ms"] < 0).any():
        report["valid"] = False
        report["errors"].append(
            "response_time_ms contains negative values."
        )

    if (dataframe["bytes_transferred"] < 0).any():
        report["valid"] = False
        report["errors"].append(
            "bytes_transferred contains negative values."
        )

    if not dataframe["is_suspicious"].isin({0, 1}).all():
        report["valid"] = False
        report["errors"].append(
            "is_suspicious must contain only 0 or 1."
        )

    # ------------------------------------------------------------------
    # Statistics
    # ------------------------------------------------------------------

    report["statistics"] = {
        "rows": len(dataframe),
        "columns": len(dataframe.columns),
        "duplicates": duplicate_count,
        "missing_values": int(missing_values.sum()),
        "suspicious_events": int(
            (dataframe["is_suspicious"] == 1).sum()
        ),
        "normal_events": int(
            (dataframe["is_suspicious"] == 0).sum()
        ),
    }

    return report


def validate_csv(csv_path: str | Path) -> dict:
    """Load a CSV file and validate its contents."""

    csv_path = Path(csv_path)

    if not csv_path.exists():
        return {
            "valid": False,
            "errors": [f"File does not exist: {csv_path}"],
            "warnings": [],
            "statistics": {},
        }

    try:
        dataframe = pd.read_csv(csv_path)
    except Exception as exc:
        return {
            "valid": False,
            "errors": [f"Unable to read CSV: {exc}"],
            "warnings": [],
            "statistics": {},
        }

    return validate_events(dataframe)


def main() -> None:
    """Run validation against the generated SentinelAI dataset."""

    project_root = Path(__file__).resolve().parents[2]

    csv_path = (
        project_root
        / "data"
        / "raw"
        / "security_events.csv"
    )

    report = validate_csv(csv_path)

    print("=" * 60)
    print("SentinelAI Data Validation Report")
    print("=" * 60)

    print(f"Status: {'VALID' if report['valid'] else 'INVALID'}")

    print("\nStatistics:")

    for key, value in report["statistics"].items():
        print(f"  {key}: {value}")

    if report["warnings"]:
        print("\nWarnings:")

        for warning in report["warnings"]:
            print(f"  ⚠ {warning}")

    if report["errors"]:
        print("\nErrors:")

        for error in report["errors"]:
            print(f"  ✗ {error}")

    print("=" * 60)


if __name__ == "__main__":
    main()