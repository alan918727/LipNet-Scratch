import numpy as np
import skvideo.io



class Video(object):
    def __init__(self, vtype='mouth', face_predictor_path=None):
        self.vtype=vtype
        self.face_predictor_path=face_predictor_path
  

    def from_video(self, path):
        frames = self.get_video_frames(path)
        self.process_frames_mouth(frames)
        return self


    def process_frames_mouth(self, frames):
        self.face = np.array(frames)
        self.mouth = np.array(frames)
        


    def get_video_frames(self, path):
        videogen = skvideo.io.vreader(path)
        frames = np.array([frame for frame in videogen])
        return frames
