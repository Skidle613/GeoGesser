import discord
from random import shuffle
from key import TOKEN
from data.db_session import global_init, create_session
from data.user import User
from data.country import Country
from random import randint


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
                    if message.content.lower() == pairs[0][1].lower():
                        user.score += 1
                        db_sess.commit()

                        await message.channel.send('Right!')
                        await message.channel.send(f'You win the game! Your general score is {user.score}')
                        user.processing = None
                        user.ids_of_countries = None
                        db_sess.commit()
                    else:
                        user.processing = None
                        user.ids_of_countries = None
                        db_sess.commit()
                        await message.channel.send('Wrong')
                        await message.channel.send('The game have finished')
                    return
                country_1 = db_sess.query(Country).filter(Country.id == country_id).first()
                country_2 = db_sess.query(Country).filter(Country.id == next_country_id).first()
                pairs = ((country_1.name, country_1.capital), (country_2.name, country_2.capital))
                if message.content.lower() == pairs[0][1].lower():
                    user.score += 1
                    db_sess.commit()
                    if user.score == 100:
                        roles = message.author.guild.roles
                        if 'Любитель географии' not in [elem.name for elem in roles]:
                            await message.author.guild.create_role(name='Любитель географии', colour=(discord.Colour.from_rgb(randint(1, 255), randint(1, 255), randint(1, 255))))
                        roles = message.author.guild.roles
                        role_id = [elem.id for elem in roles if elem.name == 'Любитель географии'][0]
                        await message.author.add_roles(discord.Object(role_id))
                        user.difficult = 2
                    if user.score == 2000:
                        roles = message.author.guild.roles
                        if 'Знаток географии' not in [elem.name for elem in roles]:
                            await message.author.guild.create_role(name='Знаток географии', colour=(discord.Colour.from_rgb(randint(1, 255), randint(1, 255), randint(1, 255))))
                        roles = message.author.guild.roles
                        role_id = [elem.id for elem in roles if elem.name == 'Знаток географии'][0]
                        await message.author.add_roles([role_id])
                        user.difficult = 3
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
                    await message.channel.send('The game have finished')
            elif str(processing) == '2':
                mlist = user.ids_of_countries
                mlist = mlist.split()
                country_id = mlist[0]
                try:
                    next_country_id = mlist[1]
                except IndexError:
                    country = db_sess.query(Country).filter(Country.id == country_id)
                    pairs = country.name, country.capital
                    if message.content.lower() == pairs[0][1].lower():
                        user.score += 1
                        db_sess.commit()
                        await message.channel.send('Right!')
                        await message.channel.send(f'You win the game! Your general score is {user.score}')
                        user.processing = None
                        user.ids_of_countries = None
                        db_sess.commit()

                    else:
                        user.processing = None
                        user.ids_of_countries = None
                        db_sess.commit()
                        await message.channel.send('Wrong')
                        await message.channel.send('The game have finished')
                country_1 = db_sess.query(Country).filter(Country.id == country_id).first()
                country_2 = db_sess.query(Country).filter(Country.id == next_country_id).first()
                pairs = ((country_1.name, country_1.capital), (country_2.name, country_2.capital))
                if message.content.lower() == pairs[0][0].lower():
                    user.score += 1
                    db_sess.commit()
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
                    await message.channel.send('The game have finished')
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
                pass
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
            elif message.content == '!!help':
                await message.channel.send("""I'm a bot for geographical games
All of my commands start with '!!'
List of commands:
help           shows this message
game 1       starts a game (gessing capital by the name of country)
game 2       starts a game (gessing country by the name of capital)
game 3       starts a game (gessing country by the picture of flag)
game 4       starts a game (gessing country by the picture of country)
game 5       starts a game (time texting countries without hints)
stop         finish current game
clear           delete messages about previous game
set_roles   set roles for certain score
info             shows info about country what you want""")
            else:
                await message.channel.send("Wrong command")


client = GeoGesser()
client.run(TOKEN)
