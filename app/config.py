import os


def get_config():
    """Read configuration from environment variables.

    No hardcoded secrets or messages are placed in code. Use environment
    variables or a local `.env` file for development.
    """
    return {
        "APP_ENV": os.environ.get("APP_ENV", "dev"),
        "GREETING": os.environ.get("GREETING"),
        "GREETING_DEV": os.environ.get("GREETING_DEV"),
        "GREETING_TEST": os.environ.get("GREETING_TEST"),
        "PORT": int(os.environ.get("PORT", 5000)),
        "HOST": os.environ.get("HOST", "0.0.0.0"),
        "UPLOAD_DIR": os.environ.get("UPLOAD_DIR", "uploads"),
    }
