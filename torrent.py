import os
import aiohttp
import json
import heroku3

from functools import wraps
from pyrogram import Client, filters, emoji
from pyrogram.types import Message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def getConfig(name: str):
    return os.environ[name]

int(getConfig('OWNER_ID'))
HEROKU_API_KEY = getConfig('HEROKU_API_KEY')
HEROKU_APP_NAME = getConfig('HEROKU_APP_NAME')
OWNER_ID = int(getConfig('OWNER_ID'))
BOT_TOKEN = getConfig('BOT_TOKEN')
TELEGRAM_API = getConfig('TELEGRAM_API')
TELEGRAM_HASH = getConfig('TELEGRAM_HASH')

app = Client(':memory:', api_id=int(TELEGRAM_API), api_hash=TELEGRAM_HASH, bot_token=BOT_TOKEN)


print("\nBot Started\n")


@app.on_message(filters.command(['start']))
async def start(_, message):
    await message.reply_text("Hello I'm 1337x Torrent Scraper Bot\nSend /help To Show Help Screen\nBot by @unkusr")



@app.on_message(filters.command(['help']))
async def help(_, message):
    text = f'''
    Example: /1337x titanic
    '''
    await message.reply_text(text, parse_mode="markdown")

# Using https://api.torrent.cloudns.cl/ API and https://www.jaybeetgx.cf API based on this repo https://github.com/devillD/Torrent-Searcher
# Implemented by https://github.com/jusidama18

m = None
i = 0
a = None
query = None

#====== 1337x =======#

@app.on_message(filters.command(["1337x"]))
async def find_1337x(_, message):
    global m
    global i
    global a
    global query
    if len(message.command) < 2:
        await message.reply_text("Usage: /1337x query")
        return
    query = message.text.split(None, 1)[1].replace(" ", "%20")
    m = await message.reply_text("Searching")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.torrent.cloudns.cl/api/1337x/{query}") \
                    as resp:
                a = json.loads(await resp.text())
    except:
        await m.edit("Found Nothing.")
        return
    result = (
        f"**Page - {i+1}**\n\n"
        f"➲**Name :** **[{a[i]['Name']}]({a[i]['Url']})**\n\n"
        f"➲**By** `{a[i]['UploadedBy']}` "
        f"`{a[i]['DateUploaded']}`\n\n" 
        f"➲`{a[i]['Type']}` "
        f"`{a[i]['Category']}`\n\n"
        f"➲**Language :** `{a[i]['Language']}` || "
        f"➲**Checked :** `{a[i]['LastChecked']}`\n\n"
        f"➲**Seeds :** `{a[i]['Seeders']}` **&** "
        f"➲**Leeches :** `{a[i]['Leechers']}`\n\n"
        f"➲**Magnet :** `{a[i]['Magnet']}`\n\n\n"
    )
    await m.edit(
        result,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(f"Next",
                                         callback_data="1337x_next"),
                    InlineKeyboardButton(f"{emoji.CROSS_MARK}",
                                         callback_data="delete")
                ]
            ]
        ),
        parse_mode="markdown",
    )


@app.on_callback_query(filters.regex("1337x_next"))
async def callback_query_next_1337x(_, message):
    global i
    global m
    global a
    global query
    i += 1
    result = (
        f"**Page - {i+1}**\n\n"
        f"➲**Name :** **[{a[i]['Name']}]({a[i]['Url']})**\n\n"
        f"➲**By** `{a[i]['UploadedBy']}` "
        f"`{a[i]['DateUploaded']}`\n\n" 
        f"➲`{a[i]['Type']}` "
        f"`{a[i]['Category']}`\n\n"
        f"➲**Language :** `{a[i]['Language']}` || "
        f"➲**Checked :** `{a[i]['LastChecked']}`\n\n"
        f"➲**Seeds :** `{a[i]['Seeders']}` **&** "
        f"➲**Leeches :** `{a[i]['Leechers']}`\n\n"
        f"➲**Magnet :** `{a[i]['Magnet']}`\n\n\n"
    )
    await m.edit(
        result,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(f"Prev",
                                         callback_data="1337x_previous"),
                    InlineKeyboardButton(f"{emoji.CROSS_MARK}",
                                         callback_data="delete"),
                    InlineKeyboardButton(f"Next",
                                         callback_data="1337x_next")
                    
                ]
            ]
        ),
        parse_mode="markdown",
    )


@app.on_callback_query(filters.regex("1337x_previous"))
async def callback_query_previous_1337x(_, message):
    global i
    global m
    global a
    global query
    i -= 1
    result = (
        f"**Page - {i+1}**\n\n"
        f"➲**Name :** **[{a[i]['Name']}]({a[i]['Url']})**\n\n"
        f"➲**By** `{a[i]['UploadedBy']}` "
        f"`{a[i]['DateUploaded']}`\n\n" 
        f"➲`{a[i]['Type']}` "
        f"`{a[i]['Category']}`\n\n"
        f"➲**Language :** `{a[i]['Language']}` || "
        f"➲**Checked :** `{a[i]['LastChecked']}`\n\n"
        f"➲**Seeds :** `{a[i]['Seeders']}` **&** "
        f"➲**Leeches :** `{a[i]['Leechers']}`\n\n"
        f"➲**Magnet :** `{a[i]['Magnet']}`\n\n\n"
    )
    await m.edit(
        result,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(f"Prev",
                                         callback_data="previous"),
                    InlineKeyboardButton(f"{emoji.CROSS_MARK}",
                                         callback_data="delete"),
                    InlineKeyboardButton(f"Next",
                                         callback_data="next")
                ]
            ]
        ),
        parse_mode="markdown",
    )

#====== 1337x =======#

#====== piratebay =======#

@app.on_message(filters.command(["piratebay"]))
async def find_piratebay(_, message):
    global m
    global i
    global a
    global query
    if len(message.command) < 2:
        await message.reply_text("Usage: /piratebay query")
        return
    query = message.text.split(None, 1)[1].replace(" ", "%20")
    m = await message.reply_text("Searching")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.torrent.cloudns.cl/api/piratebay/{query}") \
                    as resp:
                a = json.loads(await resp.text())
    except:
        await m.edit("Found Nothing.")
        return
    result = (
        f"**Page - {i+1}**\n\n"
        f"➲Name: {a[i]['Name']}\n"
        f"➲{a[i]['Uploader']} on "
        f"{a[i]['Date']}\n" 
        f"➲Size: {a[i]['Size']}\n"
        f"➲Leechers: {a[i]['Leechers']} || "
        f"➲Seeders: {a[i]['Seeders']}\n"
        f"➲Type: {a[i]['Category']}\n\n"
        f"➲Magnet: `{a[i]['Magnet']}`\n\n\n"
    )
    await m.edit(
        result,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(f"Next",
                                         callback_data="piratebay_next"),
                    InlineKeyboardButton(f"{emoji.CROSS_MARK}",
                                         callback_data="delete")
                ]
            ]
        ),
        parse_mode="markdown",
    )


@app.on_callback_query(filters.regex("piratebay_next"))
async def callback_query_next_piratebay(_, message):
    global i
    global m
    global a
    global query
    i += 1
    result = (
        f"**Page - {i+1}**\n\n"
        f"➲Name: {a[i]['Name']}\n"
        f"➲{a[i]['Uploader']} on "
        f"{a[i]['Date']}\n" 
        f"➲Size: {a[i]['Size']}\n"
        f"➲Leechers: {a[i]['Leechers']} || "
        f"➲Seeders: {a[i]['Seeders']}\n"
        f"➲Type: {a[i]['Category']}\n\n"
        f"➲Magnet: `{a[i]['Magnet']}`\n\n\n"
    )
    await m.edit(
        result,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(f"Prev",
                                         callback_data="piratebay_previous"),
                    InlineKeyboardButton(f"{emoji.CROSS_MARK}",
                                         callback_data="delete"),
                    InlineKeyboardButton(f"Next",
                                         callback_data="piratebay_next")
                    
                ]
            ]
        ),
        parse_mode="markdown",
    )


@app.on_callback_query(filters.regex("piratebay_previous"))
async def callback_query_previous_piratebay(_, message):
    global i
    global m
    global a
    global query
    i -= 1
    result = (
        f"**Page - {i+1}**\n\n"
        f"➲Name: {a[i]['Name']}\n"
        f"➲{a[i]['Uploader']} on "
        f"{a[i]['Date']}\n" 
        f"➲Size: {a[i]['Size']}\n"
        f"➲Leechers: {a[i]['Leechers']} || "
        f"➲Seeders: {a[i]['Seeders']}\n"
        f"➲Type: {a[i]['Category']}\n\n"
        f"➲Magnet: `{a[i]['Magnet']}`\n\n\n"
    )
    await m.edit(
        result,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(f"Prev",
                                         callback_data="piratebay_previous"),
                    InlineKeyboardButton(f"{emoji.CROSS_MARK}",
                                         callback_data="delete"),
                    InlineKeyboardButton(f"Next",
                                         callback_data="piratebay_next")
                ]
            ]
        ),
        parse_mode="markdown",
    )

#====== piratebay =======#

#====== yts =======#

@app.on_message(filters.command(["yts"]))
async def find_yts(_, message):
    global m
    global i
    global a
    global query
    if len(message.command) < 2:
        await message.reply_text("Usage: /yts query")
        return
    query = message.text.split(None, 1)[1].replace(" ", "%20")
    m = await message.reply_text("Searching")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.torrent.cloudns.cl/api/yts/{query}") \
                    as resp:
                a = json.loads(await resp.text())
    except:
        await m.edit("Found Nothing.")
        return
    result = (
        f"**Page - {i+1}**\n\n"
        f"➲Name: [{a[i]['Name']}]({a[i]['Url']})\n"
        f"➲Released on: {a[i]['ReleasedDate']}\n"
        f"➲Genre: {a[i]['Genre']}\n" 
        f"➲Rating: {a[i]['Rating']}\n"
        f"➲Likes: {a[i]['Likes']}\n"
        f"➲Duration: {a[i]['Runtime']}\n"
        f"➲Language: {a[i]['Language']}\n\n"
        f"➲First Link `{a[i]['Dwnload1']}`\n\n"
        f"➲Second Link: `{a[i]['Download2']}`\n\n\n"
    )
    await m.edit(
        result,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(f"Next",
                                         callback_data="yts_next"),
                    InlineKeyboardButton(f"{emoji.CROSS_MARK}",
                                         callback_data="delete")
                ]
            ]
        ),
        parse_mode="markdown", disable_web_page_preview=True,
    )


@app.on_callback_query(filters.regex("yts_next"))
async def callback_query_next_yts(_, message):
    global i
    global m
    global a
    global query
    i += 1
    result = (
        f"**Page - {i+1}**\n\n"
        f"➲Name: [{a[i]['Name']}]({a[i]['Url']})\n"
        f"➲Released on: {a[i]['ReleasedDate']}\n"
        f"➲Genre: {a[i]['Genre']}\n" 
        f"➲Rating: {a[i]['Rating']}\n"
        f"➲Likes: {a[i]['Likes']}\n"
        f"➲Duration: {a[i]['Runtime']}\n"
        f"➲Language: {a[i]['Language']}\n\n"
        f"➲First Link: `{a[i]['Dwnload1']}`\n\n"
        f"➲Second Link: `{a[i]['Download2']}`\n\n\n"
    )
    await m.edit(
        result,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(f"Prev",
                                         callback_data="yts_previous"),
                    InlineKeyboardButton(f"{emoji.CROSS_MARK}",
                                         callback_data="delete"),
                    InlineKeyboardButton(f"Next",
                                         callback_data="yts_next")
                    
                ]
            ]
        ),
        parse_mode="markdown", disable_web_page_preview=True,
    )


@app.on_callback_query(filters.regex("yts_previous"))
async def callback_query_previous_yts(_, message):
    global i
    global m
    global a
    global query
    i -= 1
    result = (
        f"**Page - {i+1}**\n\n"
        f"➲Name: [{a[i]['Name']}]({a[i]['Url']})\n"
        f"➲Released on: {a[i]['ReleasedDate']}\n"
        f"➲Genre: {a[i]['Genre']}\n" 
        f"➲Rating: {a[i]['Rating']}\n"
        f"➲Likes: {a[i]['Likes']}\n"
        f"➲Duration: {a[i]['Runtime']}\n"
        f"➲Language: {a[i]['Language']}\n\n"
        f"➲First Link: `{a[i]['Dwnload1']}`\n\n"
        f"➲Second Link: `{a[i]['Download2']}`\n\n\n"
    )
    await m.edit(
        result,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(f"Prev",
                                         callback_data="yts_previous"),
                    InlineKeyboardButton(f"{emoji.CROSS_MARK}",
                                         callback_data="delete"),
                    InlineKeyboardButton(f"Next",
                                         callback_data="yts_next")
                ]
            ]
        ),
        parse_mode="markdown", disable_web_page_preview=True,
    )

#====== yts =======#

#====== torlock =======#

@app.on_message(filters.command(["torlock"]))
async def find_torlock(_, message):
    global m
    global i
    global a
    global query
    if len(message.command) < 2:
        await message.reply_text("Usage: /torlock query")
        return
    query = message.text.split(None, 1)[1].replace(" ", "%20")
    m = await message.reply_text("Searching")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.torrent.cloudns.cl/api/torlock/{query}") \
                    as resp:
                a = json.loads(await resp.text())
    except:
        await m.edit("Found Nothing.")
        return
    result = (
        f"**Page - {i+1}**\n\n"
        f"➲Name: {a[i]['Name']}\n"
        f"➲{a[i]['Uploader']} on "
        f"{a[i]['Date']}\n" 
        f"➲Size: {a[i]['Size']}\n"
        f"➲Leechers: {a[i]['Leechers']} || "
        f"➲Seeders: {a[i]['Seeders']}\n"
        f"➲Type: {a[i]['Category']}\n\n"
        f"➲Magnet: `{a[i]['Magnet']}`\n\n\n"
    )
    await m.edit(
        result,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(f"Next",
                                         callback_data="yts_next"),
                    InlineKeyboardButton(f"{emoji.CROSS_MARK}",
                                         callback_data="delete")
                ]
            ]
        ),
        parse_mode="markdown", disable_web_page_preview=True,
    )


@app.on_callback_query(filters.regex("torlock_next"))
async def callback_query_next_torlock(_, message):
    global i
    global m
    global a
    global query
    i += 1
    result = (
        f"**Page - {i+1}**\n\n"
        f"➲Name: [{a[i]['Name']}]({a[i]['Url']})\n"
        f"➲Released on: {a[i]['ReleasedDate']}\n"
        f"➲Genre: {a[i]['Genre']}\n" 
        f"➲Rating: {a[i]['Rating']}\n"
        f"➲Likes: {a[i]['Likes']}\n"
        f"➲Duration: {a[i]['Runtime']}\n"
        f"➲Language: {a[i]['Language']}\n\n"
        f"➲First Link: `{a[i]['Dwnload1']}`\n\n"
        f"➲Second Link: `{a[i]['Download2']}`\n\n\n"
    )
    await m.edit(
        result,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(f"Prev",
                                         callback_data="yts_previous"),
                    InlineKeyboardButton(f"{emoji.CROSS_MARK}",
                                         callback_data="delete"),
                    InlineKeyboardButton(f"Next",
                                         callback_data="yts_next")
                    
                ]
            ]
        ),
        parse_mode="markdown", disable_web_page_preview=True,
    )


@app.on_callback_query(filters.regex("torlock_previous"))
async def callback_query_previous_torlock(_, message):
    global i
    global m
    global a
    global query
    i -= 1
    result = (
        f"**Page - {i+1}**\n\n"
        f"➲Name: [{a[i]['Name']}]({a[i]['Url']})\n"
        f"➲Released on: {a[i]['ReleasedDate']}\n"
        f"➲Genre: {a[i]['Genre']}\n" 
        f"➲Rating: {a[i]['Rating']}\n"
        f"➲Likes: {a[i]['Likes']}\n"
        f"➲Duration: {a[i]['Runtime']}\n"
        f"➲Language: {a[i]['Language']}\n\n"
        f"➲First Link: `{a[i]['Dwnload1']}`\n\n"
        f"➲Second Link: `{a[i]['Download2']}`\n\n\n"
    )
    await m.edit(
        result,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(f"Prev",
                                         callback_data="yts_previous"),
                    InlineKeyboardButton(f"{emoji.CROSS_MARK}",
                                         callback_data="delete"),
                    InlineKeyboardButton(f"Next",
                                         callback_data="yts_next")
                ]
            ]
        ),
        parse_mode="markdown", disable_web_page_preview=True,
    )

#====== torlock =======#

#====== tgx =======#

@app.on_message(filters.command(["tgx"]))
async def find_tgx(_, message):
    global m
    global i
    global a
    global query
    if len(message.command) < 2:
        await message.reply_text("Usage: /tgx query")
        return
    query = message.text.split(None, 1)[1].replace(" ", "%20")
    m = await message.reply_text("Searching")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://www.jaybeetgx.cf/tor/{query}") \
                    as resp:
                a = json.loads(await resp.text())
    except:
        await m.edit("Found Nothing.")
        return
    result = (
        f"**Page - {i+1}**\n\n"
        f"➲Name: {a[i]['name']}\n"
        f"➲{a[i]['uploader']} on "
        f"{a[i]['date']}\n" 
        f"➲Size: {a[i]['size']}\n"
        f"➲Leechers: {a[i]['peers']} || "
        f"➲Seeders: {a[i]['seeders']}\n\n"
        f"➲Magnet: `{a[i]['magnet']}`\n\n\n"
    )
    await m.edit(
        result,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(f"Next",
                                         callback_data="tgx_next"),
                    InlineKeyboardButton(f"{emoji.CROSS_MARK}",
                                         callback_data="delete")
                ]
            ]
        ),
        parse_mode="markdown",
    )


@app.on_callback_query(filters.regex("tgx_next"))
async def callback_query_next_tgx(_, message):
    global i
    global m
    global a
    global query
    i += 1
    result = (
        f"**Page - {i+1}**\n\n"
        f"➲Name: {a[i]['name']}\n"
        f"➲{a[i]['uploader']} on "
        f"{a[i]['date']}\n" 
        f"➲Size: {a[i]['size']}\n"
        f"➲Leechers: {a[i]['peers']} || "
        f"➲Seeders: {a[i]['seeders']}\n\n"
        f"➲Magnet: `{a[i]['magnet']}`\n\n\n"
    )
    await m.edit(
        result,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(f"Prev",
                                         callback_data="tgx_previous"),
                    InlineKeyboardButton(f"{emoji.CROSS_MARK}",
                                         callback_data="delete"),
                    InlineKeyboardButton(f"Next",
                                         callback_data="tgx_next")
                    
                ]
            ]
        ),
        parse_mode="markdown",
    )


@app.on_callback_query(filters.regex("tgx_previous"))
async def callback_query_previous_tgx(_, message):
    global i
    global m
    global a
    global query
    i -= 1
    result = (
        f"**Page - {i+1}**\n\n"
        f"➲Name: {a[i]['name']}\n"
        f"➲{a[i]['uploader']} on "
        f"{a[i]['date']}\n" 
        f"➲Size: {a[i]['size']}\n"
        f"➲Leechers: {a[i]['peers']} || "
        f"➲Seeders: {a[i]['seeders']}\n\n"
        f"➲Magnet: `{a[i]['magnet']}`\n\n\n"
    )
    await m.edit(
        result,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(f"Prev",
                                         callback_data="tgx_previous"),
                    InlineKeyboardButton(f"{emoji.CROSS_MARK}",
                                         callback_data="delete"),
                    InlineKeyboardButton(f"Next",
                                         callback_data="tgx_next")
                ]
            ]
        ),
        parse_mode="markdown",
    )

#====== tgx =======#


@app.on_callback_query(filters.regex("delete"))
async def callback_query_delete(_, message):
    global m
    global i
    global a
    global query
    await m.delete()
    m = None
    i = 0
    a = None
    query = None

# OWNER ONLY    

# Setting Message

def get_text(message: Message) -> [None, str]:
    """Extract Text From Commands"""
    text_to_return = message.text
    if message.text is None:
        return None
    if " " in text_to_return:
        try:
            return message.text.split(None, 1)[1]
        except IndexError:
            return None
    else:
        return None

# Preparing

heroku_client = None
if HEROKU_API_KEY:
    heroku_client = heroku3.from_key(HEROKU_API_KEY)

def _check_heroku(func):
    @wraps(func)
    async def heroku_cli(client, message):
        heroku_app = None
        if not heroku_client:
            await message.reply_text("`Please Add HEROKU_API_KEY Key For This To Function To Work!`", parse_mode="markdown")
        elif not HEROKU_APP_NAME:
            await message.reply_text("`Please Add HEROKU_APP_NAME For This To Function To Work!`", parse_mode="markdown")
        if HEROKU_APP_NAME and heroku_client:
            try:
                heroku_app = heroku_client.app(HEROKU_APP_NAME)
            except:
                await message.reply_text(message, "`Heroku Api Key And App Name Doesn't Match!`", parse_mode="markdown")
            if heroku_app:
                await func(client, message, heroku_app)

    return heroku_cli

# Add Variable

@app.on_message(filters.command('setvar') & filters.user(OWNER_ID))
@_check_heroku
async def set_varr(client, message, app_):
    msg_ = await message.reply_text("`Please Wait!`")
    heroku_var = app_.config()
    _var = get_text(message)
    if not _var:
        await msg_.edit("`Here is Usage Syntax : .setvar KEY VALUE`", parse_mode="markdown")
        return
    if not " " in _var:
        await msg_.edit("`Here is Usage Syntax : .setvar KEY VALUE`", parse_mode="markdown")
        return
    var_ = _var.split(" ", 1)
    if len(var_) > 2:
        await msg_.edit("`Here is Usage Syntax : .setvar KEY VALUE`", parse_mode="markdown")
        return
    _varname, _varvalue = var_
    await msg_.edit(f"`Variable {_varname} Added With Value {_varvalue}!`")
    heroku_var[_varname] = _varvalue

# Delete Variable
        
@app.on_message(filters.command('delvar') & filters.user(OWNER_ID))
@_check_heroku
async def del_varr(client, message, app_):
    msg_ = await message.reply_text("`Please Wait!`", parse_mode="markdown")
    heroku_var = app_.config()
    _var = get_text(message)
    if not _var:
        await msg_.edit("`Give Var Name As Input!`", parse_mode="markdown")
        return
    if not _var in heroku_var:
        await msg_.edit("`This Var Doesn't Exists!`", parse_mode="markdown")
        return
    await msg_.edit(f"`Sucessfully Deleted {_var} Var!`", parse_mode="markdown")
    del heroku_var[_var]


app.run()
