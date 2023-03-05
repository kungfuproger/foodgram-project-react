"""
Для ревью !/
Братан вообще не парься, тут все уже работает)
Все что надо это:
1. Создать и выполнить миграции
2. Запустить |> python manage.py import_csv |

Нормальная документация (в моем понимании ...)/
Это модуль для импортирования csv файлов в БД.
    1. Поместить в папку: management\commands : в директории
            любого твоего приложения (того которое startapp).
    2. Добавляет managment-команду: import_csv : которая импортирует
            данные из всех csv файлов из директории static\data твоего проекта.
       Доплнительными опциональными параметрами является конструкция : 
            import_csv <имя_csv_файла.csv> <имя_другого_csv_файла.csv> <и_так_далее.csv>
            которая позволяет импортировать не все, а только лишь конкретные файлы.
    3. Необходимые жертвы:
        FILE_MODEL - сюда надо добавить названия csv-файлов в качестве ключей,
            и соответствующие им модели в качестве значений.
        FK_FIELDS - сюда через запятую все поля представленные связью ForeiginKey.
        M2M_FIELDS - а сюда поля ManyToMany как ключи и соответствующие им модели-посредники
            как значения.

    Вот и все настройки. Комфортного использования !
"""
from csv import DictReader

from django.core.management.base import BaseCommand

from foodgram_api.models import Ingredient, IngredientAmount, Recipe, Tag
from users.models import User


CSV_ROOT = "static/data/"
FILE_MODEL = {
    "ingredients.csv": Ingredient,
    "tags.csv": Tag,
    "users.csv": User,
    "ingredients_amount.csv": IngredientAmount,
    "recipes.csv": Recipe,
}
FK_FIELDS = ["ingredient", "author"]
M2M_FIELDS = {"ingredients": IngredientAmount}


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
            n = 0
            m2m_objs = {}
            for row in data:
                n += 1
                id = n
                kwargs = {}
                for field, value in row.items():
                    if "_id" in field:
                        field = field[:-3]
                    if field in FK_FIELDS:
                        fk_model = model._meta.get_field(
                            field
                        ).remote_field.model
                        kwargs[field] = fk_model.objects.get(id=value)
                    elif field in M2M_FIELDS.keys():
                        m2m_model = M2M_FIELDS[field]
                        if id not in m2m_objs:
                            m2m_objs[id] = {}
                        m2m_objs[id][field] = [
                            m2m_model.objects.get(id=value)
                            for value in value.split(";")
                        ]
                    else:
                        kwargs[field] = value
                models.append(model(**kwargs))

            model.objects.bulk_create(models)

            for id, objs in m2m_objs.items():
                model_obj = model.objects.get(id=id)
                for field, objs_list in objs.items():
                    getattr(model_obj, field).set(objs_list)

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
