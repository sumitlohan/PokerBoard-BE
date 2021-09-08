from django.urls import reverse

from rest_framework.test import APITestCase

from apps.user import models as user_models


class CommentTestCases(APITestCase):
    """
    Group testcases for testing group list, details and add member functionality
    """
    COMMENTS_URL = reverse('comment')

    def setUp(self):
        """
        Setup method for creating default user and it's token
        """
        data = {
            "email": "rohit@gmail.com",
            "password": "root",
            "first_name": "Rohit",
            "last_name": "Jain",
        }

        self.user = user_models.User.objects.create(**data)
        self.token = user_models.Token.objects.create(user=self.user).key
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    def test_get_comments(self):
        # response = self.client.get(self.COMMENTS_URL)
        pass

    def test_post_comments(self):
        data = {
            "comment": "Hello there",
            "issue": "KD-2"
        }
        response = self.client.post(self.COMMENTS_URL, data=data)
        res_data = response.data
        self.assertEqual(response.status_code, 201)
        self.assertDictEqual(res_data, data)

    def test_post_comments_with_invalid_issue(self):
        data = {
            "comment": "Hello there",
            "issue": "KD-267"
        }
        response = self.client.post(self.COMMENTS_URL, data=data)
        self.assertEqual(response.status_code, 400)

    def test_post_comments_with_invalid_comment(self):
        data = {
            "comment": "",
            "issue": "KD-2"
        }
        response = self.client.post(self.COMMENTS_URL, data=data)
        self.assertEqual(response.status_code, 400)
