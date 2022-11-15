# Import libraries
from telegram import Update
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters
import os, subprocess

# Base variables
DOWNLOAD_LOCATION = "./temp/"

# Send welcome message to new users
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Welcome to my video Fader bot.')

def meta_date_reader():
    file1 = open('./result/meta_data.txt', 'r')
    Lines = file1.readlines()
    created_time = Lines[7]
    return created_time
def audio_extractor(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user['id']
    # Download video
    input_name = update.message.video.file_name
    input_ext = input_name.split('.')[-1]
    file_id = update.message.video.file_id
    file = context.bot.getFile(file_id)
    input_path = f'./temp/{file_id}.{input_ext}'
    output_path = f'./result/blurred_video.mp4'
    print('here')
    file.download(input_path)
    # Extract audio
    subprocess.call(['sh', './Video_fader.sh','./temp/'])
    # Send audio
    context.bot.send_video(chat_id=user_id, video=open(output_path, 'rb'), supports_streaming=True)
    created_time = meta_date_reader()
    update.message.reply_text(created_time)
    # Delete files
    os.remove(input_path)
    os.remove(output_path)


if __name__ == '__main__':
    updater = Updater(token='5628937070:AAF62VD5pYkVrB6IGrv3UGJc4QvhR_nhdfc',
                      request_kwargs={'read_timeout': 1000, 'connect_timeout': 1000})
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.video, audio_extractor))

    updater.start_polling()
    updater.idle()