# video-thumbnail-tool
a tool used to modify videos. uses ffmpeg, opencv and python.<br>
## how to use
you can run video-thumbnail-tool by running this command: `python main.py [-st, --set-thumbnail, -fc, --frame-copy, -ar, --audio-replace, -aa, --audio-append, -i2v, --image-to-video]`<br>
--set-thumbnail, -st: sets a video's first frame to an image. usage: `python main.py [-st, --set-thumbnail] [input image path] [input video path]`
--frame-copy, -fc: copies the first frame from a video to another. usage: `python main.py [-fc, --frame-copy] [input video path to copy] [input video path to paste]`<br>
--audio-replace, -ar: replaces the video's audio. usage: `python main.py [-ar, --audio-replace] [input audio path] [input video path]`<br>
--audio-append, -aa: appends an audio to the video's audio. usage: `python main.py [-aa, --audio-append] [input audio path] [input video path]`<br>
--image-to-video, -i2v: converts an image into a video. usage: `python main.py [-aa, --audio-append] [video length in seconds]`<br>