import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq


env_ = "Scripts\src\.env"
load_dotenv(env_)


User_Vaion_Cliente = Groq(
    api_key= os.getenv("KEY_API_GROQ_IA")
)

res_Groq = User_Vaion_Cliente.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
        {
            "role":"system",
            "content":"""
                Você é uma IA que responde em portugues feitos para calculos
            """
        },
        {
            "role":"user",
            "content":[
                {
                    "type":"text",
                    "text":(
                        """
                        """
                    )
                },
                {
                    "type":"image_url",
                    "image_url":{
                        "url":(
                            f"data:{};base64"
                        )
                    }
                }
            ]
        }
    ]

)

print(res_Groq.choices[0].message.content)