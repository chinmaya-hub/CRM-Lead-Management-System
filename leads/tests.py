from django.test import TestCase
from django.contrib.auth.models import User, Group
from django.urls import reverse

from rest_framework.test import APIClient

from .models import Lead, Activity, FollowUp, Customer


class LeadModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='salesperson1',
            password='TestPass123!'
        )

        self.lead = Lead.objects.create(
            name='Rahul Sharma',
            email='rahul@example.com',
            phone='9876543210',
            company='Tech Solutions',
            source='Website',
            status='New',
            score=75,
            assigned_to=self.user,
        )

    def test_lead_creation(self):
        self.assertEqual(self.lead.name, 'Rahul Sharma')
        self.assertEqual(self.lead.status, 'New')

    def test_lead_string_representation(self):
        self.assertEqual(str(self.lead), 'Rahul Sharma')

    def test_activity_creation(self):
        activity = Activity.objects.create(
            lead=self.lead,
            activity_type='Call',
            description='Initial discussion',
        )

        self.assertEqual(activity.lead, self.lead)
        self.assertEqual(activity.activity_type, 'Call')

    def test_followup_creation(self):
        from django.utils import timezone

        followup = FollowUp.objects.create(
            lead=self.lead,
            scheduled_at=timezone.now(),
            note='Call the lead tomorrow',
        )

        self.assertEqual(followup.lead, self.lead)
        self.assertFalse(followup.completed)

    def test_customer_conversion_record(self):
        customer = Customer.objects.create(lead=self.lead)

        self.assertEqual(customer.lead, self.lead)
        self.assertEqual(Customer.objects.count(), 1)


class LeadPageTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testadmin',
            password='TestPass123!',
            is_staff=True,
        )

        self.lead = Lead.objects.create(
            name='Test Lead',
            email='test@example.com',
            source='Website',
            status='New',
        )

    def test_dashboard_loads(self):
        response = self.client.get(reverse('dashboard'))

        self.assertEqual(response.status_code, 200)

    def test_lead_list_loads(self):
        response = self.client.get(reverse('lead_list'))

        self.assertEqual(response.status_code, 200)

    def test_add_lead_page_loads(self):
        response = self.client.get(reverse('add_lead'))

        self.assertEqual(response.status_code, 200)


class LeadAPITests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='apiadmin',
            password='TestPass123!',
            is_staff=True,
        )

        self.lead = Lead.objects.create(
            name='API Test Lead',
            email='api@example.com',
            source='Website',
            status='New',
            assigned_to=self.user,
        )

        self.client_api = APIClient()

    def test_anonymous_api_access_is_denied(self):
        response = self.client_api.get('/api/leads/')

        self.assertIn(response.status_code, [401, 403])

    def test_authenticated_admin_can_list_leads(self):
        self.client_api.force_authenticate(user=self.user)

        response = self.client_api.get('/api/leads/')

        self.assertEqual(response.status_code, 200)

    def test_admin_can_retrieve_lead(self):
        self.client_api.force_authenticate(user=self.user)

        response = self.client_api.get(
            f'/api/leads/{self.lead.id}/'
        )

        self.assertEqual(response.status_code, 200)

    def test_salesperson_group_setup(self):
        salesperson_group, _ = Group.objects.get_or_create(
            name='Salesperson'
        )

        salesperson = User.objects.create_user(
            username='salesperson_test',
            password='TestPass123!',
        )

        salesperson.groups.add(salesperson_group)

        self.lead.assigned_to = salesperson
        self.lead.save()

        self.client_api.force_authenticate(user=salesperson)

        response = self.client_api.get('/api/leads/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(
            response.data['results'][0]['id'],
            self.lead.id,
        )