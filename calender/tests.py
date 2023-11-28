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

# 자동 메일 전송이 되는지 확인 -> 성공
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

        expected_date_format_in_payload = '소비기한: 2023-11-25'

        self.assertIn(email, sent_message['To'])

        # Handling multipart messages
        if sent_message.is_multipart():
            payload = ''.join(part.get_payload(decode=True).decode('utf-8') for part in sent_message.get_payload())
        else:
            payload = sent_message.get_payload(decode=True).decode('utf-8')

        self.assertIn(name, payload)
        self.assertIn(expected_date_format_in_payload, payload)


from django.test import TestCase
from django.urls import reverse
from .models import Events
from django.contrib.auth.models import User

class RemoveEventTestCase(TestCase):
    def setUp(self):
        # 테스트 사용자와 이벤트 생성
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.event = Events.objects.create(name='Test Event', user=self.user)

    def test_remove_event(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('remove-event'), {'id': self.event.id})
        self.assertEqual(response.status_code, 200)
        # 이벤트가 삭제되었는지 확인
        self.assertFalse(Events.objects.filter(id=self.event.id).exists())
