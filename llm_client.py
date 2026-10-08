import os
import time
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_llm_patch(vulnerable_code: str):
    prompt = f"""
    Analiza el siguiente código vulnerable en Python, genera un parche en formato diff (patch.diff) 
    para corregir la vulnerabilidad, e indica si consideras que la corrección es totalmente exitosa 
    (llm_claimed_success: true/false) junto con tu nivel de confianza (confidence de 0.0 a 1.0).

    Código vulnerable:
    {vulnerable_code}

    Responde estrictamente en formato JSON con las llaves: 
    "patch_diff", "llm_claimed_success", "confidence".
    """

    start_time = time.time()
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        latency = time.time() - start_time
        content = response.choices[0].message.content
        import json
        result = json.loads(content)
        result["latency"] = latency
        return result
    except Exception as e:
        print(f"Error al conectar con OpenAI: {e}")
        return None
