from azure.ai.translation.text import TextTranslationClient
from azure.core.credentials import AzureKeyCredential

def translate_text(text, target_language="es"):
    translator_key = "4cypniRyc1YF5mIRsHPMkU663BUSurRpXqYC8ky3XEa0Dz5y8lgTJQQJ99BAACYeBjFXJ3w3AAAbACOGwXGj"
    translator_endpoint = "https://api.cognitive.microsofttranslator.com/"
    
    # Create a Translator client
    translator_client = TextTranslationClient(endpoint=translator_endpoint, credential=AzureKeyCredential(translator_key))
    
    # Perform translation
    response = translator_client.translate(content=[{'text': text}], to=[target_language])
    return response[0].translations[0].text
