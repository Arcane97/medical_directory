from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import localdate
from rest_framework import status

from .. import models, serializers


class ReferenceBookListViewTestCase(TestCase):
    def setUp(self):
        self.ref_book1 = models.ReferenceBook.objects.create(
            code='ref_book1',
            name='Справочник 1',
        )
        self.ref_book2 = models.ReferenceBook.objects.create(
            code='ref_book2',
            name='Справочник 2',
        )
        self.ref_book3 = models.ReferenceBook.objects.create(
            code='ref_book3',
            name='Справочник 3',
        )
        self.version1 = models.ReferenceBookVersion.objects.create(
            ref_book=self.ref_book1,
            version='1.0',
            date=localdate() - timedelta(days=1),
        )
        self.version2 = models.ReferenceBookVersion.objects.create(
            ref_book=self.ref_book2,
            version='1.0',
            date=localdate() + timedelta(days=1),
        )
        self.version3 = models.ReferenceBookVersion.objects.create(
            ref_book=self.ref_book3,
            version='1.0',
            date=localdate() - timedelta(days=1),
        )
        self.element1 = models.ReferenceBookElement.objects.create(
            ref_book_version=self.version1,
            code='code1',
            value='Value 1',
        )
        self.element2 = models.ReferenceBookElement.objects.create(
            ref_book_version=self.version2,
            code='code2',
            value='Value 2',
        )
        self.element3 = models.ReferenceBookElement.objects.create(
            ref_book_version=self.version3,
            code='code3',
            value='Value 3',
        )

    def test_list_all_ref_books(self):
        url = reverse('referencebook-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['refbooks']), 3)
        self.assertEqual(
            list([b['code'] for b in response.data['refbooks']]),
            [self.ref_book1.code, self.ref_book2.code, self.ref_book3.code]
        )

    def test_list_ref_books_with_date(self):
        url = reverse('referencebook-list')
        date = localdate() - timedelta(days=1)
        response = self.client.get(url, {'date': date.isoformat()})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['refbooks']), 2)
        self.assertEqual(
            list([b['code'] for b in response.data['refbooks']]),
            [self.ref_book1.code, self.ref_book3.code]
        )

    def test_list_ref_books_with_invalid_date(self):
        url = reverse('referencebook-list')
        invalid_date = 'invalid date'
        response = self.client.get(url, {'date': invalid_date})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data,
            {
                "date": [
                    "Неправильный формат date. Используйте один из этих форматов: YYYY-MM-DD."
                ]
            }
        )


class ReferenceBookElementListViewTest(TestCase):
    def setUp(self):
        self.ref_book = models.ReferenceBook.objects.create(code='test_ref_book', name='Test Reference Book')
        self.version1 = models.ReferenceBookVersion.objects.create(
            ref_book=self.ref_book,
            version='1.0',
            date=localdate(),
        )
        self.element1 = models.ReferenceBookElement.objects.create(
            ref_book_version=self.version1,
            code='test_element1',
            value='Test Element'
        )
        self.element2 = models.ReferenceBookElement.objects.create(
            ref_book_version=self.version1,
            code='test_element2',
            value='Test Element'
        )

    def test_get_elements_by_ref_book_id(self):
        url = reverse('refbooks-elements-list', kwargs={"id": self.ref_book.id})
        response = self.client.get(url)
        serializer = serializers.ReferenceBookElementSerializer([self.element1, self.element2], many=True)
        self.assertEqual(response.data, {'elements': serializer.data})
        self.assertEqual(response.status_code, 200)

    def test_get_elements_by_ref_book_id_and_version(self):
        url = reverse('refbooks-elements-list', kwargs={"id": self.ref_book.id})
        response = self.client.get(url, {'version': self.version1.version})
        serializer = serializers.ReferenceBookElementSerializer([self.element1, self.element2], many=True)
        self.assertEqual(response.data, {'elements': serializer.data})
        self.assertEqual(response.status_code, 200)

    def test_get_elements_by_ref_book_id_and_non_existing_version(self):
        url = reverse('refbooks-elements-list', kwargs={"id": self.ref_book.id})
        response = self.client.get(url, {'version': "2.0"})
        self.assertEqual(response.data, {'elements': []})
        self.assertEqual(response.status_code, 200)

    def test_get_elements_by_invalid_version(self):
        url = reverse('refbooks-elements-list', kwargs={"id": self.ref_book.id})
        invalid_version = "1" * 52
        response = self.client.get(url, {'version': invalid_version})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data,
            {
                "version": [
                    "Убедитесь, что это значение содержит не более 50 символов."
                ]
            }
        )


class ElementValidationViewTestCase(TestCase):
    def setUp(self):
        self.ref_book = models.ReferenceBook.objects.create(code='ref_book1', name='Справочник 1')
        self.version1 = models.ReferenceBookVersion.objects.create(ref_book=self.ref_book, version='1.0',
                                                                   date=localdate() - timedelta(days=1))
        self.version2 = models.ReferenceBookVersion.objects.create(ref_book=self.ref_book, version='2.0',
                                                                   date=localdate())

        ref_book_element_1 = models.ReferenceBookElement.objects.create(
            code="elem1",
            value="Element 1",
            ref_book_version=self.version2,
        )
        ref_book_element_2 = models.ReferenceBookElement.objects.create(
            code="elem2",
            value="Element 2",
            ref_book_version=self.version2,
        )
        ref_book_element_3 = models.ReferenceBookElement.objects.create(
            code="elem3",
            value="Element 3",
            ref_book_version=self.version1,
        )

    def test_validate_element_with_valid_data(self):
        url = reverse("element-validation", kwargs={"id": self.ref_book.id})
        data = {"code": "elem1", "value": "Element 1"}
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["exists"], True)

    def test_validate_element_with_valid_data_and_version(self):
        url = reverse("element-validation", kwargs={"id": self.ref_book.id})
        data = {"code": "elem3", "value": "Element 3", "version": "1.0"}
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["exists"], True)

    def test_validate_element_with_invalid_data(self):
        url = reverse("element-validation", kwargs={"id": self.ref_book.id})
        data = {"code": "elem1", "value": "Invalid value"}
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["exists"], False)

    def test_validate_element_missing_code_and_value_parameter(self):
        url = reverse("element-validation", kwargs={"id": self.ref_book.id})
        data = {"version": "1.0"}
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data,
            {
                "code": [
                    "Обязательное поле."
                ],
                "value": [
                    "Обязательное поле."
                ]
            }
        )

    def test_validate_element_missing_code_parameter(self):
        url = reverse("element-validation", kwargs={"id": self.ref_book.id})
        data = {"value": "value 1", "version": "1.0"}
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data,
            {
                "code": [
                    "Обязательное поле."
                ]
            }
        )

    def test_validate_element_missing_value_parameter(self):
        url = reverse("element-validation", kwargs={"id": self.ref_book.id})
        data = {"code": "100", "version": "1.0"}
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data,
            {
                "value": [
                    "Обязательное поле."
                ]
            }
        )
