import time
from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write("Connecting to the DB...")
        conn = None
        while not conn:
            try:
                conn = connections['default']
            except OperationalError:
                time.sleep(1)
                self.stdout.write("DB not available, waiting 1s...")

        self.stdout.write(self.style.SUCCESS("DB connection successfull"))
