----------------------------------------------------File handeling-------------------------------------------------

- ### copy desktop to machine
```
scp C:\\Users\\User\\Desktop\\cam_footage\\forazi55.mp4 tigerit@192.168.1.231:~/src/mmaction2/demo
scp -r C:\\Users\\User\\Desktop\\cam_footage tigerit@192.168.1.231:~/src/mmaction2/demo
```
- ### Download machine to computer
```
scp tigerit@192.168.1.231:~/src/mmaction2/demo_out/55_out.mp4 . 
```
- ### File Rename
```
i=1;for img in $(find . -iname '*.jpg'); do echo -n "Converting $img"; mv $img $i.jpg  && echo $i && ((i++)); done
```
- ### Image resize: 
```
mogrify -resize 640x640 -background white -gravity center -extent 640x640 *.jpg
or (without extra pading )
find . -name '*.jpg' -exec mogrify -resize 640x640\> {} \;
```
- ### Recursively find images and see dimension (width height)
```

find . -name "*.jpg" -exec identify {} \;
```
- ### Multi Folder create
```
  mkdir -p {1..5}
  mkdir -p {7..25}/{1,2,3}
```

- ### sorting all data folder to others Folder
```
cp -r row/*.mp4 all_videos/
cp -r folder_name/*/*.mp4 folder_name2/
```
- ### ZIP
```
zip -r forazi_test1.zip forazi
```
