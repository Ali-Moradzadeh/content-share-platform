from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User, UserProfile
from abc import abstractmethod
from constants.testing import SimpleTests


class UserTest(SimpleTests):
    model = User
    list_url = "user-list"
    detail_url = "user-detail"
    list_data = {
        "test1" : {
            "username": "user1",
            "email": "user1@gmail.com",
            "password": "Ali541379?"
        },
        "test2" : {
            "username": "user2",
            "email": "user2@gmail.com",
            "password": "Ali541379?"
        },
    }
    create_data = {
        "username": "user3",
        "email": "user3@gmail.com",
        "password": "Ali541379?"
    }
    test_detail_obj_name = "test1"
    partial_update_data = {
        "username": "user3_updated",
        "email": "user3.updated@gmail.com",
    }
    testing_field = "username"
