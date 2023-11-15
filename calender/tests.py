# calender/tests.py


from django.test import TestCase
from .views import send_email_function
from unittest.mock import patch, MagicMock

class EmailTest(TestCase):
    @patch('calender.views.smtplib.SMTP')
    def test_send_email_function(self, mock_smtp):
        # Mock 객체 설정
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        # 함수 호출
        email = 'test@example.com'
        name = '테스트 재료'
        date = '2023-11-20'
        send_email_function(email, name, date)

        # 함수가 호출되었는지 검증
        mock_server.send_message.assert_called()

        # send_message가 호출된 인자 검증
        args, kwargs = mock_server.send_message.call_args
        sent_message = args[0]
        self.assertIn(email, sent_message['To'])
        self.assertIn(name, sent_message.get_payload())
        self.assertIn(date, sent_message.get_payload())