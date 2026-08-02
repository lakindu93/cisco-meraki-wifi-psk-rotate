import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from config import load_config
import meraki


def main():
    parser = argparse.ArgumentParser(description="List SSIDs on the configured network.")
    parser.add_argument("--config", default=str(Path(__file__).resolve().parent.parent / "config" / "config.yaml"))
    args = parser.parse_args()

    cfg = load_config(args.config)
    dashboard = meraki.DashboardAPI(cfg.meraki.api_key, suppress_logging=True)

    ssids = dashboard.wireless.getNetworkWirelessSsids(cfg.meraki.network_id)
    for ssid in ssids:
        if not ssid.get("enabled"):
            continue
        print(f"number={ssid['number']}  name={ssid['name']!r}  authMode={ssid.get('authMode')}")


if __name__ == "__main__":
    main()
