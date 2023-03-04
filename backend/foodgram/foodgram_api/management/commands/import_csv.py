from csv import DictReader

from django.core.management.base import BaseCommand
from foodgram_api.models import Ingredient, Tag

CSV_ROOT = "static/data/"
FILE_MODEL = {
    "ingredients.csv": Ingredient,
    "tags.csv": Tag,
}
FK_FIELDS = []


class Command(BaseCommand):
    """Команда импорта csv"""

    help = "Импорт данных из scv"

    def add_arguments(self, parser):
        parser.add_argument(
            "csv_file",
            help=(
                "Enter the csv-file to import.\n"
                "Format: users.csv\n\n"
                "Or nothing to import all."
            ),
            nargs="*",
        )

    def handle(self, **options):
        def importer(csv_file, model):
            url = CSV_ROOT + csv_file
            data = DictReader(open(url, encoding="utf-8"))
            models = []
            for row in data:
                kwargs = {}
                for field, value in row.items():
                    if "_id" in field:
                        field = field[:-3]
                    if field in FK_FIELDS:
                        fk_model = model._meta.get_field(
                            field
                        ).remote_field.model
                        kwargs[field] = fk_model.objects.get(id=value)
                    else:
                        kwargs[field] = value
                models.append(model(**kwargs))
            model.objects.bulk_create(models)
            print('Successfully imported file "%s"' % csv_file)

        if options["csv_file"]:
            for csv_file in options["csv_file"]:
                if csv_file not in FILE_MODEL.keys():
                    raise KeyError('"%s"| Неизвестное имя файла' % csv_file)
                model = FILE_MODEL[csv_file]
                importer(csv_file, model)
        else:
            for csv_file, model in FILE_MODEL.items():
                importer(csv_file, model)
