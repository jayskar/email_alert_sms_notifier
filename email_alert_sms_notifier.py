import requests
import logging
from exchangelib import Credentials, Account, Configuration, DELEGATE
from config import EMAIL_SERVER, EMAIL_ADDRESS, EMAIL_PASSWORD, SMS_SENDER, SMS_RECIPIENT, SMS_GATEWAY, SMS_GW_USER, \
    SMS_GW_PASS


class easn:
    def __init__(self):
        self.sms_content = None
        self.new_content = None
        self.query_email_list = self.get_queryemaillist()

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
            datefmt='%m/%d/%Y %I:%M:%S %p',
            handlers=[
                logging.FileHandler("debug.log"),
                logging.StreamHandler()
            ]
        )

    def get_queryemaillist(self):
        file = open("email_senders.txt", "r")
        data = file.read()
        # print("\nData of the File: ", data)
        sender_list = data.split('\n')
        # print("\nData Converted into List : ", listVar)
        file.close()
        return sender_list

    def check_email(self):
        credentials = Credentials(EMAIL_ADDRESS, EMAIL_PASSWORD)
        config = Configuration(server=EMAIL_SERVER, credentials=credentials)

        account = Account(
            primary_smtp_address=EMAIL_ADDRESS,
            credentials=credentials,
            autodiscover=False,
            access_type=DELEGATE,
            config=config
        )

        # test_folder = account.inbox / "TEST2"
        # print(test_folder.absolute)
        # test_qs = test_folder.all().values_list('id', 'subject', 'changekey')

        qs1 = account.inbox.all().values_list('id', 'subject', 'changekey')

        count_emails = qs1.count()

        if count_emails > 0:
            logging.info("{} emails found in queryset.".format(str(qs1.count())))
            for msg in qs1:
                item = account.inbox.get(id=msg[0])
                localized_date = item.datetime_received.astimezone(account.default_timezone)
                # print(localized_date)
                datetime_rec = str(localized_date).split("+")[0]
                _date = datetime_rec.split(" ")[0]
                _time = datetime_rec.split(" ")[1]
                # print(_date)
                # print(_time)
                email_from = item.sender.email_address
                self.sms_content = str(item.text_body) + "\nDATE: {}".format(_date) + "\nTIME: {}".format(_time)
                self.new_content = self.sms_content.rstrip()
                # print(item.datetime_received)

                if email_from in self.query_email_list:
                    logging.info("Executing Send Alert")
                    self._sendalert()
                    item.delete()
                else:
                    logging.warning("Email {} not in email_sender list".format(email_from))
        else:
            logging.info("No emails!")

    def _sendalert(self):
        """
        NOTE: sms_data will be different for different SMS GATEWAY PROVIDERS.
        Please consult with your SMS GATEWAY provider.
        Some will require API KEY, others may provide you with credentials as is my case. You may be also required to
        provide additional information, such as message id etc.
        """
        sms_data = {
            'from': SMS_SENDER,
            'to': SMS_RECIPIENT,
            'text': self.new_content,
            'user': SMS_GW_USER,
            'pass': SMS_GW_PASS,
            'id': "1234",
            'dlrreq': 0
        }

        try:
            logging.info("Sending data: {}".format(sms_data))
            requests.post(SMS_GATEWAY, data=sms_data)
        except Exception as e:
            logging.error(str(e))

    def runmain(self):
        self.check_email()


na = easn()
na.runmain()
