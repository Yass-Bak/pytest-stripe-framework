from .config import Config

class AuthProvider:
    @staticmethod
    def get_auth_headers():
        """
        Returns the authorization headers for Stripe API.
        """
        return {
            "Authorization": f"Bearer {Config.API_KEY}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
