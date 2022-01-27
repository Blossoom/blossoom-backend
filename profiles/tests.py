from rest_framework.test import APITestCase
from rest_framework import status
# Create your tests here.


class ProfilesTestCase(APITestCase):

    def setUp(self) -> None:

        from django.contrib.auth.models import User

        self.base_api = "/api/v1/users/"

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

    def user_login(self):
        response = self.client.post(self.base_api + 'login/', self.login_cred)
        return response.json()['access'], response.json()['refresh']
    
    def test_get_all_users(self):
        response = self.client.get(self.base_api)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()[0]['id'], 1)


    def test_get_user_pk(self):
        response = self.client.get(self.base_api + '1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['id'], 1)

    def test_get_user_followers(self):
        response = self.client.get(self.base_api + '1/followers/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), [])

    def test_get_user_followings(self):
        response = self.client.get(self.base_api + '1/followings/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), [])


class ProfileRelationshipTestCase(APITestCase):

    def setUp(self) -> None:

        from django.contrib.auth.models import User

        self.base_api = "/api/v1/users/"

        user_object_1 = User.objects.create_user(
            **{
            "email": "testinguser@gmail.com",
            "username": "testuser",
            "password": "AZER1234",
        }
        )
        user_object_1.save()

        user_object_2 = User.objects.create_user(
            **{
            "email": "testinguser2@gmail.com",
            "username": "testuser2",
            "password": "AZER1234",
        }
        )
        user_object_2.save()

        self.login_cred = {
            "username": "testuser",
            "password": "AZER1234"
        }

        self.login_cred_2 = {
            "username": "testuser2",
            "password": "AZER1234"
        }

        return super().setUp()

    def user_login(self):
        response = self.client.post('/api/v1/auth/login/', self.login_cred)
        return response.json()['access'], response.json()['refresh']


    def test_follow_without_creds(self):
        response = self.client.get(self.base_api + '2/follow/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json(), {"detail": "Authentication credentials were not provided."})



    def test_follow_unfollow_action(self):
        access, _ = self.user_login()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access)
        response = self.client.get(self.base_api + '2/follow/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'detail': 'Follow success.'})

        response = self.client.get(self.base_api + '2/follow/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'detail': 'Unfollow success.'})

    