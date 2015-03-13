# -*- coding: utf8 -*-

import os, sys
import re
import urllib.request, urllib.error, urllib.parse
import time
from pydub import AudioSegment


class voice():

    def __init__(self, language):
        self.vars = {}
        self.vars['tl'] = language
        self.output = "/tmp/speech.mp3"
        self.woutput = "/tmp/speech.wav"
        self.url = "http://translate.google.com/translate_tts"
        self.lenmax = 100


    def say(self, message):
        self._audio_extract(message)
        try:
            #convert mp3 to wav
            sound = AudioSegment.from_mp3(self.output)
            sound.export(self.woutput, format="wav")
            
            #read wav file
            os.system("aplay " + self.woutput)
            
            #delete temporary output files
            os.system("rm -f self.woutput self.output 1> /dev/null")
        except:
            sys.stderr.write("Google translate's module return error")


    def read(self, file):
        f = open(file, 'r')
        message = f.read()
        f.close()
        self._audio_extract(message)
        try:
            #convert mp3 to wav
            sound = AudioSegment.from_mp3(self.output)
            sound.export(self.woutput, format="wav")
            
            #read wav file
            os.system("aplay " + self.woutput)
            
            #delete temporary output files
            os.system("rm -f self.woutput self.output 1> /dev/null")
        except:
            sys.stderr.write("Google translate's module return error")


    def _split_text(self, message):
        split_text = {}

        #Si le text est plus petit que lenmax, return le text
        if (len(message) < self.lenmax):
            split_text[0] = message
            return split_text

        #Sinon on sépare le text en phrase (determiné par le .)
        split_point = message.split('.')
        idx = 0
        for sentence in split_point:
            #Remise en forme de la phrase
            if (sentence == ''):
                continue
            if (not sentence == message):
                sentence = sentence + '.'
            sentence = re.sub('^ ', '', sentence)


            #Traitement de la phrase
            if (len(sentence) < self.lenmax):
                split_text[idx] = sentence
                idx += 1
            else:


                #Si ce n'est pas encore suffisant on sépare la phrase en respiration (déterminé par la ,)
                split_comma = sentence.split(', ')
                for breath in split_comma:
                    #Remise en forme de la respiration
                    if (not breath == sentence and not breath[len(breath) - 1] == '.'):
                        breath = breath + ','
                    breath = re.sub('^ ', '', breath)

                    #Traitement de la respiration
                    if (len(breath) < self.lenmax):
                        split_text[idx] = breath
                        idx +=1
                    else:


                        #Si ce n'est toujours pas suffisant on sépare les respirations en groupement de mot < self.lenmax
                        word_group = ""
                        split_word = breath.split()
                        for word in split_word:
                            #traitement du mot
                            if(len(word_group + " " + word) < self.lenmax):
                                word_group = word_group + " " + word
                            else:
                                split_text[idx] = re.sub('^ ', '', word_group)
                                idx += 1
                                word_group = word


                        #Traitement de la fin de la phrase
                        if (len(word_group) > 0):
                            split_text[idx] = re.sub('^ ', '', word_group)
                            idx += 1


        #Rattrapage des séparations injustifiées
        idx = 0
        while (idx < len(split_text) - 1):
            #Si 2 lignes peuvent être concatenées, on le fait et on recalcul les indexes
            if ( len(split_text[idx] + " " + split_text[idx + 1]) < self.lenmax ):
                #Concatenation des lignes
                split_text[idx] = split_text[idx] + " " + split_text[idx + 1]

                #On remonte toutes les lignes d'un cran
                line = idx + 1
                while ( line < len(split_text) - 1):
                    split_text[line] = split_text[line + 1]
                    line += 1

                #On supprime la dernière ligne
                del split_text[len(split_text) - 1]
            else:
                idx += 1


        return split_text


    def _audio_extract(self, input_text):
        combined_text = self._split_text(input_text)

        #download chunks and write them to the output file
        mp3file = open(self.output, 'wb+')
        for line in combined_text:
            idx = line
            val = combined_text[line]
            self.vars['q'] = val.encode('utf-8')
            self.vars['total'] = str(len(combined_text))
            self.vars['idx'] = str(idx)
            
            if len(val) > 0:
                try:
                    data = urllib.parse.urlencode(self.vars)
                    headers = {"Host": "translate.google.com",
                           "Referer": "http://www.gstatic.com/translate/sound_player2.swf",
                           "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) "
                                         "AppleWebKit/535.19 (KHTML, like Gecko) "
                                         "Chrome/18.0.1025.163 Safari/535.19"
                    }
                    req = urllib.request.Request(self.url, data.encode('utf-8'), headers)
                    response = urllib.request.urlopen(req)
                    mp3file.write(response.read())
                    time.sleep(.5)
                except urllib.error.URLError as e:
                    print (('%s' % e))
        
        mp3file.close()



class info():

    def getModuleName(self):
        return "Google translate"

    def getSupportedLanguage(self):
        #Supported language of Google translate
        return [["Afrikaans", "af"], ["Albanian", "sq"], ["Arabic", "ar"], ["Azerbaijani", "az"], ["Basque", "eu"], ["Bengali", "bn"], ["Belarusian", "be"], ["Bulgarian", "bg"], ["Catalan", "ca"], ["Chinese Simplified", "zh-CN"], ["Chinese Traditional", "zh-TW"], ["Croatian", "hr"], ["Czech", "cs"], ["Danish", "da"], ["Dutch", "nl"], ["English", "en"], ["Esperanto", "eo"], ["Estonian", "et"], ["Filipino", "tl"], ["Finnish", "fi"], ["French", "fr"], ["Galician", "gl"], ["Georgian", "ka"], ["German", "de"], ["Greek", "el"], ["Gujarati", "gu"], ["Haitian Creole", "ht"], ["Hebrew", "iw"], ["Hindi", "hi"], ["Hungarian", "hu"], ["Icelandic", "is"], ["Indonesian", "id"], ["Irish", "ga"], ["Italian", "(it)"], ["Japanese", "ja"], ["Kannada", "kn"], ["Korean", "ko"], ["Latin", "la"], ["Latvian", "lv"], ["Lithuanian", "lt"], ["Macedonian", "mk"], ["Malay", "ms"], ["Maltese", "mt"], ["Norwegian", "no"], ["Persian", "fa"], ["Polish", "pl"], ["Portuguese", "pt"], ["Romanian", "ro"], ["Russian", "ru"], ["Serbian", "sr"], ["Slovak", "sk"], ["Slovenian", "sl"], ["Spanish", "es"], ["Swahili", "sw"], ["Swedish", "sv"], ["Tamil", "ta"], ["Telugu", "te"], ["Thai", "th"], ["Turkish", "tr"], ["Ukrainian", "uk"], ["Urdu", "ur"], ["Vietnamese", "vi"], ["Welsh", "cy"], ["Yiddish", "yi"]]
