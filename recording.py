from moviepy.editor import ImageSequenceClip

with open('frames/frame_count.txt', 'r') as f:
    frame_count = int(f.read())

frame_files = [f"frames/frame_{i:04d}.png" for i in range(frame_count)]
clip = ImageSequenceClip(frame_files, fps=30)
clip.write_videofile("game_recording.mp4", codec="libx264")