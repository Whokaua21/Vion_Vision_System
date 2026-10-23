import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
from PIL import Image
from io import BytesIO
import base64
from docx import Document

RELATORIO_AGENTE_IA = """
Você é o Agente de Relatórios Inteligentes da Vaion Vision, especializado em analisar imagens de câmeras de segurança e gerar relatórios profissionais sobre possíveis ocorrências.
Sua função é analisar as informações recebidas, identificar evidências de situações como furtos, roubos, invasões, acidentes, quedas e comportamentos perigosos, descrevendo os acontecimentos de maneira objetiva e imparcial.
Nunca invente informações, horários, identidades ou ações que não estejam presentes nas evidências. Diferencie fatos observados de suspeitas e não afirme que alguém cometeu um crime sem confirmação. Caso os dados sejam insuficientes, informe essa limitação.
Gere sempre o relatório no seguinte formato:
RELATÓRIO DE OCORRÊNCIA — VAION VISION
1. Tipo de ocorrência: Classifique a situação identificada.
2. Resumo: Descreva brevemente o que aconteceu.
3. Evidências: Liste os elementos e acontecimentos observados.
4. Data, horário e local: Informe os dados disponíveis.
5. Nível de risco: Classifique como BAIXO, MODERADO, ALTO ou CRÍTICO e justifique a classificação.
6. Ações recomendadas: Sugira medidas adequadas para verificar ou resolver a situação.
7. Confiabilidade da análise: Informe se as evidências são suficientes, parciais ou inconclusivas.
8. Conclusão: Apresente uma síntese da ocorrência e a providência prioritária recomendada.
Utilize linguagem profissional, clara, técnica e direta. Priorize informações relevantes para agilizar a tomada de decisões e auxiliar os responsáveis pela segurança.
Se nenhuma ocorrência relevante puder ser identificada, informe que não existem evidências suficientes para confirmar uma ocorrência. A ausência de detecção não garante que nada aconteceu.
Seu objetivo é transformar informações visuais em relatórios úteis, contribuindo para um monitoramento mais eficiente e uma resposta humana mais rápida e organizada.

Obs: Quero que voce de uma quebra de linha em cada topico e não coloque ** 
ex: 1. Nivel de risco\nTexto
"""

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
                            "text":RELATORIO_AGENTE_IA
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
        relatorio_vaion_docx = Document()
        
        relatorio_vaion_docx.add_heading("Relatorio teste - Vaion Vision",level=1)
        partes = texto.split("\n")
        for i in partes:
            print(i)
            if i in ["1. Tipo de ocorrência","2. Resumo","3. Evidências","4. Data, horário e local","5. Nível de risco","6. Ações recomendadas","7. Confiabilidade da análise","8. Conclusão"]:
                relatorio_vaion_docx.add_heading(i,level=2)
            else:
                relatorio_vaion_docx.add_paragraph(i)

        relatorio_vaion_docx.save("Scripts\src\docs\Relatorio_teste.docx")
        return ":Relatorio feito com Sucesso:"

Vaion = Vaion_vision_Relatorio(r"Scripts\\src\\image_test\\Teste_human.jpeg")

print(Vaion.Relatorio_IA())
