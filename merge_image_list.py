import torch


class Merge_Image_List:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
            "images": ("IMAGE",),
        }
        }

    INPUT_IS_LIST = True

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "doit"

    CATEGORY = "AInseven"

    def doit(self, images):
        print('Merge_Image_List input data type:', type(images), 'length:',len(images))
        if len(images) <= 1:
            return (images,)
        else:
            merged_batch = torch.cat(images, dim=0)

            # Check the shape of the merged batch
            print("Merge_Image_List output data shape:", merged_batch.shape, merged_batch.dtype)
            return (merged_batch,)
