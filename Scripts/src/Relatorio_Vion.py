import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
from PIL import Image
from io import BytesIO
import base64

env_ = "Scripts\src\.env"
load_dotenv(env_)
class Vaion_vision_Relatorio:
    def __init__(self, imagem:str):
        # Atributos para a classe Vaion_vision_Relatorio
        self.imagem_vision = imagem
    def Relatorio_IA(self):
        with Image.open(self.imagem_vision) as image:
            buffer = BytesIO()
            image.save(buffer, format="JPEG")

        image_base64 = base64.b64encode(
            buffer.getvalue()
        ).decode("utf-8")

        KEY_API_GROQ = Groq(
           api_key= os.getenv("KEY_API_GROQ_IA")
        )

        RES_GROQ = KEY_API_GROQ.chat.completions.create(
            model="qwen/qwen3.8-27b",
            messages=[
                {
                    "role":"user",
                    "content":[
                        {
                            "type":"text",
                            "text":"Oque voce ve?"
                        },
                        {
                            "type":"image_url",
                            "image_url":{
                                "url":f"data:image/jpeg;base64,{image_base64}"
                            }
                        }
                    ]
                }
            ],
            temperature=1,
            top_p=1,
            stream=False,
            stop=None,
            max_completion_tokens=500

        )
        texto = RES_GROQ.choices[0].message.content
        return texto
        

Vaion = Vaion_vision_Relatorio(r"Scripts\\src\\e011.jpg")

print(Vaion.Relatorio_IA())
