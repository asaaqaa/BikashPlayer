# Powered By @BikashHalder @AdityaHalder
# ©️ Copy Right By Bikash Halder Or Aditya Halder
# Any Problem To Report @Bgt_Chat or @AdityaDiscus
# Bot Owner @BikashHalder Or @AdityaHalder

from pyrogram import filters
from pyrogram.types import Message

from Bikash.config import BANNED_USERS
from Bikash.strings import get_command
from Bikash import YouTube, app
from Bikash.core.call import Bikashh
from Bikash.misc import db
from Bikash.utils import AdminRightsCheck, seconds_to_min

# Commands
SEEK_COMMAND = get_command("SEEK_COMMAND")


@app.on_message(
    filters.command(["SEEK_COMMAND"],prefixes= ["/", "!","","#"]))
    & filters.group
    & ~filters.edited
    & ~BANNED_USERS
)
@AdminRightsCheck
async def seek_comm(cli, message: Message, _, chat_id):
    if len(message.command) == 1:
        return await message.reply_text(_["admin_28"])
    query = message.text.split(None, 1)[1].strip()
    if not query.isnumeric():
        return await message.reply_text(_["admin_29"])
    playing = db.get(chat_id)
    if not playing:
        return await message.reply_text(_["queue_2"])
    duration_seconds = int(playing[0]["seconds"])
    if duration_seconds == 0:
        return await message.reply_text(_["admin_30"])
    file_path = playing[0]["file"]
    if "index_" in file_path or "live_" in file_path:
        return await message.reply_text(_["admin_30"])
    duration_played = int(playing[0]["played"])
    duration_to_skip = int(query)
    duration = playing[0]["dur"]
    if message.command[0][-2] == "c":
        if (duration_played - duration_to_skip) <= 10:
            return await message.reply_text(
                _["admin_31"].format(
                    seconds_to_min(duration_played), duration
                )
            )
        to_seek = duration_played - duration_to_skip + 1
    else:
        if (
            duration_seconds - (duration_played + duration_to_skip)
        ) <= 10:
            return await message.reply_text(
                _["admin_31"].format(
                    seconds_to_min(duration_played), duration
                )
            )
        to_seek = duration_played + duration_to_skip + 1
    mystic = await message.reply_text(_["admin_32"])
    if "vid_" in file_path:
        n, file_path = await YouTube.video(playing[0]["vidid"], True)
        if n == 0:
            return await message.reply_text(_["admin_30"])
    try:
        await Anon.seek_stream(
            chat_id,
            file_path,
            seconds_to_min(to_seek),
            duration,
            playing[0]["streamtype"],
        )
    except:
        return await mystic.edit_text(_["admin_34"])
    if message.command[0][-2] == "c":
        db[chat_id][0]["played"] -= duration_to_skip
    else:
        db[chat_id][0]["played"] += duration_to_skip
    await mystic.edit_text(
        _["admin_33"].format(seconds_to_min(to_seek))
    )
