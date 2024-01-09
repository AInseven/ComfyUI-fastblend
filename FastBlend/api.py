from .runners import AccurateModeRunner, FastModeRunner, BalancedModeRunner, InterpolationModeRunner, \
    InterpolationModeSingleFrameRunner
from .data import VideoData, get_video_fps, save_video, search_for_images
import os



def check_input_for_blending(video_guide, video_guide_folder, video_style, video_style_folder):
    frames_guide = VideoData(video_guide, video_guide_folder)
    frames_style = VideoData(video_style, video_style_folder)
    message = ""
    if len(frames_guide) < len(frames_style):
        message += f"The number of frames mismatches. Only the first {len(frames_guide)} frames of style video will be used.\n"
        frames_style.set_length(len(frames_guide))
    elif len(frames_guide) > len(frames_style):
        message += f"The number of frames mismatches. Only the first {len(frames_style)} frames of guide video will be used.\n"
        frames_guide.set_length(len(frames_style))
    height_guide, width_guide = frames_guide.shape()
    height_style, width_style = frames_style.shape()
    if height_guide != height_style or width_guide != width_style:
        message += f"The shape of frames mismatches. The frames in style video will be resized to (height: {height_guide}, width: {width_guide})\n"
        frames_style.set_shape(height_guide, width_guide)
    return frames_guide, frames_style, message


def smooth_video(
        video_guide,
        video_guide_folder,
        video_style,
        video_style_folder,
        mode,
        window_size,
        batch_size,
        tracking_window_size,
        output_path,
        fps,
        minimum_patch_size,
        num_iter,
        guide_weight,
        initialize,
        progress=None,
):
    # input
    frames_guide, frames_style, message = check_input_for_blending(video_guide, video_guide_folder, video_style,
                                                                   video_style_folder)
    if len(message) > 0:
        print(message)
    # output
    # if output_path == "":
    #     if video_style is None:
    #         output_path = os.path.join(video_style_folder, "output")
    #     else:
    #         output_path = os.path.join(os.path.split(video_style)[0], "output")
    #     os.makedirs(output_path, exist_ok=True)
    #     print("No valid output_path. Your video will be saved here:", output_path)
    # elif not os.path.exists(output_path):
    #     os.makedirs(output_path, exist_ok=True)
    #     print("Your video will be saved here:", output_path)
    # frames_path = os.path.join(output_path, "frames")
    # video_path = os.path.join(output_path, "video.mp4")
    # os.makedirs(frames_path, exist_ok=True)
    # process
    if mode == "Fast" or mode == "Balanced":
        tracking_window_size = 0
    ebsynth_config = {
        "minimum_patch_size": minimum_patch_size,
        "threads_per_block": 8,
        "num_iter": num_iter,
        "gpu_id": 0,
        "guide_weight": guide_weight,
        "initialize": initialize,
        "tracking_window_size": tracking_window_size,
    }
    if mode == "Fast":
        frames=FastModeRunner().run(frames_guide, frames_style, batch_size=batch_size, window_size=window_size,
                             ebsynth_config=ebsynth_config, save_path=None)
    elif mode == "Balanced":
        frames=BalancedModeRunner().run(frames_guide, frames_style, batch_size=batch_size, window_size=window_size,
                                 ebsynth_config=ebsynth_config, save_path=None)
    elif mode == "Accurate":
        frames=AccurateModeRunner().run(frames_guide, frames_style, batch_size=batch_size, window_size=window_size,
                                 ebsynth_config=ebsynth_config, save_path=None)
    # output
    # try:
    #     fps = int(fps)
    # except:
    #     fps = get_video_fps(video_style) if video_style is not None else 30
    # print("Fps:", fps)
    # print("Saving video...")
    # video_path = save_video(frames_path, video_path, num_frames=len(frames_style), fps=fps)
    # print("Success!")
    # print("Your frames are here:", frames_path)
    # print("Your video is here:", video_path)
    return frames


class KeyFrameMatcher:
    def __init__(self):
        pass

    def extract_number_from_filename(self, file_name):
        result = []
        number = -1
        for i in file_name:
            if ord(i) >= ord("0") and ord(i) <= ord("9"):
                if number == -1:
                    number = 0
                number = number * 10 + ord(i) - ord("0")
            else:
                if number != -1:
                    result.append(number)
                    number = -1
        if number != -1:
            result.append(number)
        result = tuple(result)
        return result

    def extract_number_from_filenames(self, file_names):
        numbers = [self.extract_number_from_filename(file_name) for file_name in file_names]
        min_length = min(len(i) for i in numbers)
        for i in range(min_length - 1, -1, -1):
            if len(set(number[i] for number in numbers)) == len(file_names):
                return [number[i] for number in numbers]
        return list(range(len(file_names)))

    def match_using_filename(self, file_names_a, file_names_b):
        file_names_b_set = set(file_names_b)
        matched_file_name = []
        for file_name in file_names_a:
            if file_name not in file_names_b_set:
                matched_file_name.append(None)
            else:
                matched_file_name.append(file_name)
        return matched_file_name

    def match_using_numbers(self, file_names_a, file_names_b):
        numbers_a = self.extract_number_from_filenames(file_names_a)
        numbers_b = self.extract_number_from_filenames(file_names_b)
        numbers_b_dict = {number: file_name for number, file_name in zip(numbers_b, file_names_b)}
        matched_file_name = []
        for number in numbers_a:
            if number in numbers_b_dict:
                matched_file_name.append(numbers_b_dict[number])
            else:
                matched_file_name.append(None)
        return matched_file_name

    def match_filenames(self, file_names_a, file_names_b):
        matched_file_name = self.match_using_filename(file_names_a, file_names_b)
        if sum([i is not None for i in matched_file_name]) > 0:
            return matched_file_name
        matched_file_name = self.match_using_numbers(file_names_a, file_names_b)
        return matched_file_name


def detect_frames(frames_path, keyframes_path):
    if not os.path.exists(frames_path) and not os.path.exists(keyframes_path):
        return "Please input the directory of guide video and rendered frames"
    elif not os.path.exists(frames_path):
        return "Please input the directory of guide video"
    elif not os.path.exists(keyframes_path):
        return "Please input the directory of rendered frames"
    frames = [os.path.split(i)[-1] for i in search_for_images(frames_path)]
    keyframes = [os.path.split(i)[-1] for i in search_for_images(keyframes_path)]
    if len(frames) == 0:
        return f"No images detected in {frames_path}"
    if len(keyframes) == 0:
        return f"No images detected in {keyframes_path}"
    matched_keyframes = KeyFrameMatcher().match_filenames(frames, keyframes)
    max_filename_length = max([len(i) for i in frames])
    if sum([i is not None for i in matched_keyframes]) == 0:
        message = ""
        for frame, matched_keyframe in zip(frames, matched_keyframes):
            message += frame + " " * (max_filename_length - len(frame) + 1)
            message += "--> No matched keyframes\n"
    else:
        message = ""
        for frame, matched_keyframe in zip(frames, matched_keyframes):
            message += frame + " " * (max_filename_length - len(frame) + 1)
            if matched_keyframe is None:
                message += "--> [to be rendered]\n"
            else:
                message += f"--> {matched_keyframe}\n"
    return message


def check_input_for_interpolating(frames_path, keyframes_path, select_every_nth):
    # search for images
    # frames = [os.path.split(i)[-1] for i in search_for_images(frames_path)]
    # keyframes = [os.path.split(i)[-1] for i in search_for_images(keyframes_path)]
    # match frames
    # matched_keyframes = KeyFrameMatcher().match_filenames(frames, keyframes)
    # file_list = [file_name for file_name in matched_keyframes if file_name is not None]
    # index_style = [i for i, file_name in enumerate(matched_keyframes) if file_name is not None]

    index_style = [i * select_every_nth for i in range(len(keyframes_path))]
    frames_guide = VideoData(None, frames_path)
    frames_style = VideoData(None, keyframes_path)
    # match shape
    message = ""
    height_guide, width_guide = frames_guide.shape()
    height_style, width_style = frames_style.shape()
    if height_guide != height_style or width_guide != width_style:
        message += f"The shape of frames mismatches. The rendered keyframes will be resized to (height: {height_guide}, width: {width_guide})\n"
        frames_style.set_shape(height_guide, width_guide)
    return frames_guide, frames_style, index_style, message


def interpolate_video(
        frames_np_list,
        keyframes_np_list,
        select_every_nth,
        output_path,
        fps,
        batch_size,
        tracking_window_size,
        minimum_patch_size,
        num_iter,
        guide_weight,
        initialize,
        progress=None,
):
    # input
    frames_guide, frames_style, index_style, message = check_input_for_interpolating(frames_np_list, keyframes_np_list,
                                                                                     select_every_nth=select_every_nth)
    if len(message) > 0:
        print(message)
    # output
    # if output_path == "":
    #     output_path = os.path.join(keyframes_np_list, "output")
    #     os.makedirs(output_path, exist_ok=True)
    #     print("No valid output_path. Your video will be saved here:", output_path)
    # elif not os.path.exists(output_path):
    #     os.makedirs(output_path, exist_ok=True)
    #     print("Your video will be saved here:", output_path)
    # output_frames_path = os.path.join(output_path, "frames")
    # output_video_path = os.path.join(output_path, "video.mp4")
    # os.makedirs(output_frames_path, exist_ok=True)
    # process
    ebsynth_config = {
        "minimum_patch_size": minimum_patch_size,
        "threads_per_block": 8,
        "num_iter": num_iter,
        "gpu_id": 0,
        "guide_weight": guide_weight,
        "initialize": initialize,
        "tracking_window_size": tracking_window_size
    }
    if len(index_style) == 1:
        frames=InterpolationModeSingleFrameRunner().run(frames_guide, frames_style, index_style, batch_size=batch_size,
                                                 ebsynth_config=ebsynth_config, save_path=None)
    else:
        frames=InterpolationModeRunner().run(frames_guide, frames_style, index_style, batch_size=batch_size,
                                      ebsynth_config=ebsynth_config, save_path=None)
    # try:
    #     fps = int(fps)
    # except:
    #     fps = 30
    # print("Fps:", fps)
    # print("Saving video...")
    # video_path = save_video(output_frames_path, output_video_path, num_frames=len(frames_guide), fps=fps)
    # print("Success!")
    # print("Your frames are here:", output_frames_path)
    # print("Your video is here:", video_path)
    # return output_path, fps, video_path
    return frames



