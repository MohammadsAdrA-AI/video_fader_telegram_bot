## Usage: Please pass him a directory that there are raw videos
## ./Video_fader.sh ./tmp
echo "The directory is: $1."
rm ./result/*
mkdir -p result
for FILE in $1*; do echo $FILE; done
for FILE in $1*; do ffmpeg -i $FILE -vf "boxblur=10" -c:a copy ./result/blurred_video.mp4 && stat $FILE > ./result/meta_data.txt; done