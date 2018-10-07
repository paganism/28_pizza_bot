from server import app
from models import Pizza, Choices, db
from sqlalchemy import exc
import argparse
import os
import json


def load_data(filepath):
    with open(filepath, 'r') as f:
        raw_data = f.read()
    return json.loads(raw_data)


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--path',
        dest='path',
        required=True,
        help='Path to json file'
    )
    return parser.parse_args()


def insert_data_to_db(loaded_json):
    for pizza in loaded_json:
        pizza_to_insert = Pizza(
            title=pizza['title'],
            description=pizza['description']
            )
        for choice in pizza['choices']:
            choices_to_insert = Choices(choice_title=choice['title'],
                                        choice_price=choice['price'],
                                        pizza=pizza_to_insert)
            db.session.add(choices_to_insert)
        db.session.add(pizza_to_insert)
        db.session.commit()


if __name__ == '__main__':
    args = parse_arguments()
    if not os.path.exists(args.path) or not args.path:
        sys.exit('Некорректно указан аргумент')
    catalog = load_data(args.path)
    with app.app_context():
        try:
            insert_data_to_db(catalog)
        except exc.SQLAlchemyError:
            print('Ошибка при выгрузке данных')
