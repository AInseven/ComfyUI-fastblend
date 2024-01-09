import torch


class reBatchImage:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "batch_size": (
                    "INT", {
                        "default": 5,
                        "min": 0,  # Minimum value
                        "max": 100,  # Maximum value
                        "step": 1,  # Slider's step
                        "display": "number"  # Cosmetic only: display as "number" or "slider"
                    }),
            },

        }

    RETURN_TYPES = ("IMAGE",)
    OUTPUT_IS_LIST = (True,)
    FUNCTION = "doit"

    CATEGORY = "AInseven"

    def doit(self, image, batch_size):
        splits_tuple = torch.split(image, split_size_or_sections=batch_size, dim=0)
        images = list(splits_tuple)
        return (images,)
