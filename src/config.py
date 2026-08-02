from dataclasses import dataclass
from pathlib import Path
from typing import List

import yaml


@dataclass
class MerakiConfig:
    api_key: str
    org_id: str
    network_id: str
    ssid_number: int
    ssid_name: str


@dataclass
class EmailConfig:
    smtp_host: str
    smtp_port: int
    smtp_username: str
    smtp_password: str
    from_address: str
    recipients: List[str]
    admin_alert_recipients: List[str]


@dataclass
class PasswordConfig:
    length: int = 8
    special_char_count: int = 2
    special_chars: str = "!@#$%^&*-_"


@dataclass
class AppConfig:
    meraki: MerakiConfig
    email: EmailConfig
    password: PasswordConfig


def load_config(path) -> AppConfig:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    with open(path) as f:
        raw = yaml.safe_load(f)

    return AppConfig(
        meraki=MerakiConfig(**raw["meraki"]),
        email=EmailConfig(**raw["email"]),
        password=PasswordConfig(**raw.get("password", {})),
    )
