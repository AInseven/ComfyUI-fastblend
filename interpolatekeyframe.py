from .FastBlend.api import interpolate_video

import numpy as np
import torch

class InterpolateKeyFrame:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "orginalframe": ("IMAGE",),
                "keyframe": ("IMAGE",),
                # "output_folder": ("STRING", {"default": ""}),
                "select_every_nth": ("INT", {
                    "default": 5,
                    "min": 0,  # Minimum value
                    "max": 20,  # Maximum value
                    "step": 1,  # Slider's step
                    "display": "number"  # Cosmetic only: display as "number" or "slider"
                }),
                "batch_size": ("INT", {
                    "default": 16,
                    "min": 1,  # Minimum value
                    "max": 100,  # Maximum value
                    "step": 8,  # Slider's step
                    "display": "number"  # Cosmetic only: display as "number" or "slider"
                }),
                "tracking_window_size": ("INT", {
                    "default": 1,
                    "min": 1,  # Minimum value
                    "max": 100,  # Maximum value
                    "step": 1,  # Slider's step
                    "display": "number"  # Cosmetic only: display as "number" or "slider"
                }),
                "minimum_patch_size": ("INT", {
                    "default": 15,
                    "min": 1,  # Minimum value
                    "max": 100,  # Maximum value
                    "step": 2,  # Slider's step
                    "display": "number"  # Cosmetic only: display as "number" or "slider"
                }),
                "num_iter": ("INT", {
                    "default": 5,
                    "min": 1,  # Minimum value
                    "max": 100,  # Maximum value
                    "step": 1,  # Slider's step
                    "display": "number"  # Cosmetic only: display as "number" or "slider"
                }),
                "guide_weight": ("FLOAT", {
                    "default": 10.0,
                    "min": 1,  # Minimum value
                    "max": 100,  # Maximum value
                    "step": 0.5,  # Slider's step
                    "display": "number"  # Cosmetic only: display as "number" or "slider"
                }),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    # RETURN_TYPES = ()

    FUNCTION = "execute"
    CATEGORY = "AInseven"

    def execute(self, orginalframe,keyframe,select_every_nth,batch_size,tracking_window_size,minimum_patch_size,num_iter,guide_weight):
        print("orginalframe Type:", type(orginalframe))
        print("orginalframe shape:", orginalframe.shape)
        print("orginalframe Maximum value of the first item:", torch.max(orginalframe[0]))
        print("orginalframe Minimum value of the first item:", torch.min(orginalframe[0]))
        print(orginalframe.dtype)

        print("keyframe Type:", type(keyframe))
        print("keyframe shape:", keyframe.shape)
        print("keyframe Maximum value of the first item:", torch.max(keyframe[0]))
        print("keyframe Minimum value of the first item:", torch.min(keyframe[0]))
        print(keyframe.dtype)

        orginalframe_np = (orginalframe.cpu().numpy() * 255).astype(np.uint8)
        keyframe_np = (keyframe.cpu().numpy() * 255).astype(np.uint8)

        frames=interpolate_video(
            frames_np_list = orginalframe_np,
            keyframes_np_list = keyframe_np,
            select_every_nth=select_every_nth,
            output_path = None,
            fps = None,
            batch_size = batch_size,
            tracking_window_size = tracking_window_size,
            minimum_patch_size = minimum_patch_size,
            num_iter = num_iter,
            guide_weight = guide_weight,
            initialize = "identity"
        )

        print('numpy_images = np.stack(frames)')
        numpy_images = np.stack(frames)
        print("numpy_images.shape", numpy_images.shape)

        numpy_images = numpy_images.clip(0, 255)
        normalized_images = numpy_images / 255.0

        print('torch_images = torch.from_numpy(normalized_images)')
        torch_images = torch.from_numpy(normalized_images)
        print("torch_images.shape",torch_images.shape)
        print(torch_images.dtype)


        return (torch_images.type(torch.float32),)