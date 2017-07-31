from uncropped import Video
import os, sys,fnmatch
from skimage import io

SOURCE_PATH = sys.argv[1]
SOURCE_EXTS = sys.argv[2]
TARGET_PATH = sys.argv[3]

FACE_PREDICTOR_PATH = sys.argv[4]


def find_files(directory, pattern):
    for root, dirs, files in os.walk(directory):
        for basename in files:
            if fnmatch.fnmatch(basename, pattern):
                filename = os.path.join(root, basename)
                yield filename

for filepath in find_files(SOURCE_PATH, SOURCE_EXTS):
    print ("Processing: {}".format(filepath))
    video = Video(vtype='mouth', face_predictor_path=FACE_PREDICTOR_PATH).from_video(filepath)
 
    filepath_wo_ext = os.path.splitext(filepath)[0]

    target_dir = os.path.join(TARGET_PATH, filepath_wo_ext)
    os.makedirs(target_dir)

    i = 0
    for frame in video.face:
    	io.imsave(os.path.join(target_dir, "mouth_{0:03d}.png".format(i)), frame)
    	i += 1