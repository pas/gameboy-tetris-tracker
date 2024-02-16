import tempfile

from PIL import Image
import PySimpleGUI as sg

from tetristracker.capturer.mss_capturer import MSSCapturer
from tetristracker.capturer.obs_virtual_cam_capturer import OBSVirtualCamCapturer
from tetristracker.gui.window import Window
from tetristracker.helpers.config import Config



class TrimmedImageWindow(Window):
  def __init__(self):
    self.config = Config()
    self.bounding_box = None
    self.temp_dir = tempfile.TemporaryDirectory()
    self._init_bounding_box()
    self.create_image()


  def get_path(self):
      return self.temp_dir.name + "\image.png"

  def modal(self):
      return True

  def finalize(self):
     return True

  def _update(self):
    self.input_width.update(self.bounding_box["width"])
    self.input_height.update(self.bounding_box["height"])
    self.input_left.update(self.bounding_box["left"])
    self.input_top.update(self.bounding_box["top"])

  def _window_create_hook(self):
    self._update()

  def _init_bounding_box(self):
    if self.config.get_capturer() == "screen":
        self.bounding_box = self.config.get_screen_bounding_box()
    if self.config.get_capturer() == "obs":
        self.bounding_box = self.config.get_obs_bounding_box()

  def _save_bounding_box(self):
    if self.config.get_capturer() == "screen":
        self.bounding_box = self.config.set_screen_bounding_box(self.bounding_box)
    if self.config.get_capturer() == "obs":
        self.bounding_box = self.config.set_obs_bounding_box(self.bounding_box)

  def create_image(self):
    if self.config.get_capturer() == "screen":
        self.image = self.retrieve_screenshot_mss()
    if self.config.get_capturer() == "obs":
        self.image = self.retrieve_camera_image()

    self.image = Image.fromarray(self.image)
    self.image.save(self.get_path(), format="PNG")

  def retrieve_camera_image(self):
      capturer = OBSVirtualCamCapturer(bounding_box=self.bounding_box,
                                       config=self.config)
      return capturer.grab_image()

  def retrieve_screenshot_mss(self):
      capturer = MSSCapturer(bounding_box=self.bounding_box)
      return capturer.grab_image()

  def name(self):
      return "trimmed-image"

  def layout(self):
    self.image_view = sg.Image(self.get_path())
    self.input_width = sg.Input(key='__WIDTH__')
    self.input_height = sg.Input(key='__HEIGHT__')
    self.input_top = sg.Input(key='__TOP__')
    self.input_left = sg.Input(key='__LEFT__')

    return [[ sg.Column([[self.image_view]]),
              sg.Column([
                          [sg.Text("Width")],
                          [self.input_width],
                          [sg.Text("Height")],
                          [self.input_height],
                          [sg.Text("Top")],
                          [self.input_top],
                          [sg.Text("Left")],
                          [self.input_left],
                          [sg.Button("Retake", key="__RETAKE__")],
                          [sg.Button("Save", key="__SAVE__")],
                          [sg.Button("Reset", key="__RESET__")],
                        ])
           ]]

  def _retake(self):
    self.bounding_box["height"] = int(self.input_height.get())
    self.bounding_box["width"] = int(self.input_width.get())
    self.bounding_box["top"] = int(self.input_top.get())
    self.bounding_box["left"] = int(self.input_left.get())

    self.create_image()
    self.image_view.update(self.get_path())

  def _save(self):
    self._retake()
    self._save_bounding_box()

  def _reset(self):
    self._init_bounding_box()
    self._update()
    self._retake()

  def _event_loop_hook(self, event, values):
    if(event == "__RETAKE__"):
      self._retake()
    elif(event == "__SAVE__"):
      self._save()
    elif(event == "__RESET__"):
      self._reset()

    return False