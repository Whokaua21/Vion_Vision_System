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
    def __init__(self, imagem:str,res_yolo:str):
        # Atributos para a classe Vaion_vision_Relatorio
        self.imagem_vision = imagem
        self.res_yolo_test = res_yolo

    def Converter_imagem_base64(self):
        # Aqui ele ira converter as imagens para uma base64, para a ia entender a imagem
        with Image.open(self.imagem_vision) as image:
            buffer = BytesIO()
            image.save(buffer, format="JPEG")

            image_base64 = base64.b16encode(
                buffer.getvalue()
            ).decode("utf-8")
        return image_base64

    def IA_comands(self):
        #Aqui sera a parte da IA fazer um relatorio da situação e caracteriazar o nivel e acontecimentos

        yolo_analise = Groq(
            api_key= os.getenv("KEY_API_GROQ_IA")  
        )

        res_ia = yolo_analise.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[{
                "role":"system",
                "content":"Responda de um jeito tecnico, como voce fosse um professor "
            },
            {
                "role":"user",
                "content":self.res_yolo_test
            }]

        )
        return res_ia.choices[0].message.content
        
        


Vaion_r = Vaion_vision_Relatorio(r'Scripts\\src\\e011.jpg',"Voce consegue detectar imagens?")
print(Vaion_r.IA_comands())