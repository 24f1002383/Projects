"""
SentinelAI - Security Event Generator

Generates synthetic security events for development and ML experimentation.
The generated data represents normal and suspicious activity patterns.
"""

from __future__ import annotations

import random
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

NUM_EVENTS = 10_000
RANDOM_SEED = 42

PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = PROJECT_ROOT / "data" / "raw" / "security_events.csv"


USERS = [
    "user_001",
    "user_002",
    "user_003",
    "user_004",
    "user_005",
    "admin_001",
    "admin_002",
    "service_api",
]

EVENT_TYPES = [
    "login",
    "failed_login",
    "file_access",
    "api_request",
    "password_change",
    "logout",
    "privilege_change",
]

RESOURCES = [
    "/home",
    "/dashboard",
    "/documents",
    "/reports",
    "/api/users",
    "/api/transactions",
    "/admin",
]

NORMAL_IP_PREFIXES = [
    "192.168.1",
    "192.168.2",
    "10.0.0",
    "10.0.1",
]

SUSPICIOUS_IP_PREFIXES = [
    "185.220.101",
    "45.155.205",
    "91.240.118",
]


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def generate_ip(suspicious: bool = False) -> str:
    """Generate a synthetic IPv4 address."""

    prefixes = SUSPICIOUS_IP_PREFIXES if suspicious else NORMAL_IP_PREFIXES

    return f"{random.choice(prefixes)}.{random.randint(1, 254)}"


def generate_normal_event(timestamp: datetime) -> dict:
    """Generate a normal security event."""

    event_type = random.choices(
        EVENT_TYPES,
        weights=[30, 4, 20, 25, 3, 12, 1],
        k=1,
    )[0]

    user = random.choice(USERS)

    # Admin-only event
    if event_type == "privilege_change":
        user = random.choice(["admin_001", "admin_002"])

    status = "success"

    if event_type == "failed_login":
        status = "failure"

    return {
        "timestamp": timestamp,
        "user_id": user,
        "source_ip": generate_ip(),
        "event_type": event_type,
        "resource": random.choice(RESOURCES),
        "status": status,
        "response_time_ms": random.randint(40, 500),
        "bytes_transferred": random.randint(500, 50_000),
        "is_suspicious": 0,
    }


def generate_suspicious_event(timestamp: datetime) -> dict:
    """Generate a suspicious security event."""

    suspicious_pattern = random.choice(
        [
            "brute_force",
            "large_transfer",
            "privilege_abuse",
            "unusual_access",
        ]
    )

    if suspicious_pattern == "brute_force":
        return {
            "timestamp": timestamp,
            "user_id": random.choice(USERS[:5]),
            "source_ip": generate_ip(suspicious=True),
            "event_type": "failed_login",
            "resource": "/login",
            "status": "failure",
            "response_time_ms": random.randint(50, 300),
            "bytes_transferred": random.randint(100, 2_000),
            "is_suspicious": 1,
        }

    if suspicious_pattern == "large_transfer":
        return {
            "timestamp": timestamp,
            "user_id": random.choice(USERS),
            "source_ip": generate_ip(suspicious=True),
            "event_type": "api_request",
            "resource": "/api/transactions",
            "status": "success",
            "response_time_ms": random.randint(800, 3_000),
            "bytes_transferred": random.randint(5_000_000, 50_000_000),
            "is_suspicious": 1,
        }

    if suspicious_pattern == "privilege_abuse":
        return {
            "timestamp": timestamp,
            "user_id": random.choice(USERS[:5]),
            "source_ip": generate_ip(suspicious=True),
            "event_type": "privilege_change",
            "resource": "/admin",
            "status": "success",
            "response_time_ms": random.randint(100, 1_000),
            "bytes_transferred": random.randint(1_000, 20_000),
            "is_suspicious": 1,
        }

    return {
        "timestamp": timestamp,
        "user_id": random.choice(USERS[:5]),
        "source_ip": generate_ip(suspicious=True),
        "event_type": "file_access",
        "resource": random.choice(
            ["/admin", "/reports", "/api/transactions"]
        ),
        "status": "success",
        "response_time_ms": random.randint(500, 2_500),
        "bytes_transferred": random.randint(100_000, 5_000_000),
        "is_suspicious": 1,
    }


# ---------------------------------------------------------------------------
# Dataset generation
# ---------------------------------------------------------------------------

def generate_dataset(num_events: int = NUM_EVENTS) -> pd.DataFrame:
    """Generate a synthetic security-event dataset."""

    start_time = datetime.now() - timedelta(days=30)

    events = []

    for _ in range(num_events):
        timestamp = start_time + timedelta(
            seconds=random.randint(0, 30 * 24 * 60 * 60)
        )

        # Approximately 5% suspicious events.
        if random.random() < 0.05:
            event = generate_suspicious_event(timestamp)
        else:
            event = generate_normal_event(timestamp)

        events.append(event)

    dataframe = pd.DataFrame(events)

    dataframe = dataframe.sort_values("timestamp").reset_index(drop=True)

    return dataframe


def main() -> None:
    """Generate and save the security-event dataset."""

    random.seed(RANDOM_SEED)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    dataframe = generate_dataset()

    dataframe.to_csv(OUTPUT_PATH, index=False)

    print("=" * 60)
    print("SentinelAI Security Event Generator")
    print("=" * 60)
    print(f"Generated events : {len(dataframe):,}")
    print(f"Suspicious events: {dataframe['is_suspicious'].sum():,}")
    print(f"Normal events    : {(dataframe['is_suspicious'] == 0).sum():,}")
    print(f"Output file      : {OUTPUT_PATH}")
    print("=" * 60)


if __name__ == "__main__":
    main()