import discord as ds                                # pip install discord.py
from discord.ext import commands
from VT_bot_config import settings
import time
from PIL import Image, ImageDraw, ImageFont         # pip install Pillow
import textwrap, datetime as dt, requests, os
from io import BytesIO
import codecs
import os

folders = ['Бич', 'Вкидончики', 'Время', 'Гей', 'Демотивы', 'Класс', 'Мда', 'Муты', 'Насилие', 'Ор', 'Панчи', 'Песка', 'Ржака', 'Сори', 'Стоп', 'Ум', 'Ум ваче сей']
os.mkdir('Results/') if not os.path.isdir("Results/") else print()
os.mkdir('User_image/') if not os.path.isdir("User_image/") else print()
os.mkdir('Temp/') if not os.path.isdir("Temp/") else print()
for folder_name in folders:
    os.mkdir(f'Results/{folder_name}/') if not os.path.isdir(f'Results/{folder_name}/') else print()

save_path = list(__file__)
save_path.reverse()
save_path = ''.join(save_path[ -1 : save_path.index('\\') : -1]).replace('\\', '/') + '/'
print(save_path)


bot = commands.Bot(command_prefix=(settings['prefix']))
client = ds.Client()

def log_write(text):
    os.mkdir('Mat/') if not os.path.isdir("Mat/") else print()
    log = open(save_path + 'Mat/log.txt', 'a')
    log.write(f"{text}\n---------------\n")
    log.close()


def resize(inp_img_path, width=1069, height=520):
    img = Image.open(inp_img_path)
    resized_img = img.resize((width, height), Image.ANTIALIAS)
    img.close()
    return resized_img


def turn_off(ctx):
    time = dt.datetime.now()
    author = ctx.message.author
    log_write(f"{author} turned off bot at {time}")
    exit('Bot stopped')


def put_meme(save_fold, MFP, meme_name, len_x, len_y, ctx, pos_x=0, pos_y=0):
    if MFP == ' ':
        MFP = save_path + 'Mat/Error.png'
    attachment = ctx.message.attachments[0].url
    author = ctx.message.author
    filename = attachment.split('/')[(-1)]
    r = requests.get(attachment, allow_redirects=True)
    main_path = save_path
    res_mid = os.path.join('Results/', save_fold)
    FFP_path = os.path.join(main_path, 'User_image/')
    WFP_path = os.path.join(main_path, res_mid)
    FFP = os.path.join(FFP_path, filename)
    num_add = os.path.join(main_path, 'Mat/num_.txt')
    num_file = open(num_add, 'r')
    line = num_file.readlines()[0]
    num = int(line)
    WFP_c = WFP_path + str(num) + '.png'
    num += 1
    num_file.close()
    with open(num_add, 'wb'):
        pass
    num_file = open(num_add, 'w')
    num_file.write(str(num))
    num_file.close()
    change, f_ext = os.path.splitext(FFP)
    with open(FFP, 'wb') as (img):
        img.write(r.content)
    mat = Image.open(MFP)
    temp, us_file_ext = os.path.splitext(FFP)
    us_file = Image.open(FFP)
    us_file.convert('RGB')
    us_file.save(FFP)
    mat.paste(resize(FFP, len_x, len_y), (pos_x, pos_y))
    mat.save(WFP_c, 'png')
    time = dt.datetime.now()
    log_write(f"{author} create a {meme_name} fotolup at {time}, saved in {WFP_path} as {num - 1}")
    print(f"Picture saved in {WFP_path} as {num - 1}\n")
    num_file.close()
    return (author, time, num - 1, WFP_c, WFP_path, author)


@bot.event
async def on_ready():
    time = dt.datetime.now()
    log_write(f"Bot started at {time}")
    print(f"Bot started as {bot.user.name}, V3.5\n----------------------------------------------------------------")


@bot.command(pass_context=True)
async def хэлп(ctx):
    await ctx.channel.purge(limit=1)
    mat = Image.open(save_path + 'Mat/White.png')
    draw = ImageDraw.Draw(mat)
    help_file = codecs.open((save_path + 'Mat/Помощь.txt'), 'r', encoding='UTF-8')
    help_lines = help_file.readlines()
    size = 38
    font = ImageFont.truetype((save_path + 'Mat/times-new-roman.ttf'), size=size)
    H = 50
    for lines in help_lines:
        for line in textwrap.wrap(lines, width=(size + int(size / 2) - 2)):
            draw.text((50, H), (line + '\n'), font=font, fill='black')
            H += font.getsize(line)[1]

    mat.save(save_path + 'Temp/White.png')
    mat.close()
    await ctx.send(file=(ds.File(save_path + 'Temp/White.png')))
    #os.remove(save_path + 'Temp/White.png')
    help_file.close()
    del draw
    await ctx.send("Есть пара скрытых опций. Чтобы о них узнать, обратись к kernolle\nПока это все, окда.")


@bot.command()
async def roles(ctx):
    await ctx.channel.purge(limit=1)
    roles_dict = settings['roles']
    post = roles_dict['post_id']
    roles_ = list(roles_dict.items())
    print(f"post_id = {post}, roles = {roles_}")


class memes:

    @bot.command()
    async def каеф(ctx):
        author = ctx.message.author
        await ctx.channel.purge(limit=1)
        log_write(f"{author} кайфанул {time}")
        await ctx.send(f"{author.mention} кайфует  🤙")

    @bot.command(pass_context=True)
    async def класс(ctx, *, text='крута'):
        try:
            result = put_meme('Класс/', f"{save_path}Mat/class.jpg", 'CLASS', 845, 475, ctx)
            mat = Image.open(result[3])
            draw = ImageDraw.Draw(mat)
            size = 30
            font = ImageFont.truetype(f"{save_path}Mat/times-new-roman.ttf", size=size)
            W = 110
            H = 570
            for line in textwrap.wrap(text, width=(int(size - size / 3))):
                draw.text((110, H), line, font=font, fill='black')
                H += font.getsize(line)[1]

            del draw
            mat.save(result[3])
            await ctx.channel.purge(limit=1)
            await ctx.send('Фоталуп гатов')
            await ctx.send(file=(ds.File(result[3])))
        except IndexError:
            await ctx.channel.purge(limit=1)
            await ctx.send('Родной, мне нужна ПИКЧА, а не пустота')

    @bot.command(pass_context=False)
    async def вкид(ctx):
        try:
            result = put_meme('Вкидончики/', f"{save_path}Mat/vkid.jpg", 'VKID', 1071, 519, ctx)
            await ctx.channel.purge(limit=1)
            await ctx.send('Фоталуп гатов')
            await ctx.send(file=(ds.File(result[3])))
        except IndexError:
            await ctx.channel.purge(limit=1)
            await ctx.send('Родной, мне нужна ПИКЧА, а не пустота')

    @bot.command(pass_context=True)
    async def мотив(ctx, *, text=' '):
        try:
            MFP = f"{save_path}Mat/motivate.jpg"
            result = put_meme('Демотивы/', MFP, 'DEMOTIVATOR', 478, 468, ctx, 41, 41)
            WFP_c = result[3]
            mat = Image.open(WFP_c)
            draw = ImageDraw.Draw(mat)
            W, H = mat.size
            w, h = draw.textsize(text.encode('UTF-8', 'ignore'))
            size = 30
            font = ImageFont.truetype(f"{save_path}Mat/times-new-roman.ttf", size=size)
            W = int((W - w) / 3)
            H = 520
            width = 26
            for line in textwrap.wrap(text, width=width):
                draw.text((W, H), line, font=font, fill='white', align='center')
                H += font.getsize(line)[1]
                size = size - 5
                W += W / 2

            del draw
            mat.save(WFP_c)
            await ctx.channel.purge(limit=1)
            await ctx.send('Фоталуп гатов')
            await ctx.send(file=(ds.File(WFP_c)))
        except IndexError:
            await ctx.channel.purge(limit=1)
            await ctx.send('Родной, мне нужна ПИКЧА, а не пустота')

    @bot.command(pass_context=True)
    async def пс(ctx, *, text='эта хуила?'):
        try:
            MFP = f"{save_path}Mat/ps3.jpg"
            result = put_meme('Песка/', MFP, 'PS3', 290, 174, ctx, 48, 50)
            await ctx.channel.purge(limit=1)
            WFP_c = result[3]
            mat = Image.open(WFP_c)
            draw = ImageDraw.Draw(mat)
            font = ImageFont.truetype(f"{save_path}Mat/times-new-roman.ttf", size=14)
            draw.text((55, 7), (str(result[5])), font=font, fill='white', align='center')
            draw.text((120, 26), text, font=font, fill='white', align='center')
            del draw
            mat.save(WFP_c, 'png')
            await ctx.channel.purge(limit=1)
            await ctx.send('Фоталуп гатов')
            await ctx.send(file=(ds.File(WFP_c)))
        except IndexError:
            await ctx.channel.purge(limit=1)
            await ctx.send('Родной, мне нужна ПИКЧА, а не пустота')

    @bot.command(pass_context=True)
    async def мут(ctx, *, text=' '):
        try:
            result = put_meme('Муты/', f"{save_path}Mat/mute.jpg", 'MUT', 1519, 666, ctx)
            await ctx.channel.purge(limit=1)
            await ctx.send('Фоталуп гатов')
            await ctx.send(file=(ds.File(result[3])))
        except IndexError:
            await ctx.channel.purge(limit=1)
            await ctx.send('Родной, мне нужна ПИКЧА, а не пустота')

    @bot.command(pass_context=True)
    async def ум(ctx, *, text=' '):
        try:
            result = put_meme('Ум/', f"{save_path}Mat/smart.jpg", 'BRAIN', 1080, 508, ctx)
            await ctx.channel.purge(limit=1)
            await ctx.send('Фоталуп гатов')
            await ctx.send(file=(ds.File(result[3])))
        except IndexError:
            await ctx.channel.purge(limit=1)
            await ctx.send('Родной, мне нужна ПИКЧА, а не пустота')

    @bot.command(pass_context=True)
    async def панч(ctx, *, text=' '):
        try:
            result = put_meme('Панчи/', f"{save_path}Mat/Punch.jpg", 'PUNCH', 488, 286, ctx)
            await ctx.channel.purge(limit=1)
            await ctx.send('Фоталуп гатов')
            await ctx.send(file=(ds.File(result[3])))
        except IndexError:
            await ctx.channel.purge(limit=1)
            await ctx.send('Родной, мне нужна ПИКЧА, а не пустота')

    @bot.command(pass_context=True)
    async def мда(ctx, *, text=' '):
        try:
            result = put_meme('Мда/', f"{save_path}Mat/mda.jpg", 'MDA', 606, 176, ctx, 75, 45)
            await ctx.channel.purge(limit=1)
            await ctx.send('Фоталуп гатов')
            await ctx.send(file=(ds.File(result[3])))
        except IndexError:
            await ctx.channel.purge(limit=1)
            await ctx.send('Родной, мне нужна ПИКЧА, а не пустота')

    @bot.command(pass_context=True)
    async def время(ctx, *, text=' '):
        try:
            result = put_meme('Время/', f"{save_path}Mat/Fjtzth6lMTs.jpg", 'TIME', 606, 454, ctx, 75, 45)
            await ctx.channel.purge(limit=1)
            await ctx.send('Фоталуп гатов')
            await ctx.send(file=(ds.File(result[3])))
        except IndexError:
            await ctx.channel.purge(limit=1)
            await ctx.send('Родной, мне нужна ПИКЧА, а не пустота')

    @bot.command()
    async def бич(ctx):
        try:
            result = put_meme('Бич/', f"{save_path}Mat/beatch.jpg", 'TUPAK', 778, 797, ctx, 54, 39)
            await ctx.channel.purge(limit=1)
            await ctx.send('Фоталуп гатов')
            await ctx.send(file=(ds.File(result[3])))
        except IndexError:
            await ctx.channel.purge(limit=1)
            await ctx.send('Родной, мне нужна ПИКЧА, а не пустота')

    @bot.command()
    async def сей(ctx):
        try:
            result = put_meme('Ум ваче сей/', f"{save_path}Mat/vache_sey.jpg", 'UMVACHESEY', 800, 490, ctx)
            await ctx.channel.purge(limit=1)
            await ctx.send('Фоталуп гатов')
            await ctx.send(file=(ds.File(result[3])))
        except IndexError:
            await ctx.channel.purge(limit=1)
            await ctx.send('Родной, мне нужна ПИКЧА, а не пустота')

    @bot.command()
    async def ор(ctx):
        try:
            result = put_meme('Ор/', f"{save_path}Mat/Ор.png", 'SCREAM', 607, 567, ctx, 68, 78)
            await ctx.channel.purge(limit=1)
            await ctx.send('Фоталуп гатов')
            await ctx.send(file=(ds.File(result[3])))
        except IndexError:
            await ctx.channel.purge(limit=1)
            await ctx.send('Родной, мне нужна ПИКЧА, а не пустота')

    @bot.command()
    async def ржака(ctx):
        try:
            result = put_meme('Ржака/', f"{save_path}Mat/laugh.jpg", 'LMAO', 568, 435, ctx)
            await ctx.channel.purge(limit=1)
            await ctx.send('Фоталуп гатов')
            await ctx.send(file=(ds.File(result[3])))
        except IndexError:
            await ctx.channel.purge(limit=1)
            await ctx.send('Родной, мне нужна ПИКЧА, а не пустота')

    @bot.command()
    async def гей(ctx):
        try:
            result = put_meme('Гей/', f"{save_path}Mat/gay.jpg", 'GAY', 720, 360, ctx)
            await ctx.channel.purge(limit=1)
            await ctx.send('Фоталуп гатов')
            await ctx.send(file=(ds.File(result[3])))
        except IndexError:
            await ctx.channel.purge(limit=1)
            await ctx.send('Родной, мне нужна ПИКЧА, а не пустота')

    @bot.command()
    async def стоп(ctx):
        try:
            result = put_meme('Стоп/', f"{save_path}Mat/stop.jpg", 'STOP', 604, 258, ctx)
            await ctx.channel.purge(limit=1)
            await ctx.send('Фоталуп гатов')
            await ctx.send(file=(ds.File(result[3])))
        except IndexError:
            await ctx.channel.purge(limit=1)
            await ctx.send('Родной, мне нужна ПИКЧА, а не пустота')

    @bot.command()
    async def насилие(ctx):
        try:
            result = put_meme('Насилие/', f"{save_path}Mat/fuck.jpg", 'FUCK', 750, 276, ctx)
            await ctx.channel.purge(limit=1)
            await ctx.send('Фоталуп гатов')
            await ctx.send(file=(ds.File(result[3])))
        except IndexError:
            await ctx.channel.purge(limit=1)
            await ctx.send('Родной, мне нужна ПИКЧА, а не пустота')

    @bot.command()
    async def сори(ctx):
        try:
            result = put_meme('Сори/', f"{save_path}Mat/sorry.jpg", 'SORRY', 1920, 542, ctx)
            await ctx.channel.purge(limit=1)
            await ctx.send('Фоталуп гатов')
            await ctx.send(file=(ds.File(result[3])))
        except IndexError:
            await ctx.channel.purge(limit=1)
            await ctx.send('Родной, мне нужна ПИКЧА, а не пустота')

    @bot.command()
    async def test(ctx):
        attachment = ctx.message.attachments[0].url
        await ctx.send(attachment)

    @bot.command()
    async def cycle(ctx):
        await ctx.channel.purge(limit=1)
        i = 0
        while i != 101:
            time.sleep(1)
            i += 1
            await ctx.send('-вкид')


@bot.command()
async def чисти(ctx, all='', amount=10):
    cha = ctx.message.channel
    author = ctx.message.author
    if all == 'все' or all == 'всё':
        amount = 1
        history = await cha.history(limit=9999).flatten()
        for i in history:
            amount += 1

    await ctx.channel.purge(limit=amount)
    time = dt.datetime.now()
    log_write(f"{amount} messages been deleted from {cha} by {author} at {time}")
    print(f"{amount} messages been deleted from {cha} by {author} at {time}")
    await ctx.send(f"Говно в количестве {amount} сообщений вычищено, {author.mention}", delete_after=5)


class Off:

    @bot.command()
    async def оф(ctx):
        await ctx.channel.purge(limit=1)
        await ctx.send('Покеда, ушлепки')
        turn_off(ctx)

    @bot.command()
    async def съеби(ctx):
        await ctx.channel.purge(limit=1)
        await ctx.send('Покеда, ушлепки')
        turn_off(ctx)

    @bot.command()
    async def exit(ctx):
        await ctx.channel.purge(limit=1)
        await ctx.send('Покеда, ушлепки')
        turn_off(ctx)


bot.run(settings['token'])
