import datetime
import asyncio
from pprint import pprint
from more_itertools import chunked
import aiohttp
from models import init_db, SwapiPeople, Session, engine
import requests

MAX_CHUNK = 5


async def get_person(client, person_id):
    http_response = await client.get(f'http://swapi.py4e.com/api/people/{person_id}')
    json_result = await http_response.json()
    return json_result


async def get_data(client, url):
    http_response = await client.get(f'{url}')
    json_result = await http_response.json()
    return json_result


async def insert_to_db(list_of_json):
    models = SwapiPeople(**list_of_json)
    async with Session() as session:
        session.add(models)
        await session.commit()


async def main():
    await init_db()
    client = aiohttp.ClientSession()
    for chunk in chunked(range(1, 51), MAX_CHUNK):
        coros_person = [get_person(client, person_id) for person_id in chunk]
        result_person = await asyncio.gather(*coros_person)
        datas = (person for person in result_person)

        for j, data in enumerate(datas):
            try:
                result_dict = {
                    'id_person': chunk[j],
                    'birth_year': data['birth_year'],
                    'eye_color': data['eye_color'],
                    'gender': data['gender'],
                    'hair_color': data['hair_color'],
                    'height': data['height'],
                    'homeworld': data['name'],
                    'mass': data['mass'],
                    'name': data['name'],
                    'skin_color': data['skin_color']
                }
            except:
                continue

            buff = []
            for film in data['films']:
                coros_films = [get_data(client, film)]
                result_film = await asyncio.gather(*coros_films)
                buff.append(result_film[0]['title'])
            result_dict['films'] = ', '.join(buff)

            buff = []
            for specie in data['species']:
                coros_species = [get_data(client, specie)]
                result_species = await asyncio.gather(*coros_species)
                buff.append(result_species[0]['classification'])
            result_dict['species'] = ', '.join(buff)

            buff = []
            for starship in data['starships']:
                coros_starships = [get_data(client, starship)]
                result_starships = await asyncio.gather(*coros_starships)
                buff.append(result_starships[0]['name'])
            result_dict['starships'] = ', '.join(buff)

            buff = []
            for vehicle in data['vehicles']:
                coros_vehicles = [get_data(client, vehicle)]
                result_vehicles = await asyncio.gather(*coros_vehicles)
                buff.append(result_vehicles[0]['name'])
            result_dict['vehicles'] = ', '.join(buff)

            print(result_dict)
            asyncio.create_task(insert_to_db(result_dict))
    tasks_set = asyncio.all_tasks() - {asyncio.current_task()}
    await asyncio.gather(*tasks_set)
    await client.close()
    await engine.dispose()


if __name__ == "__main__":
    start = datetime.datetime.now()
    asyncio.run(main())
    print(datetime.datetime.now() - start)
