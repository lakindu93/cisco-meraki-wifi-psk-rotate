import argparse
import logging
import os
import sys
import time
from pathlib import Path

from config import load_config
from mailer import send_email
from meraki_client import MerakiClient
from password_gen import generate_psk

logger = logging.getLogger("cisco-meraki-wifi-psk-rotate")

DEFAULT_CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "config.yaml"
RETRY_BACKOFF_SECONDS = (5, 15, 45)


def retry(fn, attempts=3, description=""):
    last_exc = None
    for attempt in range(1, attempts + 1):
        try:
            return fn()
        except Exception as exc:
            last_exc = exc
            logger.warning("%s attempt %d/%d failed: %s", description, attempt, attempts, exc)
            if attempt < attempts:
                time.sleep(RETRY_BACKOFF_SECONDS[min(attempt - 1, len(RETRY_BACKOFF_SECONDS) - 1)])
    raise last_exc


def send_admin_alert(cfg, subject, body):
    try:
        send_email(
            cfg.email.smtp_host,
            cfg.email.smtp_port,
            cfg.email.smtp_username,
            cfg.email.smtp_password,
            cfg.email.from_address,
            cfg.email.admin_alert_recipients,
            subject,
            body,
        )
    except Exception as exc:
        logger.error("Failed to send admin alert email as well: %s", exc)


def main():
    parser = argparse.ArgumentParser(description="Rotate the Meraki TEST-WIFI WiFi PSK and email the new password.")
    parser.add_argument(
        "--config",
        default=os.environ.get("WIFI_ROTATE_CONFIG", str(DEFAULT_CONFIG_PATH)),
        help="Path to config.yaml",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Fetch and validate the target SSID but do not change the PSK or send email.",
    )
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", stream=sys.stdout)

    cfg = load_config(args.config)
    client = MerakiClient(
        cfg.meraki.api_key,
        cfg.meraki.network_id,
        cfg.meraki.ssid_number,
        cfg.meraki.ssid_name,
    )

    if args.dry_run:
        logger.info("[DRY RUN] Fetching current SSID config only, no changes will be made.")
        current = client.get_current_ssid()
        logger.info("[DRY RUN] Current SSID name: %s (number %s)", current.get("name"), cfg.meraki.ssid_number)
        logger.info("[DRY RUN] Would generate a new PSK and rotate it now.")
        return

    new_psk = generate_psk(cfg.password.length, cfg.password.special_char_count, cfg.password.special_chars)

    try:
        retry(lambda: client.update_psk(new_psk), description="Meraki PSK update")
    except Exception as exc:
        logger.error("Meraki PSK update failed after retries: %s", exc)
        send_admin_alert(
            cfg,
            "[WiFi Rotate] Meraki PSK update FAILED",
            f"Automatic PSK rotation failed for SSID '{cfg.meraki.ssid_name}'.\n\n"
            f"Error: {exc}\n\nThe PSK was NOT changed.",
        )
        sys.exit(1)

    logger.info("Meraki PSK updated successfully for SSID '%s'.", cfg.meraki.ssid_name)

    recipient_body = (
        f"The WiFi password for '{cfg.meraki.ssid_name}' has been rotated.\n\n"
        f"New password: {new_psk}\n\n"
        "This password is valid until the next scheduled rotation."
    )

    try:
        retry(
            lambda: send_email(
                cfg.email.smtp_host,
                cfg.email.smtp_port,
                cfg.email.smtp_username,
                cfg.email.smtp_password,
                cfg.email.from_address,
                cfg.email.recipients,
                f"[WiFi] New password for {cfg.meraki.ssid_name}",
                recipient_body,
            ),
            description="Recipient email send",
        )
    except Exception as exc:
        logger.error("Email delivery to recipients failed after retries: %s", exc)
        logger.warning("New PSK (email delivery failed, retrieve manually): %s", new_psk)
        send_admin_alert(
            cfg,
            "[WiFi Rotate] PSK rotated but EMAIL DELIVERY FAILED",
            f"SSID '{cfg.meraki.ssid_name}' PSK was rotated successfully, but sending the new "
            f"password by email failed.\n\nError: {exc}\n\nNew password (for manual distribution): {new_psk}",
        )
        sys.exit(1)

    logger.info("Rotation complete: PSK updated and email sent to recipients.")


if __name__ == "__main__":
    main()
