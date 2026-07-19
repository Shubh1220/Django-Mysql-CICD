from django.test import TestCase
from django.urls import reverse

from .models import Note


class NoteModelTests(TestCase):
    def test_create_note(self):
        note = Note.objects.create(title="Test", content="Hello world")
        self.assertEqual(str(note), "Test")
        self.assertEqual(Note.objects.count(), 1)


class NoteViewTests(TestCase):
    def test_note_list_status_code(self):
        response = self.client.get(reverse('note_list'))
        self.assertEqual(response.status_code, 200)

    def test_health_check(self):
        response = self.client.get(reverse('health_check'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'ok')

    def test_note_create(self):
        self.client.post(reverse('note_create'), {'title': 'New', 'content': 'Body'})
        self.assertEqual(Note.objects.filter(title='New').count(), 1)
