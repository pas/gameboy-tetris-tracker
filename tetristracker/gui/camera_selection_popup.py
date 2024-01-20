import csv
from pathlib import Path
import PySimpleGUI as sg

from tetristracker.capturer.interceptor_capturer import InterceptorCapturer
from tetristracker.capturer.obs_virtual_cam_capturer import OBSVirtualCamCapturer
from tetristracker.gui.window import Window


class SelectCameraPopupWindow(Window):
  def __init__(self, master_window, use_case="interceptor"):
    """
    use_case should be either interceptor or obs
    """
    self.use_case = use_case
    self.master_window = master_window
    self._reset()

  def set_use_case(self, use_case):
    self.use_case = use_case

  def _reset(self):
    if self.use_case == "obs_virtual_cam":
      self.capturer = OBSVirtualCamCapturer(bounding_box=[])
    else:
      self.capturer = InterceptorCapturer()

  def name(self):
    return "Select camera"

  def finalize(self):
    return True

  def modal(self):
    return True

  def layout(self):
    elements = []
    for value in self.capturer.working_values:
      unique_name = str(value[0]) + value[2]
      elements.append(sg.Button(unique_name, image_filename=self.capturer.get_image_path(value),  key="_" + unique_name.upper() + "_"))

    return [
      elements
    ]

  def _window_close_hook(self):
    self.capturer.close()

  def _event_loop_hook(self, event, values):
    leave_event_loop = False

    print(event)

    return leave_event_loop