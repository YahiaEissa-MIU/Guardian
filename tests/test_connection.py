# tests/test_wazuh_connection.py
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class TestWazuhConnection:
    def __init__(self):
        # Use the same configuration as your DashboardController
        self.base_url = "https://192.168.1.5:55000"
        self.auth = ('wazuh-wui', '1p.xwBLv9W*VwXGmwiYWn**Z9VwNLSn8')

    def test_connection(self):
        """Test connection to Wazuh API"""
        try:
            # Get token
            response = requests.post(
                f"{self.base_url}/security/user/authenticate",
                auth=self.auth,
                verify=False
            )

            if response.status_code == 200:
                print("✅ Successfully got authentication token!")
                token = response.json()['data']['token']

                # Test getting manager info
                headers = {'Authorization': f'Bearer {token}'}
                manager_info = requests.get(
                    f"{self.base_url}/manager/info",
                    headers=headers,
                    verify=False
                )

                if manager_info.status_code == 200:
                    print("✅ Successfully connected to Wazuh API!")
                    print("\nManager info:", manager_info.json())
                    return True
                else:
                    print(f"❌ Error getting manager info: {manager_info.text}")
            else:
                print(f"❌ Error getting token: {response.text}")

        except Exception as e:
            print(f"❌ Connection error: {e}")

        return False


def main():
    print("Testing Wazuh API Connection...")
    print("-" * 50)

    tester = TestWazuhConnection()
    success = tester.test_connection()

    print("-" * 50)
    if success:
        print("✅ All connection tests passed!")
    else:
        print("❌ Connection test failed!")


if __name__ == "__main__":
    main()