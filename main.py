import os

from discord import Game
from dotenv import load_dotenv
from os.path import join, dirname
from discord.ext.commands import Bot
from database import Database

PREFIX = '!'

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

TOKEN = os.environ.get('TOKEN')
PRODUCTION_ENV = os.environ.get("ENVIRONMENT") != "DEV"
UNAME = os.environ.get("USERNAME")
PWD = os.environ.get("PASSWORD")
DB_HOST = os.environ.get("DB_HOST")
DB_NAME = os.environ.get("DB_NAME")
listen_chan = os.environ.get("PROD_CHAN") if PRODUCTION_ENV else os.environ.get("DEV_CHAN")
error_message = "that's an invalid query. Try !resume help to see commands. PSA: please anonymize your resumes."

bot = Bot(command_prefix=PREFIX)
db = Database(DB_NAME, uname=UNAME, pwd=PWD, host=DB_HOST)
db.start_connection()


# Bot Events
@bot.event
async def on_ready():
    await bot.change_presence(game=Game(name="Something CS Related"))
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("------")

@bot.event
async def on_message(msg):
    global listen_chan
    if msg.channel.name == listen_chan:
        await bot.process_commands(msg)

# Bot commands
@bot.group(pass_context=True)
async def resume(ctx):
    if ctx.invoked_subcommand is None:
        await bot.send_message(ctx.message.channel, error_message)

@resume.group(name='submit', aliases=['add'], pass_context=True)
async def submit(ctx, *args):
    global db
    if len(args) != 1:
        await bot.send_message(ctx.message.channel, error_message)
        return
    if db.push_resume(ctx.message.author.id, args[0]).is_success:
        await bot.send_message(
            ctx.message.channel,
            "successfully added you to the resume queue.\n" +
            "PSA: please anonymize your resumes. You can replace your resume and keep your spot with !resume replace.")
    else:
        await bot.send_message(ctx.message.channel, "you already have a resume in the queue. Try !resume replace [resume].")
    
@resume.group(name='delete', aliases=['remove'], pass_context=True)
async def remove(ctx, *args):
    global db
    if len(args) != 0:
        await bot.send_message(ctx.message.channel, error_message)
        return
    if db.delete_resume(ctx.message.author.id).is_success:
        await bot.send_message(ctx.message.channel, "successfully deleted your resume.")
    else:
        await bot.send_message(ctx.message.channel, "you don't have a resume in the queue.")

@resume.group(name='replace', pass_context=True)
async def replace(ctx, *args):
    global db
    if len(args) != 1:
        await bot.send_message(ctx.message.channel, error_message)
        return
    if db.replace_resume(ctx.message.author.id, args[0]).is_success:
        await bot.send_message(ctx.message.channel, "successfully replaced your resume.")
    else:
        await bot.send_message(ctx.message.channel, "you don't have a resume in the queue.")

@resume.group(name='poll', aliases=['pop'], pass_context=True)
async def poll(ctx, *args):
    global db
    if len(args) != 0:
        await bot.send_message(ctx.message.channel, error_message)
        return
    query_result = db.pop_resume()
    if query_result.is_success:
        (user_id, resume) = query_result.data
        user = await bot.get_user_info(user_id)
        await bot.send_message(ctx.message.channel, f"resume by {user.mention}: <{resume}>")
    else:
        await bot.send_message(ctx.message.channel, "there are no resumes currently in the queue.")

@resume.group(name='peek', pass_context=True)
async def peek(ctx, *args):
    global db
    if len(args) != 0:
        await bot.send_message(ctx.message.channel, error_message)
        return
    result = db.show_resumes(1)
    if result.is_success and len(result.data):
        msg_content = ["resumes currently in the queue:"]
        for (user_id, resume) in result.data:
            user = await bot.get_user_info(user_id)
            msg_content.append(f"{user.mention}: <{resume}>")
        await bot.send_message(ctx.message.author, "\n".join(msg_content))
    else:
        await bot.send_message(ctx.message.channel, "there are no resumes currently in the queue.")

@resume.group(name='show', pass_context=True)
async def show(ctx, *args):
    global db
    if len(args) != 1 and len(args) != 0:
        await bot.send_message(ctx.message.channel, error_message)
        return
    if len(args) == 0:
        result = db.show_resumes(3)
    elif args[0] == "all":
        result = db.show_resumes()
    else:
        try:
            nb_resumes = int(args[0])
        except:
            await bot.send_message(ctx.message.channel, error_message)
            return
        if nb_resumes == 0:
            await bot.send_message(ctx.message.channel, "you really want zero resumes? Try again, kiddo.")
            return
        result = db.show_resumes(nb_resumes)
    if result.is_success:
        msg_content = ["resumes currently in the queue:"]
        for (user_id, resume) in result.data:
            user = await bot.get_user_info(user_id)
            msg_content.append(f"{user.mention}: <{resume}>")
        await bot.send_message(ctx.message.author, "\n".join(msg_content))
    else:
        await bot.send_message(ctx.message.channel, "there are no resumes currently in the queue.")

@resume.group(name='help', pass_context=True)
async def help(ctx):
    await bot.send_message(
        ctx.message.channel,
        'PSA: please anonymize your resumes.\n' +
        'Use "!resume submit [url to resume]" to add a resume.\n' +
        'Use "!resume delete" to delete a resume you submitted.\n' +
        'Use "!resume replace [new url] to replace your resume, and keep your spot.\n' +
        '\n' +
        'Use "!resume poll" to get a resume to review and delete it from the queue.\n' +
        'Use "!resume show" to see the next 3 resumes currently in the queue.\n' +
        'Use "!resume show all" to see all of them.\n' +
        'Use "!resume show [number]" to see up to that many.\n' +
        'Remember to mention the user so they see the comments you made!\n' +
        'PSA: please anonymize your resumes.')


if __name__ == '__main__':
    bot.run(TOKEN)
