import kivy
kivy.require('1.10.0') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.properties import StringProperty, ObjectProperty, NumericProperty
from kivy.core.audio import SoundLoader
import os
import pygame

PIANOKEY=('a0','a0m','b0','c1','c1m','d1','d1m','e1','f1','f1m','g1','g1m','a1','a1m','b1', \
          'c2', 'c2m', 'd2', 'd2m', 'e2', 'f2', 'f2m', 'g2', 'g2m','a2','a2m','b2', \
          'c3', 'c3m', 'd3', 'd3m', 'e3', 'f3', 'f3m', 'g3', 'g3m', 'a3', 'a3m', 'b3', \
          'c4', 'c4m', 'd4', 'd4m', 'e4', 'f4', 'f4m', 'g4', 'g4m', 'a4', 'a4m', 'b4', \
          'c5', 'c5m', 'd5', 'd5m', 'e5', 'f5', 'f5m', 'g5', 'g5m', 'a5', 'a5m', 'b5', \
          'c6', 'c6m', 'd6', 'd6m', 'e6', 'f6', 'f6m', 'g6', 'g6m', 'a6', 'a6m', 'b6', \
          'c7', 'c7m', 'd7', 'd7m', 'e7', 'f7', 'f7m', 'g7', 'g7m', 'a7', 'a7m', 'b7','c8')

class soundButton(Button):
    filename= StringProperty(None)
    sound= ObjectProperty(None,allownone=True)

    def on_press(self):
        self.sound=SoundLoader.load(self.filename)
        self.sound.play()

class Keys(GridLayout):
    def __init__(self,**kwargs):
        super(Keys,self).__init__(**kwargs)
        self.cols=12
        for k in PIANOKEY:
            btn=soundButton(text=k,filename="raw_ogg/"+k+".ogg",halign='center')
            self.add_widget(btn)

class MyApp(App):
    def build(self):
        return Keys()


if __name__ == '__main__':
    MyApp().run()