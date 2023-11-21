from typing import Any
from django.core.management import BaseCommand
import json
import os
from pathlib import Path
from core.models import Listing


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any):
        path = Path(__file__).resolve().parent.parent.parent / "scraper/data/data.json"

        with open(path) as fd:
            data = json.load(fd)
            for i in data:
                try:
                    Listing.objects.create(**i)
                except:
                    continue
