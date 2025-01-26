#Cloned from (Original)
[GoPro-Concat-Automation](https://github.com/scuc/GoPro-Concat-Automation)



# GoPro Concat with Python and FFMPEG

A Python script to stitch together large batches of
segmented GoPro files. 

## Project Description

GoPro records .MP4 video files that are segmented based on a 4Gb file size limit.
This script is used to go through a large batch of segmented GoPro files and
merge them based on their file number and creation dates.

**Example:**

`GOPR1234.mp4` The first video in a set - always contains "GOPR" at the head of the filename, followed by a file number.)

`GP011234.mp4` 1st chapter of the original video - subsequent files have "GPO" followed by a chapter number and then a file number. )

`GP021234.mp4` 2nd chapter of the same video - GP0 + 2 + 1234 + .mp4



## Prerequisites

[Mac OS X 10.11 or later](https://support.apple.com/en_CA/downloads/macos)

[Python 3.6 or later](https://www.python.org/downloads/)

[pymediainfo](https://pymediainfo.readthedocs.io/en/stable/)

[FFMPEG 4.1 or later](https://www.ffmpeg.org/download.html)

## Files Included

**``setup.py``** - optional script to run, it will install the pymediainfo library.

**``gopro_main.py``** - execute for initialization of the script.

**``gopro_concat.py``** - the module that handles the concatantion and downconvert of the segmented GoPro files. 

**``get_mediainfo.py``** - the  module that uses pymediainfo to get all the metadata on the video files. 

## Getting Started

After the prerequisites are installed.

1. cd to the working dir for the script and execute **`` python3 gopro_main.py``** from the terminal.

2. The terminal will prompt for user input: 	
	* 	Source Directory path
	* 	Output Directory path
	* 	DownConvert (Yes/No)

3. Let the script run, monitor the progress by checking the logs in output folder. 


## Steps in the Script

1.   Make a list of all the GoPro .MP4 files in a given source directory.
1.   Loop through the list and group files into dictionaries based on name and creation.
1.   Get the mediainfo for these files.
1.   Create a .txt file(s) with the full paths of files. 
1.   Pass the .txt file to FFMPEG which concats the grouped MP4 into one .MP4. 
1.   (Optional) Downconvert the merged file to a lower bitrate. 

