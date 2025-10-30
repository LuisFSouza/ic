from deep_translator import GoogleTranslator

def translate(text):
    translator = GoogleTranslator(source='en', target='pt')
    translation = translator.translate(text)
    return translation