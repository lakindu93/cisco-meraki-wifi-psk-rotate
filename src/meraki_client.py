import meraki


class MerakiClient:
    def __init__(self, api_key: str, network_id: str, ssid_number: int, ssid_name: str = None, max_retries: int = 3):
        self.dashboard = meraki.DashboardAPI(
            api_key,
            suppress_logging=True,
            maximum_retries=max_retries,
            wait_on_rate_limit=True,
        )
        self.network_id = network_id
        self.ssid_number = ssid_number
        self.ssid_name = ssid_name

    def get_current_ssid(self) -> dict:
        return self.dashboard.wireless.getNetworkWirelessSsid(self.network_id, self.ssid_number)

    def update_psk(self, new_psk: str) -> dict:
        current = self.get_current_ssid()
        if self.ssid_name and current.get("name") != self.ssid_name:
            raise RuntimeError(
                f"SSID name mismatch: expected '{self.ssid_name}', got '{current.get('name')}'. "
                "Refusing to rotate the wrong SSID."
            )

        updated = self.dashboard.wireless.updateNetworkWirelessSsid(
            self.network_id, self.ssid_number, psk=new_psk
        )

        if updated.get("psk") != new_psk:
            raise RuntimeError("PSK verification failed: Meraki did not report the expected new PSK after update.")

        return updated
