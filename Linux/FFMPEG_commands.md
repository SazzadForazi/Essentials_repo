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
- ### Resize video
```
ffmpeg -i 4.mp4 -vf scale=454:256 output451.mp4
```



---------------------------------------------------# CAM-----------------------------------------------------------
- ### Record cam footage
```
ffmpeg -rtsp_transport tcp -i 'rtsp://admin:tiger1234@192.168.107.241:554/cam/realmonitor?channel=3&subtype=0' -vcodec copy test1.mp4
```
- ### Cutting video
 ```
ffmpeg -ss 00:05:30 -i input.mp4 -t 00:01:00 -c:v copy -c:a copy output.mp4
```
- ### full video to 1 sec cutting command
```
ffmpeg -i input.mp4 -c copy -map 0 -segment_time 00:00:00 -f segment -reset_timestamps 1 output%03d.mp4
 ```


------------------------------------------------From Monirul vaiya --------------------------------------------------
- ### save rtsp
```
ffmpeg -rtsp_transport tcp -i rtsp://admin:admin123@192.168.107.149 -vcodec copy ptz.mp4
ffmpeg -rtsp_transport tcp -i 'rtsp://admin:admin123@202.164.208.221' -vcodec copy gulshan.mp4
ffmpeg -i 'rtsp://developer:C%40mera%23dev@192.168.250.84:554/cam/realmonitor?channel=5&subtype=0' -vcodec copy mohakhali.mp4
```
- ### change frame rate
```
ffmpeg -i input.mp4 -filter:v fps=30 output.mp4
```
- ### convert from mkv to mp4
```
ffmpeg -i input.mkv -vcodec copy -acodec copy output.mp4
```
- ### extract all frames
```
ffmpeg -i input.mp4 ./output/%05d.jpg -hide_banner
```
- ### cut video using duration/timestamp
```
ffmpeg -ss 00:05:30 -i input.mp4 -t 00:01:00 -c:v copy -c:a copy output.mp4
```
- ### add frame number
```
ffmpeg -i 1.mp4 -vf "drawtext=fontfile=Arial.ttf: text='%{frame_num}': start_number=1: x=(w-tw)/2: y=h-150: fontcolor=black: fontsize=60: box=1: boxcolor=white: boxborderw=5" -c:a copy output.mp4
```
- ### merge 2 videos side by side
```
ffmpeg -i v1.mp4 -i v2.mp4 -filter_complex hstack output.mp4
```
- ### add text top middle
```
frsdemo % ffmpeg -i v1.mp4 -vf "drawtext=fontfile=/path/to/font.ttf:text='V1':fontcolor=white:fontsize=24:box=1:boxcolor=black@0.5:boxborderw=5:x=(w-text_w)/2:y=10" -codec:a copy v11.mp4
```
- ### add text top middle (preview)
```
ffplay -vf "drawtext=fontfile=/path/to/font.ttf:text='V1':fontcolor=white:fontsize=24:box=1:boxcolor=black@0.5:boxborderw=5:x=(w-text_w)/2:y=10" v1.mp4
```
- ### merge multiple ts file 
```
cat segment1_0_av.ts segment2_0_av.ts segment3_0_av.ts > all.ts
ffmpeg -i all.ts -acodec copy -vcodec copy all.mp4
```
- ### change bitrate
```
ffmpeg -i output.mp4 -b 2000k output1.mp4
```
- ### make video from frames/images
```
ffmpeg -framerate 30 -i ./output/%d.jpg -c:v libx264 -r 30 output.mp4
```
- ### Remove audio
```
ffmpeg -i $input_file -vcodec copy -an $output_file
```
- ### Force opencv to use tcp for rtsp video capture
```
export OPENCV_FFMPEG_CAPTURE_OPTIONS="rtsp_transport;tcp"
```
- ### Resize/scale video
```
ffmpeg -i input.mp4 -vf scale=320:240 output.mp4
```
- ### Resize/scale video (maintain aspect ratio)
```
ffmpeg -i input.mp4 -vf scale=320:-1 output.mp4
```
- ### Make 15 seconds video from a single image
```
ffmpeg -loop 1 -i input_image.jpg -t 15 -c:v libx264 -pix_fmt yuv420p output_video.mp4
```
- ### merge/concate multiple mp4 files
```
$ cat mylist.txt
file '/path/to/file1'
file '/path/to/file2'
file '/path/to/file3'
    
$ ffmpeg -f concat -safe 0 -i mylist.txt -c copy output.mp4

```
- ###  For Windows
```
(echo file 'first file.mp4' & echo file 'second file.mp4' )>list.txt
or
(for %i in (*.mp4) do @echo file '%i') > mylist.txt
ffmpeg -safe 0 -f concat -i list.txt -c copy output.mp4
```



