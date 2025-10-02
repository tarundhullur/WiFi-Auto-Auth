import sqlite3
import requests
import datetime
import re
import sys
import os
import argparse

# Add the current directory to the path so we can import config
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.logging_config import get_logger, setup_logging_from_env, LoggerFactory

# Database setup
DB_NAME = "wifi_log.db"

# Initialize logging
setup_logging_from_env()
logger = get_logger(__name__)

def setup_database():
    """Create the database and table if they do not exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS login_attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            username TEXT,
            password TEXT,
            a TEXT,
            response_status TEXT,
            response_message TEXT
        )
    """)
    conn.commit()
    conn.close()

def log_attempt(username, password, a, response_status, response_message):
    """Log each login attempt in the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO login_attempts (timestamp, username, password, a, response_status, response_message)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (datetime.datetime.now(), username, "******", a, response_status, response_message))
    conn.commit()
    conn.close()

def extract_message(response_text):
    """Extracts the meaningful message from the XML response."""
    match = re.search(r"<message><!\[CDATA\[(.*?)\]\]></message>", response_text)
    return match.group(1) if match else "Unknown response"

def wifi_login():
    """Perform the WiFi login request and log the result."""
    url = "POST url from the inspect element"  # Change Required
    username = "username"
    password = "password"
    a_value = str(int(datetime.datetime.now().timestamp()))  # Generate dynamic 'a' value, you may refer to the screenshots in the setup.md file

    payload = {
        "mode": "191",
        "username": username,
        "password": password,
        "a": a_value,
        "producttype": "0"
    }

    try:
        response = requests.post(url, data=payload)
        response_status = response.status_code
        response_message = extract_message(response.text)

        logger.info("WiFi login attempt completed")
        logger.info(f"Username: {username}")
        logger.info(f"Session ID (a): {a_value}")
        logger.info(f"Response status: {response_status}")
        logger.info(f"Response message: {response_message}")

        # Log the attempt in SQLite
        log_attempt(username, password, a_value, response_status, response_message)

    except requests.exceptions.RequestException as e:
        logger.error(f"WiFi login request failed: {e}")
        log_attempt(username, password, a_value, "FAILED", str(e))

def view_logs(limit=5):
    """Display login logs in a readable format."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT timestamp, username, a, response_status, response_message 
        FROM login_attempts 
        ORDER BY timestamp DESC 
        LIMIT ?
    """, (limit,))

    logs = cursor.fetchall()
    conn.close()

    if not logs:
        logger.info("No login attempts found in database")
        return

    logger.info("Recent login attempts retrieved from database")
    logger.info("=" * 80)

    for log in logs:
        timestamp, username, a, status, message = log
        logger.info(f"Time: {timestamp}")
        logger.info(f"Username: {username}")
        logger.info(f"Session ID (a): {a}")
        logger.info(f"Status: {status}")
        logger.info(f"Message: {message}")
        logger.info("-" * 80)

def parse_arguments():
    """Parse command line arguments for logging configuration."""
    parser = argparse.ArgumentParser(description='WiFi Auto Login with Professional Logging')

    # Logging configuration arguments
    parser.add_argument(
        '--log-level',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        help='Set the logging level (default: INFO)'
    )
    parser.add_argument(
        '--log-file',
        action='store_true',
        default=True,
        help='Enable file logging (default: enabled)'
    )
    parser.add_argument(
        '--no-log-file',
        action='store_false',
        dest='log_file',
        help='Disable file logging'
    )
    parser.add_argument(
        '--log-dir',
        default='./logs',
        help='Directory for log files (default: ./logs)'
    )
    parser.add_argument(
        '--console-logging',
        action='store_true',
        default=True,
        help='Enable console logging (default: enabled)'
    )
    parser.add_argument(
        '--no-console-logging',
        action='store_false',
        dest='console_logging',
        help='Disable console logging'
    )

    # Application arguments
    parser.add_argument(
        '--view-logs',
        type=int,
        metavar='N',
        help='View last N login attempts instead of performing login'
    )
    parser.add_argument(
        '--max-attempts',
        type=int,
        default=5,
        help='Maximum number of login attempts to show when viewing logs (default: 5)'
    )

    return parser.parse_args()


if __name__ == "__main__":
    # Parse command line arguments
    args = parse_arguments()

    # Configure logging from command line arguments
    LoggerFactory.configure_from_args(args)

    # Get logger after configuration
    logger = get_logger(__name__)

    logger.info("WiFi Auto Login application started")

    try:
        setup_database()  # Ensure the database is set up

        if args.view_logs is not None:
            # View logs only
            logger.info(f"Viewing last {args.max_attempts} login attempts")
            view_logs(args.max_attempts)
        else:
            # Perform login and show recent logs
            logger.info("Performing WiFi login attempt")
            wifi_login()  # Attempt login
            logger.info("Login attempt completed, retrieving recent logs")
            view_logs(args.max_attempts)  # Show last 5 login attempts

    except Exception as e:
        logger.critical(f"Application error: {e}", exc_info=True)
        sys.exit(1)

    logger.info("WiFi Auto Login application completed successfully")
