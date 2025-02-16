# **Auto Wifi Login**
"Tired of entering the same Wi-Fi credentials every time you join the network? So was I! 😅 At my institute, logging into Wi-Fi manually was a hassle, so I built this Auto WiFi Login Script to automate the process!

This script automatically logs into Wi-Fi networks using pre-saved credentials and now comes with SQLite integration to store login attempts. It keeps track of all login activities, captures dynamic session parameters (a), and provides a user-friendly log display for debugging.

Ideal for schools, workplaces, or any location with recurring Wi-Fi logins, this script eliminates manual re-authentication and ensures effortless connectivity. It's fully customizable, works across different networks, and can even be automated on startup for a seamless experience.

Say goodbye to typing passwords repeatedly and hello to smart, automated Wi-Fi access!"


## **Features**

-  Secure credential storage using SQLite database
-  Login attempt logging with automatic cleanup
-  Support for multiple network configurations
-  Automatic error handling and retries
-  Detailed status tracking and logging

## **📌 Requirements**  

Before running the script, ensure you have:  
✔ **Python 3** installed (`python3 --version`)  
✔ **Required libraries** (`requests`, `sqlite3`)  
✔ **WiFi network login page details `(You may refer to the screenshots in the setup.md)`**  

## **Security Notes**
- Credentials are stored locally in your home directory
- No sensitive data is transmitted except during login
- Logs are automatically cleaned up after 30 days

## **Contributing**
Feel free to fork, improve, and submit pull requests. Some areas for improvement:
- Additional network portal support
- GUI interface
- Network status monitoring


# **License:**
   This project is licensed under the [MIT License](LICENSE), which allows for free use, modification, and distribution.

🔧 **Need help?** Open an issue on GitHub!
