import csv
from pathlib import Path
import PySimpleGUI as sg

from tetristracker.capturer.camera_detector import CameraDetector
from tetristracker.gui.window import Window

class Values():
  def __init__(self, index, api):
    self.index = index
    self.api = api

class SelectCameraPopupWindow(Window):
  def __init__(self, master_window, config, use_case="interceptor"):
    """
    This shows the user images produced by
    the various available cameras. Sets the camera index
    in config for the specified use case when the
    user clicks on one of the images.

    use_case should be either interceptor or obs
    """
    self.use_case = use_case
    self.master_window = master_window
    self.config = config
    self.detector = CameraDetector()

  def set_use_case(self, use_case):
    self.use_case = use_case

  def name(self):
    return "Select camera"

  def finalize(self):
    return True

  def modal(self):
    return True

  def layout(self):
    elements = []
    # retrieve values from temp directory created by the capturdatector
    for value in self.detector.working_values:
      unique_name = str(value[0]) + value[2]
      elements.append(sg.Button(unique_name, image_filename=self.detector.get_image_path(value), key=Values(value[0], value[1])))

    return [
      elements
    ]

  def _window_close_hook(self):
    # This removes the temp files
    self.detector.close()

  def _event_loop_hook(self, event, values):
    leave_event_loop = True
    print(event.api)
    print(event.index)

    if self.use_case == "interceptor":
      self.config.set_interceptor_camera(event.index, event.api)
    elif self.use_case == "obs":
      self.config.set_obs_camera(event.index, event.api)
    else:
      print("Could not set any camera!")

    return leave_event_loop