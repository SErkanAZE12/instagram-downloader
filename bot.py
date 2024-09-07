import telebot
import instaloader
from instaloader import Profile
import os


Token='YOUR_TOKEN'
bot=telebot.TeleBot(Token)
username='tabrizone'
loader = instaloader.Instaloader()


@bot.message_handler(commands=['start'])
def hello(msg):
    bot.send_message(msg.chat.id, 'Hello')

@bot.message_handler(commands=['send_images'])
def send_images(msg):
    
    IMAGE_FOLDER_PATH = '/content/tabrizone'
    
    # List all image files in the folder
    image_files = [os.path.join(IMAGE_FOLDER_PATH, file) for file in os.listdir(IMAGE_FOLDER_PATH) if file.endswith(('png', 'jpg', 'jpeg'))]
    
    if not image_files:
        bot.send_message(msg.chat.id, "No images found in the folder.")
        return
    
    # Send each image one by one
    for image_path in image_files:
        try:
            with open(image_path, 'rb') as photo:
                sendind=bot.send_photo(msg.chat.id, photo)
                message_id=sendind.message_id 
                
                bot.delete_message(msg.chat.id,message_id=message_id)
        except Exception as e:
            bot.send_message(msg.chat.id, f"Failed to send image {image_path}: {e}")
    
    
    bot.send_message(msg.chat.id, "All images have been sent.")
@bot.message_handler(func= lambda msg:True)
def download(msg):
    username=msg.text
    profile = Profile.from_username(loader.context, username)

# Download all posts from the profile
    for post in profile.get_posts():
        loader.download_post(post, target=profile.username)
bot.polling()

