import hashlib
import urllib.request, urllib.error, urllib.parse

class brain():

    def __init__(self, key="none"):
        self.url = 'http://www.cleverbot.com/webservicemin'
        self.endIndex = 35
        self.vars = {}
        self.vars['start'] = 'y'
        self.vars['icognoid'] = 'wsf'
        self.vars['fno'] = '0'
        self.vars['sub'] = 'Say'
        self.vars['islearning'] = '1'
        self.vars['cleanslate'] = 'false'

    def _utils_string_at_index(self, strings, index):
        if len(strings) > index:
            return strings[index]
        else:
            return ''

    def think(self, thought):
        self.vars['stimulus'] = thought

	#Requete l'API
        data = urllib.parse.urlencode(self.vars)
        data_to_digest = data[9:self.endIndex]
        data_digest = hashlib.md5(data_to_digest.encode('utf-8')).hexdigest()
        data = data + '&icognocheck=' + data_digest
        url_response = urllib.request.urlopen(self.url, data.encode('utf-8'))
        response = url_response.read().decode('utf-8')

	#Mise en forme de la réponse
        response_values = response.split('\r')
        #self.vars['??'] = self._utils_string_at_index(response_values, 0)
        self.vars['sessionid'] = self._utils_string_at_index(response_values, 1)
        self.vars['logurl'] = self._utils_string_at_index(response_values, 2)
        self.vars['vText8'] = self._utils_string_at_index(response_values, 3)
        self.vars['vText7'] = self._utils_string_at_index(response_values, 4)
        self.vars['vText6'] = self._utils_string_at_index(response_values, 5)
        self.vars['vText5'] = self._utils_string_at_index(response_values, 6)
        self.vars['vText4'] = self._utils_string_at_index(response_values, 7)
        self.vars['vText3'] = self._utils_string_at_index(response_values, 8)
        self.vars['vText2'] = self._utils_string_at_index(response_values, 9)
        self.vars['prevref'] = self._utils_string_at_index(response_values, 10)
        #self.vars['??'] = self._utils_string_at_index(response_values, 11)
        self.vars['emotionalhistory'] = self._utils_string_at_index(response_values, 12)
        self.vars['ttsLocMP3'] = self._utils_string_at_index(response_values, 13)
        self.vars['ttsLocTXT'] = self._utils_string_at_index(response_values, 14)
        self.vars['ttsLocTXT3'] = self._utils_string_at_index(response_values, 15)
        self.vars['ttsText'] = self._utils_string_at_index(response_values, 16)
        self.vars['lineRef'] = self._utils_string_at_index(response_values, 17)
        self.vars['lineURL'] = self._utils_string_at_index(response_values, 18)
        self.vars['linePOST'] = self._utils_string_at_index(response_values, 19)
        self.vars['lineChoices'] = self._utils_string_at_index(response_values, 20)
        self.vars['lineChoicesAbbrev'] = self._utils_string_at_index(response_values, 21)
        self.vars['typingData'] = self._utils_string_at_index(response_values, 22)
        self.vars['divert'] = self._utils_string_at_index(response_values, 23)

        response = self.vars['ttsText']
        return response


class info():

    def getModuleName(self):
        return "Cleverbot"

    def getSupportedLanguage(self):
        #Supported language of Cleverbot
        return [["English", "en"], ["French", "fr"]]
