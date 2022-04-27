giving_roles = [(10, 'Новичок в географии'), (50, 'Начинающий географ'), (100, 'Любитель географии'), (200, 'Прошаренный географ'), (500, 'Знаток географии'), (1000, 'Настоящий мастер в географии'), (1500, 'Гуру-географ')]


def score_count(user, message):
    global db_sess
    score = user.score
    roles = message.author.guild.roles
    for elem in giving_roles:
        if score == elem[0]:
            if elem[1] not in [role.name for role in roles]:
                message.author.guild.create_role(elem[1], color=discord.Color.from_rgb(randrange(256), randrange(256), randrange(256)))
            roles = message.author.guild.roles
            role_id = [role.id for role in roles if role.name == elem[1]]
            message.author.give_roles(discord.Object(role_id))
            if elem[0] != 10:
                role_for_delete = get(message.author.guild.roles, name=giving_roles[giving_roles.index(elem) - 1][1])
                message.author.remove_roles(role_for_delete)
            if elem[0] == 100:
                user.difficult = 2
                db_sess.commit()
            elif elem[0] == 500:
                user.difficult = 3
                db_sess.commit()
                
            
