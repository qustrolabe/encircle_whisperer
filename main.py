#!/usr/bin/env python
import ffmpeg
import logging
import os

from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )

from telegram import ForceReply, Update, File, Video, Audio
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Please send 640x640 video shorter than 60s or audio file.")

async def whisper_reply(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    audio: Audio = update.message.audio

    audio_file: File = await audio.get_file()
    await audio_file.download_to_drive("tmp_audio_file1")
    ffmpeg.input("tmp_audio_file1").output("tmp_audio_file2", format='opus', acodec="libopus").overwrite_output().run()
    await update.message.reply_voice("tmp_audio_file2")

    os.remove("tmp_audio_file1")
    os.remove("tmp_audio_file2")
    

async def encircle_reply(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    video: Video = update.message.video

    if video.width == 640 and video.height == 640 and video.duration <= 60:    
        video_file: File = await video.get_file()
        await video_file.download_to_drive("tmp_video_file")
        await update.message.reply_video_note("tmp_video_file")
        os.remove("tmp_video_file")
    else:
        await update.message.reply_text("Video must be 640x640 60s long got %sx%s %ss long" % (video.width, video.height, video.duration))

async def text_reply(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await help_command(update, context)

def main() -> None:
    key = open(".env").read().strip()
    application = Application.builder().token(key).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.VIDEO & ~filters.COMMAND, text_reply))
    application.add_handler(MessageHandler(filters.AUDIO & ~filters.COMMAND, whisper_reply))
    application.add_handler(MessageHandler(filters.VIDEO & ~filters.COMMAND, encircle_reply))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()

if __name__ == "__main__":
    main()