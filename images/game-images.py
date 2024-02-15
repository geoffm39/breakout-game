from PIL import Image, ImageTk
import os

from constants import IMAGE_DIRECTORY


class GameImages:
    def __init__(self):
        self.images = {}

        self.load_images()

    def load_images(self):
        for filename in os.listdir(IMAGE_DIRECTORY):
            print(filename)
