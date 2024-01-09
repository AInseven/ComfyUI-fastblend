import torch
import comfy.utils


class MaskListcaptoBatch:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "mask": ("MASK",),
            },
            "optional": {
                "load_cap": ("INT", {"default": -1, "min": -1}),
            }
        }

    INPUT_IS_LIST = True

    RETURN_TYPES = ("MASK",)
    FUNCTION = "doit"

    CATEGORY = "AInseven"

    def doit(self, mask, load_cap):
        print('type load cap:', type(load_cap))
        print('load_cap:', load_cap)
        if isinstance(load_cap, int):
            # Single int number, do nothing
            pass
        elif isinstance(load_cap, list):
            # If it's a list, set load_cap to its first element
            load_cap = load_cap[0] if len(load_cap) > 0 else -1
        else:
            # Handle other cases if needed
            raise ValueError("Invalid type for load_cap")

        if len(mask) == 1:
            if len(mask[0].shape) == 2:
                mask = mask[0].unsqueeze(0)
            return (mask,)
        elif len(mask) > 1:
            mask1 = mask[0]
            if len(mask1.shape) == 2:
                mask1 = mask1.unsqueeze(0)

            for mask2 in mask[1:]:
                if len(mask2.shape) == 2:
                    mask2 = mask2.unsqueeze(0)
                if mask1.shape[1:] != mask2.shape[1:]:
                    mask2 = comfy.utils.common_upscale(mask2.movedim(-1, 1), mask1.shape[2], mask1.shape[1], "bilinear",
                                                       "center").movedim(1, -1)
                mask1 = torch.cat((mask1, mask2), dim=0)

            # Cap the output if load_cap is provided

            if load_cap >= 0:
                mask1 = mask1[:load_cap]

            return (mask1,)
        else:
            empty_mask = torch.zeros((64, 64), dtype=torch.float32, device="cpu").unsqueeze(0)
            return (empty_mask,)
