import random
import datetime
from django.core.management.base import BaseCommand
from analytics.models import Visit
from faker import Faker

class Command(BaseCommand):
    help = 'Generate random visit records'

    def add_arguments(self, parser):
        parser.add_argument('num_records', type=int, help='Number of random visits to generate')

    def handle(self, *args, **kwargs):
        num_records = kwargs['num_records']
        fake = Faker()

        countries = [
            "United States", "Canada", "Russia", "Germany", "France", "India", "China", 
            "Brazil", "South Africa", "Australia", "Mexico", "Japan", "South Korea"
        ]

        for _ in range(num_records):
            country = random.choice(countries)
            city = fake.city()
            ip = fake.ipv4()
            mobile = random.choice([True, False])

            # Generate a random timestamp within the last 30 days
            entered_at = fake.date_time_between(start_date='-30d', end_date='now')
            # Visit duration between 1 minute and 60 minutes
            visit_duration = datetime.timedelta(minutes=random.randint(1, 60))
            left_at = entered_at + visit_duration

            # Create and save the visit record
            Visit.objects.create(
                url=fake.url(),
                ip=ip,
                country=country,
                city=city,
                mobile=mobile,
                entered_at=entered_at,
                left_at=left_at
            )

        self.stdout.write(self.style.SUCCESS(f'Successfully created {num_records} random visit records'))
