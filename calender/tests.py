# calender/tests.py


# from django.test import TestCase
from .views import send_email_function
from unittest.mock import patch, MagicMock

# calender/tests.py

from django.test import TestCase, SimpleTestCase
from django.contrib.auth.models import User
from django.test import Client

# 로그인한 사용자의 이메일을 가져오는지 확인
class UserEmailTest(TestCase):
    def setUp(self):
        # 테스트 사용자 생성
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='12345')
        self.client = Client()

    def test_user_email(self):
        # 사용자 로그인
        self.client.login(username='testuser', password='12345')

        # 로그인한 사용자의 이메일 주소 가져오기
        user_email = self.user.email

        # 이메일 주소 확인
        self.assertEqual(user_email, 'test@example.com')

# python manage.py test calender.tests.UserEmailTest

# 자동 메일 전송이 되는지 확인
class EmailTest(SimpleTestCase):
    @patch('calender.views.smtplib.SMTP')
    def test_send_email_function(self, mock_smtp):
        # Mock 객체 설정
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        # 함수 호출
        email = 'taegeong@naver.com'
        name = '테스트 재료'
        date = '2023-11-25 00:00:00'
        send_email_function(email, name, date)

        # 함수가 호출되었는지 검증
        mock_server.send_message.assert_called()

        # send_message가 호출된 인자 검증
        args, kwargs = mock_server.send_message.call_args
        sent_message = args[0]

        # 이메일 본문 디코딩
        payload = sent_message.get_payload(decode=True)
        decoded_payload = payload.decode('utf-8')

        self.assertIn(email, sent_message['To'])
        self.assertIn(name, decoded_payload)
        self.assertIn(date, decoded_payload)