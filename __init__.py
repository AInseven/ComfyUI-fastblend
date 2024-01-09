import os
import torch

print('torch version----------------------', torch.__version__)
import subprocess
import sys


def install_package(package_name):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])


package_list = ["imageio", "cupy", "imageio_ffmpeg", 'cv2']  # Replace with your list of packages
install_name = ['imageio', 'cupy-cuda12x', 'imageio[ffmpeg]', 'opencv-python-headless']

for package,name in zip(package_list,install_name):
    try:
        __import__(package)
    except ImportError:
        install_package(name)

from .masknumcap import MaskListcaptoBatch
from .myopenpose import MyOpenPoseNode
from .filldarkmask import FillDarkMask
from .interpolatekeyframe import InterpolateKeyFrame
from .smoothVideo import SmoothVideo
from .rebatchimage import reBatchImage

NODE_CLASS_MAPPINGS = {
    "MaskListcaptoBatch": MaskListcaptoBatch,
    "MyOpenPoseNode": MyOpenPoseNode,
    "FillDarkMask": FillDarkMask,
    "InterpolateKeyFrame": InterpolateKeyFrame,
    "SmoothVideo": SmoothVideo,
    "reBatchImage": reBatchImage,
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "MaskListcaptoBatch": "Mask List cap toBatch",
    "MyOpenPoseNode": "My OpenPose Node",
    "FillDarkMask": "Fill Dark Mask",
    "InterpolateKeyFrame": "Interpolate KeyFrame",
    "SmoothVideo": "Smooth Video",
    "reBatchImage": "reBatch Image",
}
