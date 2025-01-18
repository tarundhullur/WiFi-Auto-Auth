
### **Setting Up the Auto Wifi Login Script Project Locally**

#### 1. **Clone the Repository:**
   Clone the repository to your local machine:
   ```bash
   git clone https://github.com/your-username/RGIPT_Auto_Connect.git
   ```

#### 2. **Navigate to the Project Directory:**
   Move into the project directory:
   ```bash
   cd RGIPT_Auto_Connect
   ```

#### 3. **Set Environment Variables:**
   The script may require certain environment variables (like Wi-Fi credentials). You can either add these to a `.env` file or set them directly in your terminal.

   Example:
   ```bash
   export WIFI_SSID="Your_Wifi_SSID"
   export WIFI_PASSWORD="Your_Wifi_Password"
   ```

   If you're using a `.env` file, make sure you load it by adding the following to your script or use `python-dotenv` if it’s a Python-based script:
   ```bash
   pip3 install python-dotenv
   ```

   Add this line to your Python script:
   ```python
   from dotenv import load_dotenv
   load_dotenv()  # Load environment variables from .env file
   ```

   Create a `.env` file:
   ```
   WIFI_SSID=Your_Wifi_SSID
   WIFI_PASSWORD=Your_Wifi_Password
   ```

#### 4. **Make the Script Executable (For Bash or Shell Scripts):**
   If you are using a shell script like `auto_wifi_login.sh`, make it executable:
   ```bash
   chmod +x auto_wifi_login.sh
   ```

   For Python scripts (e.g., `wifi_auto_login.py`), ensure you have the correct Python environment set up and use `python3` to run it.

#### 5. **Running the Script:**
   Run the script to automatically log into the Wi-Fi network.

   For a Bash script (`auto_wifi_login.sh`):
   ```bash
   ./auto_wifi_login.sh
   ```

   For a Python script (`wifi_auto_login.py`):
   ```bash
   python3 wifi_auto_login.py
   ```

#### 6. **Schedule the Script to Run Automatically :**
   To make the script run periodically, you can schedule it with **cron** (Linux/Mac). For example, to run the script every 5 minutes:

   1. Open the crontab editor:
      ```bash
      crontab -e
      ```

   2. Add a cron job entry to run the script every 5 minutes (modify path and script name as necessary):
      ```bash
      */5 * * * * /path/to/your/script/auto_wifi_login.sh
      ```
   
      Or for a Python script:
      ```bash
      */5 * * * * /usr/bin/python3 /path/to/your/script/wifi_auto_login.py
      ```

   3. Save and exit the editor.

   This will automatically attempt to connect to the Wi-Fi every 5 minutes.

#### 7. **Contributing:**
   Fork the repository, make improvements or bug fixes, and submit a pull request. Contributions to enhance the functionality (e.g., adding support for more OS or network types) are welcome.

#### 8. **License:**
   This project is licensed under the [MIT License](LICENSE), which allows for free use, modification, and distribution.

---

This guide should make it easy for anyone to set up and use your **Auto Wifi Login Script** locally, with necessary environment variables and scheduling via `cron`. Let me know if you need any additional details or adjustments!