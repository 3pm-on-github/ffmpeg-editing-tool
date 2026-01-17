try:
    import cv2, os, sys
except:
    import os
    print("missing dependencies, installing...")
    os.system("pip install -r requirements.txt")

print("video-thumbnail-tool v0.2 by 3pm")

def st():
    thumbnail_path = "input.jpg"
    video_path = "input.mp4"
    if len(sys.argv) < 3:
        print("usage: python main.py [-st, --set-thumbnail] [input image path] [input video path]")
        return
    else:
        thumbnail_path = sys.argv[2]
        video_path = sys.argv[3]
    print("getting video framerate/resolution...")
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    print(f"video framerate: {round(fps)}fps\nvideo resolution: {int(width)}x{int(height)}")
    print("appending frame to video...")
    os.system(
        f'ffmpeg -loop 1 -framerate {round(fps)} -t {1/fps} -i "{thumbnail_path}" '
        f'-i "{video_path}" '
        f'-filter_complex '
        f'"[0:v]scale={int(width)}:{int(height)},setsar=1[v0];'
        f'[1:v]setsar=1[v1];'
        f'[v0][v1]concat=n=2:v=1:a=0[v]" '
        f'-map "[v]" -map 1:a? -c:v libx264 -pix_fmt yuv420p output.mp4'
    )
    print("done! output saved as output.mp4")

def fc():
    video1_path = "input1.mp4"
    video2_path = "input2.mp4"
    if len(sys.argv) < 3:
        print("usage: python main.py [-fc, --frame-copy] [input video path to copy] [input video path to paste]")
        return
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
        return
    else:
        audio_path = sys.argv[2]
        video_path = sys.argv[3]
    print("replacing audio from video...")
    os.system(f'ffmpeg -i {video_path} -i {audio_path} -c:v copy -c:a aac -shortest -map 0:v -map 1:a output.mp4')
    print("done! output saved as output.mp4")

def aa():
    audio_path = "input.mp3"
    video_path = "input.mp4"
    if len(sys.argv) < 3:
        print("usage: python main.py [-aa, --audio-append] [input audio path] [input video path]")
        return
    else:
        audio_path = sys.argv[2]
        video_path = sys.argv[3]
    print("appending audio to video...")
    os.system(f'ffmpeg -i {video_path} -i {audio_path} -filter_complex "[0:a][1:a]amix=inputs=2:duration=shortest[a]" -c:v copy -c:a aac -map 0:v -map "[a]" output.mp4')
    print("done! output saved as output.mp4")

def i2v():
    image_path = "input.jpg"
    video_len = 5
    if len(sys.argv) < 3:
        print("usage: python main.py [-i2v, --image-to-video] [input image path] [video length in seconds]")
        return
    else:
        image_path = sys.argv[2]
        video_len = float(sys.argv[3])
    print("converting image to video...")
    os.system(f'ffmpeg -loop 1 -i {image_path} -vf scale=trunc(iw/2)*2:trunc(ih/2)*2 -c:v libx264 -t {video_len} -pix_fmt yuv420p output.mp4')
    print("done! output saved as output.mp4")

def fb():
    video_path = "input.mp4"
    flashbang_duration = 2
    if len(sys.argv) < 3:
        print("usage: python main.py [-fb, --flashbang] [input video path] [flashbang duration in seconds]")
        return
    else:
        video_path = sys.argv[2]
        flashbang_duration = float(sys.argv[3])
    print("getting video framerate/resolution...")
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    print(f"video framerate: {round(fps)}fps\nvideo resolution: {int(width)}x{int(height)}")
    print("adding flashbang effect to video...")
    os.system(
        f'ffmpeg -f lavfi -i color=white@1:s={int(width)}x{int(height)}:r={round(fps)}:d={flashbang_duration} '
        f'-i {video_path} '
        f'-filter_complex "[0:v]fade=out:st=0:d={flashbang_duration}:alpha=1[white];[1:v][white]overlay=format=auto[final]" '
        f'-map "[final]" -map 1:a? -c:a copy output.mp4'
    )
    print("done! output saved as output.mp4")

if __name__ == "__main__":
    if "-st" in sys.argv or "--set-thumbnail" in sys.argv:
        st()
    elif "-fc" in sys.argv or "--frame-copy" in sys.argv:
        fc()
    elif "-ar" in sys.argv or "--audio-replace" in sys.argv:
        ar()
    elif "-aa" in sys.argv or "--audio-append" in sys.argv:
        aa()
    elif "-i2v" in sys.argv or "--image-to-video" in sys.argv:
        i2v()
    elif "-fb" in sys.argv or "--flashbang" in sys.argv:
        fb()
    else:
        print("usage: python main.py [-st, --set-thumbnail, -fc, --frame-copy, -ar, --audio-replace, -aa, --audio-append, -i2v, --image-to-video, -fb, --flashbang]")