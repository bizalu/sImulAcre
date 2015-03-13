# -*- coding: utf8 -*-

import sys
sys.path.append("../../core/lib")

import speech_recognition as sr


class ears():
    
    def __init__(self, lang):
        self.sr = sr
        self.lang = lang
        self.rec = sr.Recognizer(self.lang) 


    def listen(self):
        message = ""

        #listen the microphone
        with self.sr.Microphone() as source:
            audio = self.rec.listen(source)

        #ask to google to recognize what you say
        try:
            message = self.rec.recognize(audio)
        except LookupError: 
            print("Could not understand audio")
    
        return message


class info():

    def getModuleName(self):
        return "Google Chrome"

    def getSupportedLanguage(self):
        #Supported language of Google translate
        return [["Afrikaans", "af"], ["Albanian", "sq"], ["Arabic", "ar"], ["Azerbaijani", "az"], ["Basque", "eu"], ["Bengali", "bn"], ["Belarusian", "be"], ["Bulgarian", "bg"], ["Catalan", "ca"], ["Chinese Simplified", "zh-CN"], ["Chinese Traditional", "zh-TW"], ["Croatian", "hr"], ["Czech", "cs"], ["Danish", "da"], ["Dutch", "nl"], ["English", "en"], ["Esperanto", "eo"], ["Estonian", "et"], ["Filipino", "tl"], ["Finnish", "fi"], ["French", "fr"], ["Galician", "gl"], ["Georgian", "ka"], ["German", "de"], ["Greek", "el"], ["Gujarati", "gu"], ["Haitian Creole", "ht"], ["Hebrew", "iw"], ["Hindi", "hi"], ["Hungarian", "hu"], ["Icelandic", "is"], ["Indonesian", "id"], ["Irish", "ga"], ["Italian", "(it)"], ["Japanese", "ja"], ["Kannada", "kn"], ["Korean", "ko"], ["Latin", "la"], ["Latvian", "lv"], ["Lithuanian", "lt"], ["Macedonian", "mk"], ["Malay", "ms"], ["Maltese", "mt"], ["Norwegian", "no"], ["Persian", "fa"], ["Polish", "pl"], ["Portuguese", "pt"], ["Romanian", "ro"], ["Russian", "ru"], ["Serbian", "sr"], ["Slovak", "sk"], ["Slovenian", "sl"], ["Spanish", "es"], ["Swahili", "sw"], ["Swedish", "sv"], ["Tamil", "ta"], ["Telugu", "te"], ["Thai", "th"], ["Turkish", "tr"], ["Ukrainian", "uk"], ["Urdu", "ur"], ["Vietnamese", "vi"], ["Welsh", "cy"], ["Yiddish", "yi"]]
