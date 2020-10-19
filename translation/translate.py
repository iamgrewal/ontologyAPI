import requests
import json

class Translator():
    def get_translation(self,query,language="en"):
        url = "https://translation.googleapis.com/language/translate/v2?"
        key="AIzaSyCeWlMwjSm5kzftzjuiSERuH7ZG1wf2hUo"
        full_uri = url+"key="+key+"&q="+query+"&target="+language
        print(full_uri)
        response = requests.post(full_uri)
        response = response.text.replace("\n","")
        text = dict(json.loads(response))
        text = text["data"]["translations"][0]["translatedText"]
        return text