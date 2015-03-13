import urllib.request, urllib.parse, urllib.error
import urllib.request, urllib.error, urllib.parse
import uuid
import xml.dom.minidom

class brain():

    def __init__(self, key):
        self.url = 'http://www.pandorabots.com/pandora/talk-xml'
        self.vars = {}
        self.vars['botid'] = key
        self.vars['custid'] = uuid.uuid1()

    def think(self, thought):
        self.vars['input'] = thought

        #Requete l'API
        data = urllib.parse.urlencode(self.vars)
        url_response = urllib.request.urlopen(self.url, data.encode())
        response = url_response.read().decode()
        response_dom = xml.dom.minidom.parseString(response)

        response_thought = response_dom.getElementsByTagName('that')[0].childNodes[0].data.strip()
        return response_thought
      
        
class info():

    def getModuleName(self):
        return "Pandora"

    def getSupportedLanguage(self):
        #Supported language of Pandora
        return [["English", "en"]]
