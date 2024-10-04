from authentication.pkg.sms.test.dummy import get_test_sms_send

def get_sms_service():
    service_name = 'test'

    match service_name:
        case 'test':
            return get_test_sms_send()



