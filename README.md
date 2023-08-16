# Email Alert Checker and SMS Notifier

This Python script checks a specified email address for alerts sent by specific email senders and sends SMS notifications using an SMS Gateway. It utilizes the `exchangelib` library for interacting with the email server and the `requests` library for sending SMS messages.

## Prerequisites

- Python 3.x is required to run this script.
- `exchangelib` library (`pip install exchangelib`)
- `requests` library (`pip install requests`)
- Access to an email account with Exchange Web Services (EWS) enabled.
- An SMS Gateway API key or access.

## Configuration
1. Clone or download the repository to your local machine.

2. Create a file name `email_senders.txt` in the same directory as the script. List the email senders for which you want to receive alerts, each on a new line.

    Example `email_senders.txt`:
    ```graphql
    sender1@example.com
    sender2@example.com
    ```
3. Open the `config.py` file and provide the necessary configurations:
   
    * `EMAIL_ADDRESS`: The email address you want to monitor for alerts. 
    * `EMAIL_PASSWORD`: The password for the email address.
    * `SMS_GATEWAY_API_URL`: The URL of the SMS Gateway API.
    * `SMS_GATEWAY_API_KEY`: Your API key for the SMS Gateway.

## Usage
Run the script using the following command:
```bash
python email_alert_sms_notifier.py
```
The script will connect to the specified email address, check for emails from the configured senders, and if an alert is found, it will extract the email contents and send an SMS notification using the SMS Gateway.

## Automation
### Linux (Cron Job)
To automate the script on a Linux system using cron jobs, follow these steps:

1. Open the terminal
2. Edit the user's crontab using the command:
    ```bash
    crontab -e
    ```
3. Add the following line to run the script every hour:
    ```bash
    0 * * * * /usr/bin/python /path/to/email_alert_sms_notifier.py
    ```
4. Save and exit the crontab editor.

### Windows (Task Scheduler)
To automate the script on a Windows system using Task Scheduler, follow these steps:

1. Open Task Scheduler from the Start menu.

2. Click on "Create Basic Task" and follow the wizard to create a new task.

3. Specify the name and description for the task.

4. Choose the "Daily" or "Hourly" trigger, depending on your preference.

5. Select "Start a program" as the action and browse to the location of your Python executable (`python.exe`) and the script (`email_alert_sms_notifier.py`).

6. Complete the wizard and save the task.

## License
This project is licensed under the MIT License