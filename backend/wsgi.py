import os
from config import load_config
from app import create_app

config = load_config()
application = create_app(config)

if __name__ == "__main__":
    application.run(
        host=os.environ.get("FLASK_HOST", "0.0.0.0"),
        port=int(os.environ.get("FLASK_PORT", "5000")),
        debug=config.DEBUG,
    )
