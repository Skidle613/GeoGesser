import os
import time as tiime

import discord
from random import shuffle

import requests

from key import TOKEN
from data.db_session import global_init, create_session
from data.user import User
from data.country import Country
from random import randrange

giving_roles = [(10, 'Новичок в географии'), (50, 'Начинающий географ'), (100, 'Любитель географии'),
                (200, 'Прошаренный географ'), (500, 'Знаток географии'), (1000, 'Настоящий мастер в географии'),
                (1500, 'Гуру-географ')]


async def score_count(user, message, db_sess):
    score = user.score
    roles = message.author.guild.roles
    for elem in giving_roles:
        if score == elem[0]:
            if elem[1] not in [role.name for role in roles]:
                await message.author.guild.create_role(name=elem[1],
                                                       color=discord.Color.from_rgb(randrange(256), randrange(256),
                                                                                    randrange(256)))
            roles = message.author.guild.roles
            role_id = [role.id for role in roles if role.name == elem[1]][0]
            await message.author.add_roles(discord.Object(role_id))
            if elem[0] != 10:
                role_for_delete = [elem_ for elem_ in message.author.guild.roles if
                                   elem_.name == giving_roles[giving_roles.index(elem) - 1][1]][0]
                await message.author.remove_roles(role_for_delete)
            if elem[0] == 100:
                user.difficult = 2
                db_sess.commit()
            elif elem[0] == 500:
                user.difficult = 3
                db_sess.commit()


# def picture_of_object(toponym_to_find):
#     # Возвращает контент картинки, который надо записать в файл
#     geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
#     geocoder_params = {
#         "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
#         "geocode": toponym_to_find,
#         "format": "json"}
#     response = requests.get(geocoder_api_server, params=geocoder_params)
#     json_response = response.json()
#     toponym = json_response["response"]["GeoObjectCollection"][
#         "featureMember"][0]["GeoObject"]
#
#     toponym_coodrinates = toponym["Point"]["pos"]
#     toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
#
#     lower_corner = toponym['boundedBy']['Envelope']['lowerCorner'].split()
#     upper_corner = toponym['boundedBy']['Envelope']['upperCorner'].split()
#     delta1 = abs(float(upper_corner[0]) - float(lower_corner[0]))
#     delta2 = abs(float(upper_corner[1]) - float(upper_corner[1]))
#     map_params = {
#         'll': ",".join([toponym_longitude, toponym_lattitude]),
#         'spn': ",".join([str(25), str(25)]),
#         'l': 'sat,skl',
#         "pt": f"{','.join([toponym_longitude, toponym_lattitude])},pm2dgl"
#     }
#     print(map_params)
#     map_api_server = 'http://static-maps.yandex.ru/1.x/'
#     response = requests.get(map_api_server, params=map_params)
#     return response


class GeoGesser(discord.Client):
    async def on_message(self, message):
        global_init('db/db1.db')
        db_sess = create_session()
        if message.author.bot:
            return
        if not message.content[0:2] == '!!':
            name = message.author.name
            try:
                user = db_sess.query(User).filter(User.name == name).first()
                id, processing = user.id, user.processing
            except Exception:
                return
            if str(processing) == '1':
                mlist = user.ids_of_countries
                mlist = mlist.split()
                country_id = mlist[0]
                try:
                    next_country_id = mlist[1]
                except IndexError:
                    country = db_sess.query(Country).filter(Country.id == country_id)
                    pairs = country.name, country.capital
                    if message.content.lower() == pairs[1].lower():
                        user.score += 1
                        db_sess.commit()
                        await score_count(user, message, db_sess)
                        await message.channel.send('Right!')
                        await message.channel.send(f'{user.name}, you win the game! Your general score is {user.score}')
                        user.processing = None
                        user.ids_of_countries = None
                        db_sess.commit()
                    else:
                        user.processing = None
                        user.ids_of_countries = None
                        db_sess.commit()
                        await message.channel.send('Wrong')
                        await message.channel.send(f'The for {user.name} game have finished')
                    return
                country_1 = db_sess.query(Country).filter(Country.id == country_id).first()
                country_2 = db_sess.query(Country).filter(Country.id == next_country_id).first()
                pairs = ((country_1.name, country_1.capital), (country_2.name, country_2.capital))
                if message.content.lower() == pairs[0][1].lower():
                    user.score += 1
                    db_sess.commit()
                    await score_count(user, message, db_sess)
                    await message.channel.send('Right!')
                    await message.channel.send(pairs[1][0])
                    mlist = ' '.join(mlist[1:])
                    user.ids_of_countries = mlist
                    db_sess.commit()
                else:
                    user.processing = None
                    user.ids_of_countries = None
                    db_sess.commit()
                    await message.channel.send('Wrong')
                    await message.channel.send(f'The game for {user.name} have finished')
            elif str(processing) == '2':
                mlist = user.ids_of_countries
                mlist = mlist.split()
                country_id = mlist[0]
                try:
                    next_country_id = mlist[1]
                except IndexError:
                    country = db_sess.query(Country).filter(Country.id == country_id)
                    pairs = country.name, country.capital
                    if message.content.lower() == pairs[0].lower():
                        user.score += 1
                        db_sess.commit()
                        await score_count(user, message, db_sess)
                        await message.channel.send('Right!')
                        await message.channel.send(f'{user.name}, you win the game! Your general score is {user.score}')
                        user.processing = None
                        user.ids_of_countries = None
                        db_sess.commit()

                    else:
                        user.processing = None
                        user.ids_of_countries = None
                        db_sess.commit()
                        await message.channel.send('Wrong')
                        await message.channel.send(f'The game for {user.name} have finished')
                country_1 = db_sess.query(Country).filter(Country.id == country_id).first()
                country_2 = db_sess.query(Country).filter(Country.id == next_country_id).first()
                pairs = ((country_1.name, country_1.capital), (country_2.name, country_2.capital))
                if message.content.lower() == pairs[0][0].lower():
                    user.score += 1
                    db_sess.commit()
                    await score_count(user, message, db_sess)
                    await message.channel.send('Right!')
                    await message.channel.send(pairs[1][1])
                    mlist = ' '.join(mlist[1:])
                    user.ids_of_countries = mlist
                    db_sess.commit()
                else:
                    user.processing = None
                    user.ids_of_countries = None
                    db_sess.commit()
                    await message.channel.send('Wrong')
                    await message.channel.send(f'The game for {user.name} have finished')
            elif str(processing) == '3':
                mlist = user.ids_of_countries
                mlist = mlist.split()
                country_id = mlist[0]
                try:
                    next_country_id = mlist[1]
                except IndexError:
                    country = db_sess.query(Country).filter(Country.id == country_id)
                    pairs = country.name, country.flag
                    if message.content.lower() == pairs[0].lower():
                        user.score += 1
                        db_sess.commit()
                        await score_count(user, message, db_sess)
                        await message.channel.send('Right!')
                        await message.channel.send(f'{user.name}, you win the game! Your general score is {user.score}')
                        user.processing = None
                        user.ids_of_countries = None
                        db_sess.commit()
                    else:
                        user.processing = None
                        user.ids_of_countries = None
                        db_sess.commit()
                        await message.channel.send('Wrong')
                        await message.channel.send(f'The game for {user.name} have finished')
                country_1 = db_sess.query(Country).filter(Country.id == country_id).first()
                country_2 = db_sess.query(Country).filter(Country.id == next_country_id).first()
                pairs = ((country_1.name, country_1.flag), (country_2.name, country_2.flag))
                if message.content.lower() == pairs[0][0].lower():
                    user.score += 1
                    db_sess.commit()
                    await score_count(user, message, db_sess)
                    await message.channel.send('Right!')
                    await message.channel.send(pairs[1][1])
                    mlist = ' '.join(mlist[1:])
                    user.ids_of_countries = mlist
                    db_sess.commit()
                else:
                    user.processing = None
                    user.ids_of_countries = None
                    db_sess.commit()
                    await message.channel.send('Wrong')
                    await message.channel.send(f'The game for {user.name} have finished')
            elif str(processing) == '4':
                mlist = user.ids_of_countries
                mlist = mlist.split(' .')
                if message.content.lower() in mlist:
                    mlist.remove(message.content.lower())
                    user.score += 1
                    await score_count(user, message, db_sess)
                    db_sess.commit()
                    if len(mlist) == 1:
                        await message.channel.send(f'{user.name}, you named all of countries')
                        count = user.score - int(mlist[-1][:-7])
                        time = tiime.time() - user.nick
                        await message.channel.send(f'Your score is {count} in {round(time)} seconds')
                        user.processing = None
                        user.ids_of_countries = None
                        db_sess.commit()
                    mlist = ' .'.join(mlist)
                    user.ids_of_countries = mlist
                    db_sess.commit()

                else:
                    await message.channel.send(f'Oops! You named a wrong country. Game for {user.name} finished')
                    count = user.score - int(mlist[-1][:-7])
                    time = tiime.time() - user.nick
                    await message.channel.send(f'You wrote {count} countries in {round(time)} seconds')
                    user.processing = None
                    user.ids_of_countries = None
                    db_sess.commit()
            elif str(processing) == '6':
                countries = db_sess.query(Country).all()
                mlist1 = [elem.name.lower() for elem in countries]
                mlist2 = [elem.name for elem in countries]
                if message.content.lower() in mlist1:
                    cntr = db_sess.query(Country).filter(Country.name == mlist2[mlist1.index(message.content.lower())]).first()
                    await message.channel.send(f'Name: {cntr.name}        Capital: {cntr.capital}        Flag:')
                    await message.channel.send(cntr.flag)
                    user.processing = None
                else:
                    await message.channel.send("Country doesn't exist")
        else:
            if message.content == '!!game 1':
                name = message.author.name
                try:
                    user = db_sess.query(User).filter(User.name == name).first()
                    id = user.id
                except Exception:
                    user = User()
                    user.name = name
                    user.difficult = 1
                    user.score = 0
                    db_sess.add(user)
                    db_sess.commit()
                    id = user.id
                user.processing = 1
                countries = db_sess.query(Country).filter(Country.difficult <= user.difficult).all()
                mlist = [str(elem.id) for elem in countries]
                shuffle(mlist)
                country_id = mlist[0]
                mlist = ' '.join(mlist)
                country = db_sess.query(Country).filter(Country.id == country_id).first().name
                await message.channel.send(country)
                user.ids_of_countries = mlist
                db_sess.commit()
            elif message.content == '!!game 2':
                name = message.author.name
                try:
                    user = db_sess.query(User).filter(User.name == name).first()
                    id = user.id
                except Exception:
                    user = User()
                    user.name = name
                    user.difficult = 1
                    user.score = 0
                    db_sess.add(user)
                    db_sess.commit()
                    id = user.id
                user.processing = 2
                countries = db_sess.query(Country).filter(Country.difficult <= user.difficult).all()
                mlist = [str(elem.id) for elem in countries]
                shuffle(mlist)
                capital_id = mlist[0]
                mlist = ' '.join(mlist)
                capital = db_sess.query(Country).filter(Country.id == capital_id).first().capital
                await message.channel.send(capital)
                user.ids_of_countries = mlist
                db_sess.commit()
            elif message.content == '!!game 3':
                name = message.author.name
                try:
                    user = db_sess.query(User).filter(User.name == name).first()
                    id = user.id
                except Exception:
                    user = User()
                    user.name = name
                    user.difficult = 1
                    user.score = 0
                    db_sess.add(user)
                    db_sess.commit()
                    id = user.id
                user.processing = 3
                countries = db_sess.query(Country).filter(Country.difficult <= user.difficult).all()
                mlist = [str(elem.id) for elem in countries]
                shuffle(mlist)
                country_id = mlist[0]
                mlist = ' '.join(mlist)
                country = db_sess.query(Country).filter(Country.id == country_id).first()
                await message.channel.send(country.flag)
                user.ids_of_countries = mlist
                db_sess.commit()
            elif message.content == '!!game 4':
                name = message.author.name
                try:
                    user = db_sess.query(User).filter(User.name == name).first()
                    id = user.id
                except Exception:
                    user = User()
                    user.name = name
                    user.difficult = 1
                    user.score = 0
                    db_sess.add(user)
                    db_sess.commit()
                    id = user.id
                user.processing = 4
                user.nick = tiime.time()
                await message.channel.send('Game is started now! Write a country')
                countries = db_sess.query(Country).all()
                mlist = [elem.name.lower() for elem in countries]
                mlist.append(f'{user.score}.......')
                mlist = ' .'.join(mlist)
                user.ids_of_countries = mlist
                db_sess.commit()
            elif message.content == '!!stop':
                name = message.author.name
                try:
                    user = db_sess.query(User).filter(User.name == name).first()
                    id, processing = user.id, user.processing
                except Exception:
                    await message.channel.send("Game for you isn't started")
                if not id or not processing:
                    await message.channel.send("Game for you isn't started")
                else:
                    user.processing = None
                    user.ids_of_countries = None
                    db_sess.commit()
                    await message.channel.send("Game for you have finished")
            elif message.content == '!!score':
                name = message.author.name
                try:
                    user = db_sess.query(User).filter(User.name == name).first()
                    id = user.id
                    await message.channel.send(f'Your score is {user.score}')
                except Exception:
                    await message.channel.send('You are not in my database')
            elif message.content == '!!info':
                name = message.author.name
                try:
                    user = db_sess.query(User).filter(User.name == name).first()
                    id = user.id
                except Exception:
                    user = User()
                    user.name = name
                    user.difficult = 1
                    user.score = 0
                    db_sess.add(user)
                    db_sess.commit()
                    id = user.id
                user.processing = 6
                db_sess.commit()
                await message.channel.send('Which country do you want to know about?')
            elif message.content == '!!help':
                await message.channel.send("""I'm a bot for geographical games
All of my commands start with '!!'
List of commands:
help           shows this message
game 1       starts a game (gessing capital by the name of country)
game 2       starts a game (gessing country by the name of capital)
game 3       starts a game (gessing country by the picture of flag)
game 4       starts a game (time texting countries without hints)
stop         finish current game
score        shows your current score
info             shows info about country what you want""")
            else:
                await message.channel.send("Wrong command")


client = GeoGesser()
client.run(TOKEN)
