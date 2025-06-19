"""
Package: service
Initializes Flask app, configures logging, security, and database
"""
import sys
from flask import Flask
from flask_talisman import Talisman
from flask_cors import CORS
from service import config
from service.common import log_handlers

# Create and configure the Flask app
app = Flask(__name__)
talisman = Talisman(app)
CORS(app)
app.config.from_object(config)

# Import routes and models after app is created
from service import routes, models  # noqa: F401, E402
from service.common import error_handlers, cli_commands  # noqa: F401, E402

# Set up logging
log_handlers.init_logging(app, "gunicorn.error")
app.logger.info(70 * "*")
app.logger.info("  A C C O U N T   S E R V I C E   R U N N I N G  ".center(70, "*"))
app.logger.info(70 * "*")

# Initialize DB
try:
    models.init_db(app)
except Exception as error:
    app.logger.critical("%s: Cannot continue", error)
    sys.exit(4)

app.logger.info("Service initialized!")
