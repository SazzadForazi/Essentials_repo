
## Video Processing Guide
### Download Video
```bash
  yt-dlp -f "bestvideo[height=2160]+bestaudio" -o "output_name.%(ext)s" "VIDEO_URL"

```
### Cut Video Clip
```bash
  ffmpeg -i output_name.mp4 -ss 00:08:12 -to 00:09:30 -c:v libx264 -c:a aac cut_video.mp4
```
### Check Video Resolution
```bash
  ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of default=noprint_wrappers=1:nokey=1 cut_video.mp4
```
### Convert to Different Resolutions
```bash

  ffmpeg -i out_2160.mp4 -vf scale=1920:1080 -c:a copy output_1080p.mp4
  ffmpeg -i out_2160.mp4 -vf scale=1280:720 -c:a copy output_720p.mp4
  ffmpeg -i out_2160.mp4 -vf scale=854:480 -c:a copy output_480p.mp4
```