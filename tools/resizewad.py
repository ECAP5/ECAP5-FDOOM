import os
from PIL import Image

def resize_by_half(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.png', '.bmp')):
            path = os.path.join(input_folder, filename)
            with Image.open(path) as img:
                # Calculate new size (Divide by 2)
                new_width = max(1, img.width // 2)
                new_height = max(1, img.height // 2)

                # Convert to RGB then resize without smoothing (Nearest Neighbor)
                img = img.convert("RGB")
                img = img.resize((new_width, new_height), Image.NEAREST)

                # Final conversion to 8-bit Palette
                img = img.convert("P", palette=Image.ADAPTIVE, colors=256)

                output_path = os.path.join(output_folder, filename)
                img.save(output_path, "PNG", optimize=True)

                print(f"{filename:15} : Original {img.width * 2}x{img.height * 2} -> New {new_width}x{new_height}")

if __name__ == "__main__":
    # Example usage: resize_by_half("input_dir", "output_dir")
    resize_by_half("graphics_original", "graphics")
