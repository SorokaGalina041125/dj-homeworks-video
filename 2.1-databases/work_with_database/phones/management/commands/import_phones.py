import csv
from decimal import Decimal

from django.core.management.base import BaseCommand
from phones.models import Phone


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        with open('phones.csv', 'r') as file:
            phones = list(csv.DictReader(file, delimiter=';'))

        for phone in phones:
            phone_obj = Phone(
                id=int(phone['id']),
                name=phone['name'],
                price=Decimal(phone['price']),
                image=phone['image'],
                release_date=phone['release_date'],
                lte_exists=phone['lte_exists'].lower() == 'true',
                       
            )
            phone_obj.save()
            self.stdout.write(self.style.SUCCESS(f'Добавлен телефон: {phone_obj.name} (slug:{phone_obj.slug})'))
            
        self.stdout.write(self.style.SUCCESS(f'Всего добавлено телефонов: {len(phones)}'))