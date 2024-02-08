import cv2 as cv2

class SimpleCameraCapturer:
  def __init__(self, index, api):
    self.cap = None
    self.index = index
    self.api = api
    self.set_camera()

  def set_camera(self):
    # TODO: Error handling!
    self.release()

    print("selected camera:")
    print(self.index)
    print(self.api)
    self.cap = cv2.VideoCapture(self.index)

  def release(self):
    if(self.cap != None):
      self.cap.release()

  def grab_image(self, enhancement=True):
    ret = False
    tries = 0
    while not (ret or tries > 100):
      """
      It sometimes happens that no image can be fetched
      we just try again if this happens
      """
      ret, image = self.cap.read()
      tries += 1

    if not ret:
      raise RuntimeError("Could not fetch image from camera")

    return image

  def close(self):
    self.temp_dir.cleanup()



