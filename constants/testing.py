from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class SimpleTests(APITestCase):
    model = None
    list_url = None
    detail_url = None
    list_data = create_data = partial_update_data = None
    testing_field = None
    test_detail_obj_name = None
   
    def __init_subclass__(self):
        setattr(self, "test_list_model", self.list_model)
        setattr(self, "test_retrieve_model", self.retrieve_model)
        setattr(self, "test_create_model", self.create_model)
        setattr(self, "test_partial_update_model", self.partial_update_model)
    
    def mng(self):
        return self.model._meta.default_manager
    
    def setUp(self):
        self.model_objects_count = self.mng().count()
        for k, v in self.list_data.items():
            setattr(self, k, self.mng().create(**v))
    
    def list_model(self):
        url = reverse(self.list_url)
        rsp = self.client.get(url)
        self.assertEqual(rsp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(rsp.data), self.model_objects_count + len(self.list_data))
    
    def retrieve_model(self):
        field_name = self.testing_field
        nm = self.test_detail_obj_name
        obj = getattr(self, nm)
        url = reverse(self.detail_url, args=[obj.pk])
        rsp = self.client.get(url)
        self.assertEqual(rsp.status_code, status.HTTP_200_OK)
        self.assertEqual(rsp.data[field_name], getattr(obj, field_name))
    
    
    def create_model(self):
        url = reverse(self.list_url)
        rsp = self.client.post(url, data=self.create_data, format="json")
        self.assertEqual(rsp.status_code, status.HTTP_201_CREATED)
        t = self.testing_field
        self.assertEqual(getattr(self.mng().last(), t), self.create_data[t])
        self.assertEqual(self.mng().count(), self.model_objects_count + len(self.list_data) + 1)
    
    def partial_update_model(self):
        obj_nm = self.test_detail_obj_name
        field_name = self.testing_field
        obj = getattr(self, obj_nm)
        url = reverse(self.detail_url, args=[obj.pk])
        rsp = self.client.patch(url, data=self.partial_update_data, format="json")
        self.assertEqual(rsp.status_code, status.HTTP_200_OK)
        self.assertEqual(rsp.data[field_name], self.partial_update_data[field_name])
    
    