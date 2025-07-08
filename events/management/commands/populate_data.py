# events/management/commands/populate_data.py
from django.core.management.base import BaseCommand, CommandError
from events.models import Category, Event, Participant
from datetime import date, time

class Command(BaseCommand):
    help = 'Populates the database with dummy event, participant, and category data.'

    def handle(self, *args, **options):
        self.stdout.write("Clearing existing data...")
        # Clear existing data to avoid duplicates if running multiple times
        Participant.objects.all().delete()
        Event.objects.all().delete()
        Category.objects.all().delete()
        self.stdout.write("Existing data cleared.")

        self.stdout.write("Creating dummy categories...")
        cat1 = Category.objects.create(name='Conference', description='Large-scale professional gatherings.')
        cat2 = Category.objects.create(name='Workshop', description='Hands-on learning sessions.')
        cat3 = Category.objects.create(name='Concert', description='Live music performances.')
        self.stdout.write(self.style.SUCCESS("Categories created."))

        self.stdout.write("Creating dummy events...")
        event1 = Event.objects.create(
            name='Tech Innovation Summit',
            description='A summit showcasing the latest in tech.',
            date=date(2025, 7, 20),
            time=time(9, 0),
            location='Convention Center A',
            category=cat1
        )
        event2 = Event.objects.create(
            name='Python Web Development Workshop',
            description='Learn Django and Flask basics.',
            date=date(2025, 8, 5),
            time=time(14, 0),
            location='Online (Zoom)',
            category=cat2
        )
        event3 = Event.objects.create(
            name='Summer Music Fest',
            description='Annual outdoor music festival.',
            date=date(2025, 7, 15),
            time=time(18, 30),
            location='City Park Amphitheater',
            category=cat3
        )
        event4 = Event.objects.create(
            name='Data Science Conference',
            description='Exploring trends in AI and ML.',
            date=date(2025, 9, 10),
            time=time(9, 30),
            location='Grand Hotel Ballroom',
            category=cat1
        )
        self.stdout.write(self.style.SUCCESS("Events created."))

        self.stdout.write("Creating dummy participants...")
        p1 = Participant.objects.create(name='Alice Smith', email='alice@example.com')
        p2 = Participant.objects.create(name='Bob Johnson', email='bob@example.com')
        p3 = Participant.objects.create(name='Charlie Brown', email='charlie@example.com')
        p4 = Participant.objects.create(name='Diana Prince', email='diana@example.com')
        self.stdout.write(self.style.SUCCESS("Participants created."))

        self.stdout.write("Assigning participants to events...")
        p1.events.add(event1, event2)
        p2.events.add(event1, event3)
        p3.events.add(event2)
        p4.events.add(event1, event2, event3, event4)
        self.stdout.write(self.style.SUCCESS("Participants assigned to events."))

        self.stdout.write(self.style.SUCCESS('Successfully populated dummy data!'))
