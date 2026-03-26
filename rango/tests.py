from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rango.calculator import calculate_1rm, calculate
from rango.models import UserProfile

class CalculatorTests(TestCase):
    def test_calculate_1rm_single_rep(self):
        """Testing 1RM calculation for a single rep returns the exact weight"""
        self.assertEqual(calculate_1rm(100.0, 1), 100.0)

    def test_calculate_invalid_inputs(self):
        """Testing that invalid inputs raise ValueError"""
        with self.assertRaises(ValueError):
            calculate('squat', weight=-10, reps=5, bodyweight=80, gender='male')
        
        with self.assertRaises(ValueError):
             calculate('bench-press', weight=100, reps=0, bodyweight=80, gender='male')

class ViewTests(TestCase):
    def setUp(self):
        # Create a test user to use across view tests
        self.user = User.objects.create_user(username='testuser', password='testpassword123')
        self.profile = UserProfile.objects.create(
            user=self.user, age=25, bodyweight=80.0, gender='male',
            squat_1rm=100, bench_1rm=80, deadlift_1rm=120
        )

    def test_home_view_redirects_unauthenticated(self):
        """Test that unauthenticated users are redirected from home page to login"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse('login')))

    def test_home_view_authenticated(self):
        """Test that authenticated users can access the home page and render the correct template"""
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rango/index.html')
