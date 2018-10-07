from server import app
from models import Pizza, Choices, db
from sqlalchemy import exc
from catalog import catalog


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
    with app.app_context():
        try:
            insert_data_to_db(catalog)
        except exc.SQLAlchemyError:
            print('Ошибка при выгрузке данных')
