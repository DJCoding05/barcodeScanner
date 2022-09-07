# Kivy Dependencies
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

# Kivy UIX Dependencies
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.graphics.texture import Texture

# Other Dependencies needed
import cv2
from pyzbar import pyzbar
import apiLookup

class CameraApp(App):

    def build(self):
        self.camera = Image(size_hint=(1, .8))
        self.text = ""
        #self.button = Button(text='Take Photo', on_press=self.search(), size_hint=(1,.1))

        layout = BoxLayout(orientation='vertical')
        layout.add_widget(self.camera)
        # layout.add_widget(self.button)

        self.capture = cv2.VideoCapture(0)
        # Scheduling function on every interval (most likely the fps of the camera)
        Clock.schedule_interval(self.update, 1.0/33.0)

        return layout

    def update(self, *args):
        # Read Frames from webcam
        ret, frame = self.capture.read()
        # Shortens frame to 250 by 250
        frame = frame[120:120+250, 200:200+250, :]

        # Flip horizontal and convert webcam footage to OpenGL texture to display on kivy
        buf = cv2.flip(frame, 0).tostring()
        img_texture = Texture.create(
            size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        img_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        self.camera_copy = self.camera
        self.camera.texture = img_texture

        self.find_barcode(frame)

    def find_barcode(self, frame):
        barcode_result = ""
        barcodes = pyzbar.decode(frame)
        if barcodes:
            for barcode in barcodes:
                barcode_result = barcode.data.decode('utf-8')
            
        print(apiLookup.search(barcode_result))



if __name__ == '__main__':
    CameraApp().run()
