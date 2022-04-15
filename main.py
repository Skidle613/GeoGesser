import discord
import sqlite3
from random import shuffle

TOKEN = TOKEN


class GeoGesser(discord.Client):
    async def on_message(self, message):
        if message.author.bot:
            return
        con = sqlite3.connect('db1.db')
        cur = con.cursor()
        if not message.content[0:2] == '!!':
            name = message.author.name
            id, processing = cur.execute("""SELECT id, processing FROM users WHERE name = ?""", (name,)).fetchone()
            print(id, processing)
            if not id:
                return
            if str(processing) == '1':
                print('YES')
                mlist = cur.execute("""SELECT mlist FROM users WHERE id = ?""", (id,)).fetchone()
                mlist = mlist.split()
                country_id = mlist[0]
                try:
                    next_country_id = mlist[1]
                except IndexError:
                    pairs = cur.execute("""SELECT name, capital FROM countries WHERE id = ?""",
                                        (country_id,)).fetchall()
                    if message.content.lower().capitalize() == pairs[0][1]:
                        await message.chennel.send('Right!')
                        await message.chennel.send('You win the game! Your score is 0')
                        cur.execute("""UPDATE users SET processing = None, mlist = None WHERE id = ?""", (id,))
                        con.commit()
                    else:
                        await message.chennel.send('Wrong')
                        await message.chennel.send('The game have finished')
                pairs = cur.execute("""SELECT name, capital FROM countries WHERE id IN (?, ?)""",
                                    (country_id, next_country_id)).fetchall()
                if message.content.lower().capitalize() == pairs[0][1]:
                    await message.chennel.send('Right!')
                    await message.chennel.send(pairs[1][0])
                    mlist = ' '.join(mlist[1:])
                    cur.execute("""UPDATE users SET mlist = ? WHERE id = ?""", (mlist, id))
                    con.commit()
                else:
                    await message.chennel.send('Wrong')
                    await message.chennel.send('The game have finished')
            elif str(processing) == '2':
                mlist = cur.execute("""SELECT mlist FROM users WHERE id = ?""", (id,)).fetchone()
                mlist = mlist.split()
                country_id = mlist[0]
                try:
                    next_country_id = mlist[1]
                except IndexError:
                    pairs = cur.execute("""SELECT name, capital FROM countries WHERE id = ?""",
                                        (country_id,)).fetchall()
                    if message.content.lower().capitalize() == pairs[0][1]:
                        await message.chennel.send('Right!')
                        await message.chennel.send('You win the game! Your score is 0')
                        cur.execute("""UPDATE users SET processing = None, mlist = None WHERE id = ?""", (id,))
                        con.commit()

                    else:
                        await message.chennel.send('Wrong')
                        await message.chennel.send('The game have finished')
                pairs = cur.execute("""SELECT name, capital FROM countries WHERE id IN (?, ?)""",
                                    (country_id, next_country_id)).fetchall()
                if message.content.lower().capitalize() == pairs[0][0]:
                    await message.chennel.send('Right!')
                    await message.chennel.send(pairs[1][1])
                    mlist = ' '.join(mlist[1:])
                    cur.execute("""UPDATE users SET mlist = ? WHERE id = ?""", (mlist, id))
                    con.commit()
                else:
                    await message.chennel.send('Wrong')
                    await message.chennel.send('The game have finished')
        else:
            if message.content == '!!game 1':
                name = message.author.name
                id = cur.execute("""SELECT id FROM users WHERE name = ?""", (name,)).fetchone()
                if not id:
                    cur.execute(
                        """INSERT INTO users (name, difficult, processing, score) VALUES (?, 1, 1, 0)""",
                        (name,))
                    con.commit()
                    id = cur.execute("""SELECT id FROM users WHERE name = ?""", (name,)).fetchone()
                id = id[0]
                cur.execute("""UPDATE users SET processing = 1 WHERE id = ?""", (id,))
                mlist = cur.execute(
                    """SELECT id FROM countries WHERE difficult = (SELECT difficult FROM users WHERE id = ?)""",
                    (id,)).fetchall()
                mlist = [str(elem[0]) for elem in mlist]
                shuffle(mlist)
                country_id = mlist[0]
                mlist = ' '.join(mlist)
                country = cur.execute("""SELECT name FROM countries WHERE id = ?""", (country_id,)).fetchone()[0]
                await message.channel.send(country)
                cur.execute("""UPDATE users SET ids_of_countries = ? WHERE id = ?""", (mlist, id))
                con.commit()
            elif message.content == '!!game 2':
                name = message.author.name
                id = cur.execute("""SELECT id FROM users WHERE name = ?""", (name,)).fetchone()
                if not id:
                    cur.execute(
                        """INSERT INTO users (name, difficult, processing, score) VALUES (?, 1, 2, 0)""",
                        (name,))
                    con.commit()
                    id = cur.execute("""SELECT id FROM users WHERE name = ?""", (name,)).fetchone()
                id = id[0]
                cur.execute("""UPDATE users SET processing = 2 WHERE id = ?""", (id,))
                mlist = cur.execute(
                    """SELECT id FROM countries WHERE difficult = (SELECT difficult FROM users WHERE id = ?)""", (id,))
                mlist = [str(elem[0]) for elem in mlist]
                shuffle(mlist)
                capital_id = mlist[0]
                mlist = ' '.join(mlist)
                capital = cur.execute("""SELECT name FROM countries WHERE id = ?""", (capital_id,)).fetchone()[0]
                await message.channel.send(capital)
                cur.execute("""UPDATE users SET ids_of_countries = ? WHERE id = ?""", (mlist, id))
                con.commit()
            elif message.content == '!!stop':
                name = message.author.name
                id, processing = cur.execute("""SELECT id, processing FROM users WHERE name = ?""",
                                                (name,)).fetchone()
                if not id or not processing:
                    await message.channel.send("Game for you isn't started")
                else:
                    cur.execute("""UPDATE users SET processing = None, mlist = None WHERE id = ?""", (id,))
                    con.commit()
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
