import functools
import requests
from authentication.pkg.sms.base import Sms
from kavenegar import *


class TestSendSms(Sms):

    def send(self, message: int, phone: str) -> None:
        try:
            api = KavenegarAPI('626F464857416738562B722B49476B6C784C473171387468636D76494F66732F71782F30567337587179343D')
            params = {
                'receptor': f'{phone}',
                'template': 'verify-code',
                'token': f'{message}',
                'type': 'sms',#sms vs call
            }   
            response = api.verify_lookup(params)
        except APIException as e: 
            print(e)
        except HTTPException as e: 
            print(e)
        # print(message)
    def send_password(self, phone: str, message) -> None:
        self.send(
            phone=phone, 
            message=message
        )
    
    def send_order_message(self, message, phone):

        print(message, phone)
  
# sample of test messaging or dummy
@functools.cache
def get_test_sms_send():
    return TestSendSms()
