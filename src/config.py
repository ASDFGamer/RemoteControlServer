"""
This module is used for all interactions with the config of the program.
"""
import configparser

class Config:

    __DEFAULT__ = {''}

    def __init__(self, path):
        self.path = path

    def create(self):
        config = configparser.SafeConfigParser()


