import asyncio

from bot.core.configuration import Configuration
from motor.motor_asyncio import AsyncIOMotorClient
import sys
import argparse

# testing

database_client = AsyncIOMotorClient(Configuration.database_connection())

database = database_client.notes_bot


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-action', default='skip', help='доступные действия:  add_field (--collection, --field_name, --value)')
    parser.add_argument('--collection', default='skip', help='имя коллекции в которой надо что-то изменить')
    parser.add_argument('--field_name', default='skip', help='имя поля которое надо что-то изменить')
    parser.add_argument('--value', default='skip', help='значение которое нужно использовать')


    return parser
async def add_field(namespace) -> None:
    namespace.value = eval(namespace.value)
    print(type(namespace.value))
    confirm = int(input(
        f'ты правда хочешь добавить поле {namespace.field_name} со значением {namespace.value} в коллекцию {namespace.collection} ? - 0/1: '))
    if confirm == 0:
        raise KeyboardInterrupt
    if namespace.collection == 'users':
        replaced = 0
        async for i in database.users.find():
            i_new: dict = i.copy()
            i_new.pop('_id')
            i_new[namespace.field_name] = namespace.value
            await database.users.replace_one(dict(_id=i['_id']), i_new)
            replaced += 1
        print(f'процесс закончен изменено {replaced} обьектов')
    if namespace.collection == 'notes':
        replaced = 0
        async for i in database.notes.find():
            i_new: dict = i.copy()
            i_new.pop('_id')
            i[namespace.field_name] = namespace.value
            await database.notes.replace_one(dict(_id=i['_id']), i_new)
            replaced += 1
        print(f'процесс закончен изменено {replaced} обьектов')


if __name__ == '__main__':
    parser = create_parser()
    namespace = parser.parse_args(sys.argv[1:])

    print(namespace)

    match namespace.action:
        case "add_field":
            asyncio.run(add_field(namespace))
