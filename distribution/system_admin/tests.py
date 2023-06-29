from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


# Create your tests here.
class YourAPITestCase(APITestCase):
    def test_list_objects(self):
        url = reverse(
            "your-api-list"
        )  # Thay thế 'your-api-list' bằng tên URL của API view của bạn
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Kiểm tra logic xử lý và kiểm tra kết quả đầu ra

    def test_retrieve_object(self):
        url = reverse(
            "your-api-detail", args=[1]
        )  # Thay thế 'your-api-detail' và 1 bằng tên URL và ID của đối tượng bạn muốn truy vấn
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Kiểm tra logic xử lý và kiểm tra kết quả đầu ra

    def test_create_object(self):
        url = reverse("your-api-list")
        data = {
            "field1": "value1",
            "field2": "value2",
        }  # Thay thế các trường và giá trị tương ứng
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
