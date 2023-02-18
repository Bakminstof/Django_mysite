from django.core.management import BaseCommand

from shopapp.models import Discount, Tax


class Command(BaseCommand):
    def handle(self, *args, **options) -> None:
        self.__create_zero_discount()
        self.__create_zero_tax()

    @staticmethod
    def __create_zero_tax() -> None:
        Tax.objects.get_or_create(value=0)

    @staticmethod
    def __create_zero_discount() -> None:
        Discount.objects.get_or_create(value=0)
