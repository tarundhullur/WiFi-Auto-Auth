import os
import requests
import sqlite3
from datetime import datetime, timedelta
from xml.etree import ElementTree as ET
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('WiFiLogin')

class WiFiLogin:
    def __init__(self):
        # parent directory at home
        self.db_dir = Path.home() / '.wifi_login'
        self.db_dir.mkdir(exist_ok=True)
        self.db_path = self.db_dir / 'wifi.db'
        
        self.init_database()
        
        # whenever we restart it will clean the old data.
        self.clean_old_logs()

    def init_database(self):
        """Initialize SQLite database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create tables
        cursor.executescript('''
            CREATE TABLE IF NOT EXISTS credentials (
                id INTEGER PRIMARY KEY,
                network_name TEXT UNIQUE,
                username TEXT,
                password TEXT,
                login_url TEXT
            );

            CREATE TABLE IF NOT EXISTS login_logs (
                id INTEGER PRIMARY KEY,
                timestamp DATETIME,
                network_name TEXT,
                status TEXT,
                message TEXT
            );
        ''')
        
        conn.commit()
        conn.close()

    def save_credentials(self, network_name, username, password, login_url):
        """Save or update network credentials"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO credentials (network_name, username, password, login_url)
            VALUES (?, ?, ?, ?)
        ''', (network_name, username, password, login_url))
        
        conn.commit()
        conn.close()
        logger.info(f"Credentials saved for network: {network_name}")

    def get_credentials(self, network_name):
        """Retrieve credentials for a network"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT username, password, login_url FROM credentials WHERE network_name = ?', 
                      (network_name,))
        result = cursor.fetchone()
        
        conn.close()
        return result if result else None

    def log_attempt(self, network_name, status, message):
        """Log login attempt"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO login_logs (timestamp, network_name, status, message)
            VALUES (?, ?, ?, ?)
        ''', (datetime.now(), network_name, status, message))
        
        conn.commit()
        conn.close()

    def clean_old_logs(self):
        """Delete logs older than 30 days"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        thirty_days_ago = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute('DELETE FROM login_logs WHERE timestamp < ?', (thirty_days_ago,))
        
        deleted_count = cursor.rowcount
        conn.commit()
        conn.close()
        
        if deleted_count > 0:
            logger.info(f"Cleaned {deleted_count} old log entries")

    def login(self, network_name):
        """Attempt to login to the network"""
        credentials = self.get_credentials(network_name)
        if not credentials:
            message = f"No credentials found for network: {network_name}"
            logger.error(message)
            self.log_attempt(network_name, "ERROR", message)
            return False, message

        username, password, login_url = credentials
        
        payload = {
            "username": username,
            "password": password,
            "mode": "191"
        }

        try:
            response = requests.post(login_url, data=payload)
            
            if response.status_code == 200:
                xml_response = ET.fromstring(response.text)
                status = xml_response.find("status").text if xml_response.find("status") is not None else "UNKNOWN"
                message = xml_response.find("message").text if xml_response.find("message") is not None else ""
                
                success = "LIVE" in status or "success" in message.lower()
                log_status = "SUCCESS" if success else "FAILED"
                
                self.log_attempt(network_name, log_status, message)
                logger.info(f"Login attempt for {network_name}: {log_status} - {message}")
                
                return success, message
            else:
                message = f"HTTP Error: {response.status_code}"
                self.log_attempt(network_name, "ERROR", message)
                logger.error(message)
                return False, message
                
        except Exception as e:
            message = f"Login error: {str(e)}"
            self.log_attempt(network_name, "ERROR", message)
            logger.error(message)
            return False, message

# Example usage
if __name__ == "__main__":
    wifi = WiFiLogin()
    
    network_name = "campus_wifi(Mine is RGIPT_WLAN)"  # Change this to your network name
    login_url = "http://192.168.100.1:8090/login.xml"  # Change this to your login URL
    
    # You only need to save credentials once
    wifi.save_credentials(
        network_name=network_name,
        username="your_username",  # Change this
        password="your_password",  # Change this
        login_url=login_url
    )
    
    # Try to login
    success, message = wifi.login(network_name)
    print(f"Login {'successful' if success else 'failed'}: {message}")
