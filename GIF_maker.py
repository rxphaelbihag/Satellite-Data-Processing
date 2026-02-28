import glob
from PIL import Image
def make_gif(frame_folder):
    frames = [Image.open(image) for image in glob.glob(f"{frame_folder}/*")]
    frame_one = frames[0]
    frame_one.save("SST_Animation.gif", format="GIF", append_images=frames,
               save_all=True, duration=250, loop=0)


print("Making GIF")
make_gif("images2\SST")
print("DONE GIF")