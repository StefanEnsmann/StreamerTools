# Stream Cutter
A segmentation tool for video files written in Python and ffmpeg.

## Features
- [x] Takes a video file (e.g. a stream recording)
- [x] Splits it approximately at the given timestamps (depending on keyframe timing)
- [x] Concatenates an arbitraty subset of the segments into a new video file without recoding
- [x] Requires an installation of ffmpeg

## Usage
`python streamcutter.py [-h] [--input INPUT] [--output OUTPUT] [--concat s1[:s2[:s3[...]]]] [--clean] [[[HH:]MM:]SS ...]`

Parameter                      | Meaning
-------------------------------|----------
-h, --help                     | Shows a help message
-i, --input INPUT              | The input file to read from
-o, --output OUTPUT            | The file to write to
-n, --concat s1[:s2[:s3[...]]] | List of segment indices to concatenate
-c, --clean                    | Removes intermediate files
[[HH:]MM:]SS                   | List of timestamps at which to split the video