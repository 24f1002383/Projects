import pandas as pd

from app.ingestion.validator import validate_events


def valid_dataframe():
    return pd.DataFrame(
        [
            {
                "timestamp": "2026-01-01T10:00:00",
                "user_id": "user_001",
                "source_ip": "192.168.1.10",
                "event_type": "login",
                "resource": "/dashboard",
                "status": "success",
                "response_time_ms": 120,
                "bytes_transferred": 1024,
                "is_suspicious": 0,
            },
            {
                "timestamp": "2026-01-01T10:05:00",
                "user_id": "user_002",
                "source_ip": "192.168.1.11",
                "event_type": "file_access",
                "resource": "/documents",
                "status": "success",
                "response_time_ms": 250,
                "bytes_transferred": 2048,
                "is_suspicious": 0,
            },
        ]
    )


def test_valid_dataset():
    df = valid_dataframe()

    report = validate_events(df)

    assert report["valid"] is True
    assert report["errors"] == []


def test_missing_required_column():
    df = valid_dataframe().drop(columns=["source_ip"])

    report = validate_events(df)

    assert report["valid"] is False
    assert any("source_ip" in error for error in report["errors"])


def test_invalid_ip():
    df = valid_dataframe()
    df.loc[0, "source_ip"] = "not-an-ip"

    report = validate_events(df)

    assert report["valid"] is False
    assert any("IP" in error for error in report["errors"])


def test_invalid_event_type():
    df = valid_dataframe()
    df.loc[0, "event_type"] = "unknown_event"

    report = validate_events(df)

    assert report["valid"] is False
    assert any("event type" in error.lower() for error in report["errors"])


def test_invalid_status():
    df = valid_dataframe()
    df.loc[0, "status"] = "unknown_status"

    report = validate_events(df)

    assert report["valid"] is False
    assert any("status" in error.lower() for error in report["errors"])


def test_invalid_timestamp():
    df = valid_dataframe()
    df.loc[0, "timestamp"] = "not-a-timestamp"

    report = validate_events(df)

    assert report["valid"] is False
    assert any("timestamp" in error.lower() for error in report["errors"])


def test_negative_response_time():
    df = valid_dataframe()
    df.loc[0, "response_time_ms"] = -1

    report = validate_events(df)

    assert report["valid"] is False
    assert any("response" in error.lower() for error in report["errors"])


def test_invalid_suspicious_label():
    df = valid_dataframe()
    df.loc[0, "is_suspicious"] = 2

    report = validate_events(df)

    assert report["valid"] is False
    assert any("suspicious" in error.lower() for error in report["errors"])


def test_duplicate_rows_generate_warning():
    df = valid_dataframe()

    df = pd.concat([df, df.iloc[[0]]], ignore_index=True)

    report = validate_events(df)

    assert report["valid"] is True
    assert report["warnings"]
    assert any("duplicate" in warning.lower() for warning in report["warnings"])