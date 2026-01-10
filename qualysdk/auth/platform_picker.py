"""
Helper code for platform picking logic.

For help with platform URLs, see: https://www.qualys.com/platform-identification
"""


class PlatformPicker:
    """
    PlatformPicker - handles platform selection logic.
    """

    urls = {
        "api_urls": {
            "qg1": "https://qualysapi.qualys.com",
            "qg2": "https://qualysapi.qg2.apps.qualys.com",
            "qg3": "https://qualysapi.qg3.apps.qualys.com",
            "qg4": "https://qualysapi.qg4.apps.qualys.com",
            "eu1": "https://qualysapi.qualys.eu",
            "eu2": "https://qualysapi.qg2.apps.qualys.eu",
            "eu3": "https://qualysapi.qg3.apps.qualys.it",
            "in1": "https://qualysapi.qg1.apps.qualys.in",
            "ca1": "https://qualysapi.qg1.apps.qualys.ca",
            "ae1": "https://qualysapi.qg1.apps.qualys.ae",
            "uk1": "https://qualysapi.qg1.apps.qualys.co.uk",
            "au1": "https://qualysapi.qg1.apps.qualys.com.au",
            "ksa1": "https://qualysapi.qg1.apps.qualysksa.com",
        },
        "gateway_urls": {
            "qg1": "https://gateway.qg1.apps.qualys.com",
            "qg2": "https://gateway.qg2.apps.qualys.com",
            "qg3": "https://gateway.qg3.apps.qualys.com",
            "qg4": "https://gateway.qg4.apps.qualys.com",
            "eu1": "https://gateway.qg1.apps.qualys.eu",
            "eu2": "https://gateway.qg2.apps.qualys.eu",
            "eu3": "https://gateway.qg3.apps.qualys.it",
            "in1": "https://gateway.qg1.apps.qualys.in",
            "ca1": "https://gateway.qg1.apps.qualys.ca",
            "ae1": "https://gateway.qg1.apps.qualys.ae",
            "uk1": "https://gateway.qg1.apps.qualys.co.uk",
            "au1": "https://gateway.qg1.apps.qualys.com.au",
            "ksa1": "https://gateway.qg1.apps.qualysksa.com",
        },
        "qualysguard_urls": {
            "qg1": "https://qualysguard.qualys.com",
            "qg2": "https://qualysguard.qg2.apps.qualys.com",
            "qg3": "https://qualysguard.qg3.apps.qualys.com",
            "qg4": "https://qualysguard.qg4.apps.qualys.com",
            "eu1": "https://qualysguard.qualys.eu",
            "eu2": "https://qualysguard.qg2.apps.qualys.eu",
            "eu3": "https://qualysguard.qg3.apps.qualys.it",
            "in1": "https://qualysguard.qg1.apps.qualys.in",
            "ca1": "https://qualysguard.qg1.apps.qualys.ca",
            "ae1": "https://qualysguard.qg1.apps.qualys.ae",
            "uk1": "https://qualysguard.qg1.apps.qualys.co.uk",
            "au1": "https://qualysguard.qg1.apps.qualys.com.au",
            "ksa1": "https://qualysguard.qg1.apps.qualysksa.com",
        },
    }

    @staticmethod
    def get_gateway_url(platform: str) -> str:
        """
        Get the gateway URL based on platform value.
        """
        if platform.lower() in PlatformPicker.urls["gateway_urls"]:
            return PlatformPicker.urls["gateway_urls"][platform.lower()]
        else:
            raise ValueError(
                f"Invalid platform: {platform}. Use one of {list(PlatformPicker.urls['gateway_urls'].keys())} or provide an override_platform."
            )

    @staticmethod
    def get_api_url(platform: str) -> str:
        """
        Get the API URL based on platform value.
        """
        if platform.lower() in PlatformPicker.urls["api_urls"]:
            return PlatformPicker.urls["api_urls"][platform.lower()]
        else:
            raise ValueError(
                f"Invalid platform: {platform}. Use one of {list(PlatformPicker.urls['api_urls'].keys())} or provide an override_platform."
            )

    @staticmethod
    def get_qualysguard_url(platform: str) -> str:
        """
        Get the QualysGuard URL based on platform value.
        """
        if platform.lower() in PlatformPicker.urls["qualysguard_urls"]:
            return PlatformPicker.urls["qualysguard_urls"][platform.lower()]
        else:
            raise ValueError(
                f"Invalid platform: {platform}. Use one of {list(PlatformPicker.urls['qualysguard_urls'].keys())} or provide an override_platform."
            )
