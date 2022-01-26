from rest_framework import status
from rest_framework.test import APITestCase

# Create your tests here.


class UserRegistrationTestCase(APITestCase):


    def setUp(self) -> None:
        self.data = {
            "email": "testinguser@gmail.com",
            "username": "testuser",
            "password": "AZER1234",
            "password_2": "AZER1234",
        }

        self.base_api = "/api/v1/auth/register/"

        return super().setUp()


    def test_user_registration_valid_data(self):
        response = self.client.post(self.base_api, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_registration_wrong_email(self):
        self.data['email'] = "qdsqlskdmslfqùf"
        response = self.client.post(self.base_api, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(),  {"email": ["Enter a valid email address."]})

    def test_user_registration_wrong_passwords(self):
        """ User registration where passwords dont match.
        """
        self.data['password'] = "A"
        response = self.client.post(self.base_api, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(),  {"password": ["password and confirm_password didn't match."]})



class UserLoginTestCase(APITestCase):

    def setUp(self) -> None:

        from django.contrib.auth.models import User

        self.base_api = "/api/v1/auth/"

        user_object = User.objects.create_user(
            **{
            "email": "testinguser@gmail.com",
            "username": "testuser",
            "password": "AZER1234",
        }
        )
        user_object.save()

        self.login_cred = {
            "username": "testuser",
            "password": "AZER1234"
        }
        return super().setUp()

    @property
    def user_login(self):
        response = self.client.post(self.base_api + 'login/', self.login_cred)
        return response.json()['access'], response.json()['refresh']

    def test_user_login(self):

        response = self.client.post(self.base_api + 'login/', self.login_cred)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'access')
        self.assertContains(response, 'refresh')

        self.access_token = response.json()['access']
        self.refresh_token = response.json()['refresh']

    def test_user_login_wrong_cred(self):

        self.login_cred['username'] += 'E'
        response = self.client.post(self.base_api + 'login/', self.login_cred)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json(), {"detail": "No active account found with the given credentials"})


    def test_user_login_refresh_token(self, supply_refersh=None):
        if supply_refersh is None:
            _, refresh = self.user_login  
        else:
            refresh = supply_refersh
        response = self.client.post(self.base_api + 'login/refresh/', {"refresh": refresh})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "access")

    def test_blacklist_token_after_logout(self):

        _, refresh = self.user_login
        response = self.client.post(self.base_api + 'logout/', {"refresh": refresh})
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)

        # check if token got blacklisted
        response = self.client.post(self.base_api + 'login/refresh/', {"refresh": refresh})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json(), {'detail': 'Token is blacklisted', 'code': 'token_not_valid'}
)
