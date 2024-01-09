import numpy as np
import torch


class MyOpenPoseNode:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):

        return {
            "required": {
                "DWPose": ("IMAGE",),
                "OpenPose": ("IMAGE",),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    # RETURN_NAMES = ("output_image",)

    FUNCTION = "add_images"

    CATEGORY = "AInseven"

    def hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip("#")
        return [int(hex_color[i:i + 2], 16) for i in (0, 2, 4)]

    def remove_color(self, image, hex_color="#000099"):
        target_rgb = self.hex_to_rgb(hex_color)

        # Convert PyTorch tensor to NumPy array
        if isinstance(image, torch.Tensor):
            image = image.cpu().numpy()

        # Convert the target color to the same scale as the image
        target_rgb_normalized = [c / 255.0 for c in target_rgb]

        # Apply the color removal with a tolerance for small differences
        tolerance = 0.01
        mask = np.all(np.abs(image - target_rgb_normalized) < tolerance, axis=-1)
        image[mask] = 0

        # Convert back to PyTorch tensor
        image = torch.from_numpy(image)

        return image

    def reserve_color(self, image, reserved_colors=["#000099", "#00FF00"]):
        # Convert PyTorch tensor to NumPy array
        if isinstance(image, torch.Tensor):
            image = image.cpu().numpy()

        # Convert the reserved colors to the same scale as the image
        reserved_colors_normalized = []
        for each in reserved_colors:
            target_rgb = self.hex_to_rgb(each)
            reserved_colors_normalized.append([c / 255.0 for c in target_rgb])

        # Create a mask to reserve specified colors
        mask = None
        for color_normalized in reserved_colors_normalized:
            color_mask = np.all(np.abs(image - color_normalized) < 0.01, axis=-1)
            if mask is None:
                mask = color_mask
            else:
                mask |= color_mask

        # Set non-reserved colors to zero
        image[~mask] = 0

        # Convert back to PyTorch tensor
        image = torch.from_numpy(image)

        return image

    # def remove_color(self, image, hex_color="#000099"):
    #     target_rgb = self.hex_to_rgb(hex_color)
    #
    #     # Convert PyTorch tensor to NumPy array
    #     if isinstance(image, torch.Tensor):
    #         image = image.cpu().numpy()
    #
    #     # Convert the target color to the same scale as the image
    #     target_rgb_normalized = [c / 255.0 for c in target_rgb]
    #
    #     # Apply the color removal with a tolerance for small differences
    #     tolerance = 0.01
    #     mask = np.all(np.abs(image - target_rgb_normalized) < tolerance, axis=-1)
    #
    #     # Set non-reserved colors to zero for each image in the batch
    #     image[:, :, :, :][mask] = 0
    #
    #     # Convert back to PyTorch tensor
    #     image = torch.from_numpy(image)
    #
    #     return image
    #
    # def reserve_color(self, image, reserved_colors=["#000099", "#00FF00"]):
    #     # Convert PyTorch tensor to NumPy array
    #     if isinstance(image, torch.Tensor):
    #         image = image.cpu().numpy()
    #
    #     # Convert the reserved colors to the same scale as the image
    #     reserved_colors_normalized = []
    #     for each in reserved_colors:
    #         target_rgb = self.hex_to_rgb(each)
    #         reserved_colors_normalized.append([c / 255.0 for c in target_rgb])
    #
    #     # Create a mask to reserve specified colors
    #     mask = None
    #     for color_normalized in reserved_colors_normalized:
    #         color_mask = np.all(np.abs(image - color_normalized) < 0.01, axis=-1)
    #         if mask is None:
    #             mask = color_mask
    #         else:
    #             mask |= color_mask
    #
    #     # Set non-reserved colors to zero for each image in the batch
    #     image[:, :, :, :][~mask] = 0
    #
    #     # Convert back to PyTorch tensor
    #     image = torch.from_numpy(image)
    #
    #     return image

    def add_images(self, DWPose, OpenPose):
        print("type(DWPose)",type(DWPose))
        print("DWPose shape",DWPose.shape)
        # Remove the color #000099 from the input images
        dwpose_color_to_remove = ['#000099', '#990066', '#990099',  # 三条线
                                  '#aa00ff', '#ff0000', '#ff00aa', '#ff00ff', '#ff0055',
                                  '#660099', '#330099']
        for each in dwpose_color_to_remove:
            DWPose = self.remove_color(DWPose, hex_color=each)

        OpenPose = self.reserve_color(OpenPose, reserved_colors=['#ff0055', '#ff00aa',
                                                                 '#ffffff',
                                                                 '#000099','#660099','#330099','#990099','#990066'
                                                                 '#ff00aa','#ff0000','#ff0055'])

        # Add the numpy arrays of the input images
        result_image = np.add(DWPose, OpenPose)
        return (result_image,)


# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique



