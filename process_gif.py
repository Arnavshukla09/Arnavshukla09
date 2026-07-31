from PIL import Image, ImageSequence
import numpy as np
import sys

def process_gif(input_path, output_path):
    im = Image.open(input_path)
    duration = im.info.get('duration', 100)
    
    frames = []
    for frame in ImageSequence.Iterator(im):
        # Convert to RGB
        frame_rgb = frame.convert("RGB")
        data = np.array(frame_rgb, dtype=np.float32)
        
        # Calculate grayscale intensity (c from 0 to 255)
        # Using average of R, G, B since it's likely grayscale
        c = np.mean(data, axis=2)
        factor = c / 255.0
        
        # New background: (13, 17, 23)
        # New logo: (255, 255, 255)
        # new_c = factor * background + (1-factor) * logo
        
        r_new = factor * 13 + (1 - factor) * 255
        g_new = factor * 17 + (1 - factor) * 255
        b_new = factor * 23 + (1 - factor) * 255
        
        new_data = np.zeros_like(data, dtype=np.uint8)
        new_data[..., 0] = r_new.astype(np.uint8)
        new_data[..., 1] = g_new.astype(np.uint8)
        new_data[..., 2] = b_new.astype(np.uint8)
        
        frames.append(Image.fromarray(new_data))
        
    frames[0].save(output_path, save_all=True, append_images=frames[1:], optimize=False, duration=duration, loop=0)
    print("Saved to", output_path)

if __name__ == "__main__":
    process_gif('temp.gif', 'assets/custom_laptop.gif')
