# FFMPEG
### Commands
- ### To see information about this video
```
ffprobe video.mp4
```
- ### for video codec change
  ```
  ffmpeg -i 1.mp4 -c:v libx264 -c:a aac -strict -2 test35.mp4
  ```
- ### for video mute
  ```
  ffmpeg -i demo2.mp4 -c copy -an t_demo.mp4
  ```

- ### video_to_frame
```
ffmpeg -i input.mp4 ./output/%05d.jpg -hide_banner
```
- ### frame_to_video
```
ffmpeg -framerate 30 -i ./output/%d.jpg -c:v libx264 -r 30 output.mp4
```

---------------------------------------------------CAM-----------------------------------------------------------
- ### Record cam footage
  ```
  ffmpeg -rtsp_transport tcp -i 'rtsp://admin:tiger1234@192.168.107.241:554/cam/realmonitor?channel=3&subtype=0' -vcodec copy test1.mp4
  ```
- ### Cutting video
 ```
ffmpeg -ss 00:05:30 -i input.mp4 -t 00:01:00 -c:v copy -c:a copy output.mp4

full video to 1 sec cutting command
ffmpeg -i input.mp4 -c copy -map 0 -segment_time 00:00:00 -f segment -reset_timestamps 1 output%03d.mp4
 ```








