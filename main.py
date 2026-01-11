try:
    import cv2, os, sys
except:
    import os
    print("missing dependencies, installing...")
    os.system("pip install -r requirements.txt")

print("video-thumbnail-tool v0.1 by 3pm")

def tv():
    thumbnail_path = "input.jpg"
    video_path = "input.mp4"
    if len(sys.argv) < 3:
        print("usage: python main.py [-fc, --frame-copy] [input thumbnail path] [input video path]")
    else:
        thumbnail_path = sys.argv[1]
        video_path = sys.argv[2]
    print("getting video framerate/resolution...")
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    print(f"video framerate: {round(fps)}fps\nvideo resolution: {int(width)}x{int(height)}")
    print("appending frame to video...")
    os.system(
        f'ffmpeg -loop 1 -framerate {round(fps)} -t {1/fps} -i {thumbnail_path} '
        f'-i {video_path} '
        f'-filter_complex "[0:v]scale={int(width)}:{int(height)},setsar=1[v0];'
        f'[v0][1:v]concat=n=2:v=1:a=0[v]" '
        f'-map "[v]" -map 1:a? output.mp4'
    )
    print("done! output saved as output.mp4")

def fc():
    video1_path = "input1.mp4"
    video2_path = "input2.mp4"
    if len(sys.argv) < 3:
        print("usage: python main.py [-fc, --frame-copy] [input video path to copy] [input video path to paste]")
    else:
        video1_path = sys.argv[2]
        video2_path = sys.argv[3]
    print("getting video framerate/resolution...")
    cap = cv2.VideoCapture(video2_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    print(f"video framerate: {round(fps)}fps\nvideo resolution: {int(width)}x{int(height)}")
    print("getting first frame of video to copy...")
    cap = cv2.VideoCapture(video1_path)
    ret, frame = cap.read()
    if not ret:
        print("failed to read frame from video 1")
        return
    cv2.imwrite("temp_frame.jpg", frame)
    print("appending frame to video...")
    os.system(
        f'ffmpeg -loop 1 -framerate {round(fps)} -t {1/fps} -i temp_frame.jpg '
        f'-i {video2_path} '
        f'-filter_complex "[0:v]scale={int(width)}:{int(height)},setsar=1[v0];'
        f'[v0][1:v]concat=n=2:v=1:a=0[v]" '
        f'-map "[v]" -map 1:a? output.mp4'
    )
    os.remove("temp_frame.jpg")
    print("done! output saved as output.mp4")

def ar():
    audio_path = "input.mp3"
    video_path = "input.mp4"
    if len(sys.argv) < 3:
        print("usage: python main.py [-ar, --audio-replace] [input audio path] [input video path]")
    else:
        audio_path = sys.argv[2]
        video_path = sys.argv[3]
    print("appending audio to video...")
    os.system(f'ffmpeg -i {video_path} -i {audio_path} -c:v copy -c:a aac -shortest -map 0:v -map 1:a output.mp4')
    print("done! output saved as output.mp4")

if __name__ == "__main__":
    if "-fc" in sys.argv or "--frame-copy" in sys.argv:
        fc()
    elif "-ar" in sys.argv or "--audio-replace" in sys.argv:
        ar()
    else:
        tv()