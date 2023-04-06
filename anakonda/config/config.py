from os import environ


class Config:
    ENV = environ.get("ANAKONDA_API_ENV", "production")

    DEBUG = bool(int(environ.get("ANAKONDA_API_DEBUG", "0")))

    TESTING = DEBUG

    SECRET_KEY = environ.get("ANAKONDA_API_SECRET_KEY", "secretkey")

    JSONIFY_PRETTYPRINT_REGULAR = bool(
        int(environ.get("ANAKONDA_API_JSON_PRETTYPRINT", "0"))
    )
