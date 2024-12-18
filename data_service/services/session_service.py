import requests
from breeze_connect import BreezeConnect


class SessionService:
    """
    Handles session generation and validation for the Breeze API.
    """

    def __init__(self, api_key):
        """
        Initialize the SessionService with an API key.

        Args:
            api_key (str): The Breeze API key.
        """
        self.api_key = api_key
        self.client = BreezeConnect(api_key=api_key)

    def generate_session_token(self, api_secret, session_token):
        """
        Generates a session token using BreezeConnect.

        Args:
            api_secret (str): The API secret.
            session_token (str): The session token from the Breeze API.

        Returns:
            BreezeConnect: An initialized BreezeConnect client with the session set.

        Raises:
            ValueError: If session token generation fails.
        """
        try:
            self.client.generate_session(api_secret=api_secret, session_token=session_token)
            return self.client
        except Exception as e:
            raise ValueError(f"Failed to generate session token: {str(e)}")

    def validate_session(self, session_token):
        """
        Validates the provided session token.

        Args:
            session_token (str): The session token to validate.

        Returns:
            bool: True if the session token is valid, False otherwise.
        """
        if not session_token:
            return False

        # Add API-specific token validation logic here, if available.
        return True

    def refresh_session(self, api_secret, session_token):
        """
        Refresh the session if it has expired or is invalid.

        Args:
            api_secret (str): The API secret.
            session_token (str): The current session token.

        Returns:
            BreezeConnect: A refreshed BreezeConnect client with a valid session.
        """
        if not self.validate_session(session_token):
            return self.generate_session_token(api_secret, session_token)
        return self.client
