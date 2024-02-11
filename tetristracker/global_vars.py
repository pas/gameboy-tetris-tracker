from queue import Queue

"""
  Queue where the capturer stores at most 120 images
  and the ... gets them
"""
# TODO: Handle cases when queue gets overfull!
images_queue = Queue(maxsize=4)
"""
Queue where the ... stores the playfield
and the analysis module gets them.
"""
gameboyview_queue = Queue(maxsize=4)
