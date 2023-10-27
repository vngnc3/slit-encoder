# Slit animation encoder: Encodes input image sequence into a single image output containing all the animation frames to be used with the generated slit pattern.
from PIL import Image, ImageDraw
from tqdm import tqdm 
import numpy as np
import os


# Updated full code with requested features
input_directory = "./input/"
output_directory = "./output/"
n_slits = 120 # Total animation frames must be a factor of n_slits
debug_mode = False  # Dump all slit patterns when True, only the first when False
horizontal_mode = False  # Generate slit patterns horizontally when True

# Make sure the input and output directories exist
if not os.path.exists(input_directory):
    os.makedirs(input_directory)

if not os.path.exists(output_directory):
    os.makedirs(output_directory)

def load_animation_sequence(input_directory):
    animation_info = {"dimensions": None, "frame_count": 0, "frame_files": []}
    for root, dirs, files in os.walk(input_directory):
        for file in files:
            if file.lower().endswith((".png", ".jpg", ".jpeg", ".tif", ".tiff")):
                animation_info["frame_files"].append(os.path.join(root, file))
    animation_info["frame_files"].sort()
    if animation_info["frame_files"]:
        with Image.open(animation_info["frame_files"][0]) as img:
            animation_info["dimensions"] = img.size
    animation_info["frame_count"] = len(animation_info["frame_files"])
    return animation_info

def generate_slit_pattern(num_slits, dimensions, frame_number, total_frames, output_directory):
    canvas = Image.new("RGBA", dimensions, color=(0, 0, 0, 255))
    draw = ImageDraw.Draw(canvas)
    width, height = dimensions if not horizontal_mode else reversed(dimensions)
    loop_width_exact = width / num_slits
    loop_width = int(loop_width_exact)
    error = width - (loop_width * num_slits)
    x_start = 0
    for _ in range(num_slits):
        slots = [1] * total_frames
        slots[frame_number] = 0
        slot_width = loop_width // total_frames
        x_slot_start = x_start
        for slot in slots:
            x_slot_end = x_slot_start + slot_width
            rect_coords = [(x_slot_start, 0), (x_slot_end, height)] if not horizontal_mode else [(0, x_slot_start), (height, x_slot_end)]
            draw.rectangle(rect_coords, fill=(0, 0, 0, slot * 255))
            x_slot_start = x_slot_end
        x_start += loop_width
    if error > 0:
        x_error_start = width - error
        slots = [1] * total_frames
        slots[frame_number] = 0
        slot_width = error // total_frames
        x_slot_start = x_error_start
        for slot in slots:
            x_slot_end = x_slot_start + slot_width
            rect_coords = [(x_slot_start, 0), (x_slot_end, height)] if not horizontal_mode else [(0, x_slot_start), (height, x_slot_end)]
            draw.rectangle(rect_coords, fill=(0, 0, 0, slot * 255))
            x_slot_start = x_slot_end
    if debug_mode or frame_number == 0:
        output_path = os.path.join(output_directory, f"slit_mask_frame_{frame_number}.png")
        canvas.save(output_path)
    return canvas

def create_final_canvas(anim_seq_info, num_slits, output_directory):
    dimensions = anim_seq_info["dimensions"]
    final_canvas_array = np.zeros((dimensions[1], dimensions[0], 4), dtype=np.uint8)
    for frame_number in tqdm(range(anim_seq_info["frame_count"]), desc="Processing frames"):
        slit_pattern = generate_slit_pattern(
            num_slits,
            dimensions,
            frame_number,
            anim_seq_info["frame_count"],
            output_directory,
        )
        slit_pattern_array = np.array(slit_pattern)
        with Image.open(anim_seq_info["frame_files"][frame_number]) as frame:
            frame_array = np.array(frame.convert("RGBA"))
        alpha_channel = slit_pattern_array[:, :, 3] / 255.0
        alpha_channel = alpha_channel[:, :, np.newaxis]
        final_canvas_array = np.where(alpha_channel == 0, frame_array, final_canvas_array)
    final_canvas = Image.fromarray(final_canvas_array, "RGBA")
    output_path = os.path.join(output_directory, "final_canvas.png")
    final_canvas.save(output_path)
    print("Completed! Final canvas saved.")
    return final_canvas

# Test the functions (this part is specific to your testing setup)
anim_seq_info = load_animation_sequence(input_directory)
final_canvas = create_final_canvas(anim_seq_info, n_slits, output_directory)
print(anim_seq_info)