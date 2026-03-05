import os
import PIL.Image
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, vfx
from moviepy.config import change_settings

# 1. FIX THE PIL ERROR FOR PYTHON 3.14
if not hasattr(PIL.Image, 'ANTIALIAS'):
    PIL.Image.ANTIALIAS = PIL.Image.LANCZOS

# 2. LINK IMAGEMAGICK (Update this path to your exact version if needed!)
change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.2-Q16-HDRI\magick.exe"})

# 3. SETTINGS
input_video = "OmniSuite_Demo.mp4" # Your current file
output_video = "OmniSuite_Pro_2Min_Scripted.mp4"
target_duration = 120  # Exactly 2 minutes

# 4. YOUR FULL SCRIPT (Paste the entire thing between the triple quotes)
full_script = """
Welcome to OmniSuite Pro: The Last Assistant You'll Ever Need.
Our 6-Core Engine integrates OmniCore, OmniMirror, and OmniFinancial.
Experience autonomous business intelligence that works 24/7.
Scaling your business across Whatnot, eBay, and beyond.
OmniSuite Pro is not just software; it's your digital twin.
"""

# 5. LOAD AND PREP VIDEO
if not os.path.exists(input_video):
    print(f"Error: {input_video} not found!")
else:
    clip = VideoFileClip(input_video)
    
    # Loop the video until it reaches 2 minutes
    loops = int(target_duration / clip.duration) + 1
    extended_video = clip.loop(n=loops).subclip(0, target_duration)

    # 6. CREATE THE SCRIPT OVERLAY
    # 'caption' method handles long text by wrapping it automatically
    txt_clip = TextClip(full_script, fontsize=45, color='white', font='Arial-Bold',
                        method='caption', size=(extended_video.w * 0.8, None))
    
    # Set the text to stay on screen for the full 2 minutes
    txt_clip = txt_clip.set_pos('center').set_duration(target_duration).fadein(2)

    # 7. COMBINE AND RENDER
    final_result = CompositeVideoClip([extended_video, txt_clip])
    
    print("Starting 2-minute render for OmniSuite Pro...")
    final_result.write_videofile(output_video, fps=24, codec="libx264")
    print(f"Success! Final video saved as {output_video}")