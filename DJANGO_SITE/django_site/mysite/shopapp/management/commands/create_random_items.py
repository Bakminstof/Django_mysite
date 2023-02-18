from django.core.management import BaseCommand, CommandParser


from shopapp.funcs import gen_random_item
from shopapp.models import Item


class Command(BaseCommand):
    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('count', type=int, nargs='?', default=1)

    def handle(self, *args, **options) -> None:
        orders_count = options.get('count')

        items = []

        for _ in range(orders_count):
            random_item = gen_random_item()
            items.append(self.__create_item(random_item))

        self.stdout.write(
            self.style.SUCCESS(
                f'Create {len(items)} item{"s" if len(items) >= 2 else ""}'
            )
        )


    def __create_item(self, data: dict) -> Item:
        item = Item.objects.get_or_create(
            name=data['name'],
            description=data['description'],
            price_cent=data['price'],
        )

        self.stdout.write(f'Create item: {data["name"]}')

        return item