import torch

class FillDarkMask:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "masks": ("MASK",),
            },
        }

    RETURN_TYPES = ("MASK",)

    FUNCTION = "execute"
    CATEGORY = "AInseven"

    def execute(self, masks):
        print("type(masks):", type(masks), masks.shape)
        prev_mask = masks[0]
        modified_masks = [prev_mask]
        num = 0
        for mask in masks[1:]:
            if torch.min(mask) == torch.max(mask) == 0:
                # If the mask is totally black, set its value to the previous mask
                num += 1
                mask = prev_mask.clone()
            modified_masks.append(mask)
            prev_mask = mask
        print('found dark mask numbers:', num)

        return (torch.stack(modified_masks),)
