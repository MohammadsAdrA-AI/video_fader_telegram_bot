from flask import Flask, send_file
from flask import request
from flask import Response
import requests
import json
import subprocess

 
TOKEN = "*"


app = Flask(__name__)
def tel_parse_message(message):
    print("message-->",message)
    try:
        chat_id = message['message']['chat']['id']
        txt = message['message']['text']
        print("chat_id-->", chat_id)
        print("txt-->", txt)
 
        return chat_id,txt
    except:
        print("NO text found-->>") 

def tel_parse_get_message(message):
    print("message-->",message)
    print("1")
   
    try:
        g_chat_id = message['message']['chat']['id']
        g_file_id = message['message']['photo'][0]['file_id']
        print("g_chat_id-->", g_chat_id)
        print("g_image_id-->", g_file_id)
 
        return g_file_id
    except:
        try:
            g_chat_id = message['message']['chat']['id']
            g_file_id = message['message']['video']['file_id']
            print("g_chat_id-->", g_chat_id)
            print("g_video_id-->", g_file_id)
 
            return g_file_id
        except:
		        print("NO file found found-->>")
 
def tel_send_message(chat_id, text):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {
                'chat_id': chat_id,
                'text': text
                }
   
    r = requests.post(url,json=payload)
 
    return r
def tel_send_video(chat_id):
    url = f'https://api.telegram.org/bot{TOKEN}/sendVideo'
    filename = "./result/voice_and_video_changed.mp4"

 
    return filename
def tel_upload_file(file_id):
    url = f'https://api.telegram.org/bot{TOKEN}/getFile?file_id={file_id}'
    a = requests.post(url)
    json_resp = json.loads(a.content)
    print("a-->",a)
    print("json_resp-->",json_resp)
    file_pathh = json_resp['result']['file_path']
    print("file_path-->", file_pathh)
   
    url_1 = f'https://api.telegram.org/file/bot{TOKEN}/{file_pathh}'
    b = requests.get(url_1)
    file_content = b.content
    with open(file_pathh, "wb") as f:
        f.write(file_content)  
    subprocess.call(['sh', './Video_fader.sh','./videos/'])

def tel_send_image(chat_id):
    filename = "./MicrosoftTeams-image.png"
    return send_file(filename, mimetype="image/gif")
 
@ app.route('/', methods=['GET', 'POST'])
def index():
    

    if request.method == 'POST':
        msg = request.get_json()
        try: 
            tel_parse_message(msg)
            chat_id,txt = tel_parse_message(msg)
            if txt == "hi":
                tel_send_message(chat_id,"Hello!!")
            else:
                tel_send_message(chat_id,'from webhook')
       
            return Response('ok', status=200)

        except:
            try: 
                file_id = tel_parse_get_message(msg)
                tel_upload_file(file_id)
                return Response('ok', status=200)
            except:
                return Response('ok', status=200)

    else:
        return "<h1>Welcome!</h1>"
 
if __name__ == '__main__':
    app.run(threaded=True, debug=True)