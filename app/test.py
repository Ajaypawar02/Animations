import sys
import yaml
# import os
# sys.path.insert(0,'./Animations')
# sys.path.insert(1,'./examples/')
# sys.path.insert(2,'./TextExtraction-to-voice')
sys.path.append('/home/ubuntu/Animations')
sys.path.append('/home/ubuntu/Animations/examples')
sys.path.append('/home/ubuntu/Animations/TextExtraction-to-voice')
from examples.image_to_animation import image_to_animation
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from animated_drawings import render
from fastapi import FastAPI, Request
from dotenv import load_dotenv
from moviepy.editor import *
import urllib.request
import uvicorn
from typing import Dict
from pathlib import Path
import json
load_dotenv()
import cloudinary
from get_image import  audio_ocr
from schemas import APIPARAMTERS



cloudinary.config(
  cloud_name = "djvu7apub",
  api_key = "433374637814992",
  api_secret = "cyuhetMn3-yrGgOjJthC9FBy9FY",
  secure = True
)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def create_image(api_params : Dict):
    
    data = api_params
    motion = data['motion']
    image = data['image']


    if len(data['image_url']) == 1:
        motion = data['motion'][0]
        image_url = data['image_url'][0]
        char_anno_dir = os.getenv("OUTPUT")
        urllib.request.urlretrieve(image_url, "image.jpg")
        image_path = "image.jpg"
        # img = cv2.imread(image_path)

        if motion == 'dab' or motion == 'jumping' or motion == 'wave_hello':
            print("started")
            try:
                print("motion")
              
                print(sys.path)
                image_to_animation(image_path, char_anno_dir, f"{os.getenv('MOTION')}/{motion}.yaml", os.getenv('RETARGET'))
                print("executed")
            except Exception as e:
                return {
                    "status": "error",
                    "message": str(e),
                    "url": None
                }
            print(os.getenv("EXPORT_GIF"))
            with open(os.getenv("EXPORT_GIF"), "r") as f:
                data = yaml.load(f, Loader=yaml.FullLoader)

            data['scene']['ANIMATED_CHARACTERS'][0]['character_cfg'] = os.getenv("OUTPUT_CHAR_CFG")
            data["scene"]["ANIMATED_CHARACTERS"][0]["motion_cfg"] = f"{os.getenv('MOTION')}/{motion}.yaml"
            data['scene']['ANIMATED_CHARACTERS'][0]['retarget_cfg'] = os.getenv('RETARGET')


            print(data)
            

            try :
                with open('examplesssss.yaml', 'w') as file:
                    yaml.dump(data, file)
                print(Path('examplesssss.yaml'))
                yaml_data = yaml.dump(data)
                
                render.start('examplesssss.yaml')
                audio_path = "audio.wav"
                gif_path = "vedio.gif"
                audio = AudioFileClip(audio_path)
                if audio.duration < 10:
                    audio.duration = 10
                gif = VideoFileClip(gif_path).set_duration(audio.duration)
                final_clip = CompositeVideoClip([gif.set_audio(audio)])
                output_path = "file.mp4"
                final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")

            except Exception as e:
                return {
                    "status": "error",
                    "message": str(e),
                    "url": None
                }


if __name__ == "__main__":
  api_params = {
  "motion": [
    "dab"
  ],
  "image": "https://res.cloudinary.com/djvu7apub/image/upload/v1686329604/char3.jpg",
  "image_url": [
    "https://res.cloudinary.com/djvu7apub/image/upload/v1686329604/char3.jpg"
  ]
}
  response =  create_image(api_params=api_params)
  print(response)
                







