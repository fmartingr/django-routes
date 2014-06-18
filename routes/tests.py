from django.test import TestCase
from .models import Route


class RouteModelTestCase(TestCase):
    def create_objects(self, objects):
        """
        Creates list of dict()s as Route objects
        Assumes Route.order as Route.pk
        """
        for route in objects:
            route['order'] = route['pk']
            Route.objects.create(**route)

    def test_url_path_is_saved(self):
        """
        Tests if the full relative path to this URL is saved in the ddbb
        """
        self.create_objects([
            {'pk': 1, 'name': 'Forums', 'slug': 'forums/test/'},
            {'pk': 2, 'name': 'Forum 1', 'slug': 'forum-1', 'parent_id': 1},
        ])
        for route in Route.objects.all():
            self.assertEqual(route.cached_pattern,
                             route.get_relative_url())

        # Test recursive routes
        route = Route.objects.get(pk=2)
        self.assertTrue(route.parent.cached_pattern in route.cached_pattern)

    def test_slug_is_cleaned(self):
        """
        Check if clean function removes trailing slash but allows slashes
        to be in the middle of slugs
        """
        self.create_objects([
            {'pk': 99, 'name': 'Bogus slug', 'slug': 'bogus/'},
            {'pk': 98, 'name': 'Bogus slug 2', 'slug': 'bogus/test'},
        ])

        self.assertFalse(Route.objects.get(pk=99).slug[-1] == '/')
        self.assertTrue('/' in Route.objects.get(pk=98).slug)

    def test_create_without_slug(self):
        """
        Test if we broke something when creating a route without a slug
        """
        self.create_objects([
            {'pk': 3, 'name': 'No slug', 'slug': '', 'order': 2},
        ])

        obj = Route.objects.get(pk=3)
        self.assertTrue(obj.slug == '')


class RouteApphooksTestCase(TestCase):
    def setUp(self):
        pass

    def test_choices_loaded_from_pool(self):
        pass
