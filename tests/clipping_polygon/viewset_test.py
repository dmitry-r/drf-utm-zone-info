from django.contrib.auth.models import User
from django.contrib.gis import geos
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from clipping_geometry.models import ClippingArea


class TestClippingGeometryViewSet(APITestCase):
    def setUp(self):
        self.multipolygon = {
            "type": "MultiPolygon",
            "coordinates": [
                [
                    [[102.0, 2.0], [103.0, 2.0], [103.0, 3.0], [102.0, 3.0], [102.0, 2.0]]
                ],
                [
                    [[100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0]],
                    [[100.2, 0.2], [100.8, 0.2], [100.8, 0.8], [100.2, 0.8], [100.2, 0.2]]
                ]
            ]
        }
        self.polygon = {
            "type": "Polygon",
            "coordinates": [
                [
                    [100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0]
                ],
                [
                    [100.2, 0.2], [100.8, 0.2], [100.8, 0.8], [100.2, 0.8], [100.2, 0.2]
                ]
            ]
        }
        self.something_invalid_that_tries_to_be_a_multipolygon = {
            "type": "MultiPolygon",
            "coordinates": [
                [
                    "this is valid string, but not a valid multipolygon"
                ]
            ]
        }
        self.user = User.objects.create_user(username='lauren', password='lauri', email=None)

    def test_create_view_with_multi_polygon_succeeds(self):
        url = reverse('clipping_area-list')
        expected_name = 'Create new clipping area'
        data = {
            'name': expected_name,
            'clipping_multi_polygon': self.multipolygon,
        }
        self.client.force_authenticate(user=self.user)
        self.assertEqual(0, ClippingArea.objects.count())

        response = self.client.post(url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(1, ClippingArea.objects.count())
        self.assertEqual(expected_name, ClippingArea.objects.first().name)

    def test_create_view_with_polygon_fails(self):
        url = reverse('clipping_area-list')
        count = ClippingArea.objects.count
        self.assertEqual(0, count())
        data = {
            'name': "polygon fails",
            'clipping_multi_polygon': self.polygon,
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(0, count())

        expected_error_message = {
            "clipping_multi_polygon": [
                "The received geometry is not a MultiPolygon. Received type of Polygon."
            ]
        }

        self.assertEqual(expected_error_message, response.data)

    def test_create_view_with_invalid_data_fails(self):
        url = reverse('clipping_area-list')

        count = ClippingArea.objects.count
        self.assertEqual(0, count())

        data = {
            'name': "big fail",
            'clipping_multi_polygon': self.something_invalid_that_tries_to_be_a_multipolygon,
        }

        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(0, count())
        expected_error_message = {
            "clipping_multi_polygon": [
                "Invalid Coordinates, expected at least one coordinate pair, received none."
            ]
        }
        self.assertEqual(expected_error_message, response.data)

    def test_list_view_without_login_fails(self):
        url = reverse('clipping_area-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_view_with_correct_data_succeeds(self):
        p1 = geos.Polygon(((0, 0), (0, 1), (1, 1), (0, 0)))
        p2 = geos.Polygon(((1, 1), (1, 2), (2, 2), (1, 1)))
        multi_polygon = geos.MultiPolygon(p1, p2)
        clipping_area = ClippingArea.objects.create(
            name='test clipping area',
            clipping_multi_polygon=multi_polygon,
        )
        self.assertEqual(1, ClippingArea.objects.count())
        url = reverse('clipping_area-detail', args=[clipping_area.id])
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url, format='json')

        self.assertEqual(0, ClippingArea.objects.count())
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_view_without_login_fails(self):
        p1 = geos.Polygon(((0, 0), (0, 1), (1, 1), (0, 0)))
        p2 = geos.Polygon(((1, 1), (1, 2), (2, 2), (1, 1)))
        multi_polygon = geos.MultiPolygon(p1, p2)
        clipping_area = ClippingArea.objects.create(
            name='test clipping area',
            clipping_multi_polygon=multi_polygon,
        )
        self.assertEqual(1, ClippingArea.objects.count())
        url = reverse('clipping_area-detail', args=[clipping_area.id])
        response = self.client.delete(url, format='json')

        self.assertEqual(1, ClippingArea.objects.count())
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_detail_view_with_correct_data_succeeds(self):
        p1 = geos.Polygon(((0, 0), (0, 1), (1, 1), (0, 0)))
        p2 = geos.Polygon(((1, 1), (1, 2), (2, 2), (1, 1)))
        multi_polygon = geos.MultiPolygon(p1, p2)
        clipping_area = ClippingArea.objects.create(
            name='test clipping area',
            clipping_multi_polygon=multi_polygon,
        )
        url = reverse('clipping_area-detail', args=[clipping_area.id])
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "test clipping area")

    def test_detail_view_without_login_fails(self):
        p1 = geos.Polygon(((0, 0), (0, 1), (1, 1), (0, 0)))
        p2 = geos.Polygon(((1, 1), (1, 2), (2, 2), (1, 1)))
        multi_polygon = geos.MultiPolygon(p1, p2)
        clipping_area = ClippingArea.objects.create(
            name='test clipping area',
            clipping_multi_polygon=multi_polygon,
        )
        url = reverse('clipping_area-detail', args=[clipping_area.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
