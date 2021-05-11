#!/usr/bin/env python
"""A segmentation tool for video files written in Python and ffmpeg."""

import argparse
import datetime
import os
import subprocess

__author__     = "Stefan Ensmann"
__copyright__  = "Copyright 2021, Stefan Ensmann"
__credits__    = ["Stefan Ensmann"]

__license__    = "AGPL-3.0"
__version__    = "1.0.0"
__maintainer__ = "Stefan Ensmann"
__email__      = "stefan@ensmann.de"
__status__     = "Production"

def validTimestamp(s):
    splits = s.split(":")
    ret = 0
    l = len(splits)
    if l <= 3:
        for i in range(l):
            v = splits[i]
            try:
                parsed = int(v)
                if parsed < 0 or (l-i < 3 and parsed > 59):
                    raise argparse.ArgumentTypeError("Can not create timestamp from argument: " + s)
                ret += parsed * 60 ** (l-1-i)
            except:
                raise argparse.ArgumentTypeError("Can not create timestamp from argument: " + s)
        if ret == 0:
            raise argparse.ArgumentTypeError("Timestamp can not be zero!")
        return (s, ret)
    else:
        raise argparse.ArgumentTypeError("Can not create timestamp from argument: " + s)

def validIndexlist(l):
    splits = l.split(":")
    ret = []
    for v in splits:
        try:
            ret.append(int(v))
        except:
            raise argparse.ArgumentTypeError("Can not create index list from argument: " + v)
    return ret

def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i", help="The input file to read from")
    parser.add_argument("--output", "-o", help="The file to write to")
    parser.add_argument("--concat", "-n", type=validIndexlist, help="", metavar="s1[:s2[:s3[...]]]")
    parser.add_argument("--clean", "-c", action="store_true")
    parser.add_argument("timestamp", nargs='*', type=validTimestamp, help="List of timestamps at which to split the video", metavar="[[HH:]MM:]SS")
    args = parser.parse_args()

    try:
        if args.input is None and len(args.timestamp) > 0:
            raise argparse.ArgumentTypeError("Input file is missing! (Provided timestamps to split at)")
        if args.input is not None and len(args.timestamp) == 0:
            raise argparse.ArgumentTypeError("Provide at least one timespan to split at! (Provided input file)")
        if args.output is None and args.concat is not None:
            raise argparse.ArgumentTypeError("Output file is missing! (Provided indices to concatenate)")
        if args.output is not None and args.concat is None:
            raise argparse.ArgumentTypeError("Concatenation indices are missing! (Provided output file)")

        if args.output is None and args.clean:
            print("--clean option will have no effect since no output file is generated!")

        if args.concat is not None and args.input is not None and max(args.concat) > len(args.timestamp):
            raise argparse.ArgumentTypeError("Given index is larger than number of video files!", str(max(args.concat)), str(1+len(args.timestamp)))
    except argparse.ArgumentTypeError as e:
        print(" ".join(e.args))
        return None

    spans = args.timestamp
    spans.sort(key=lambda x: x[1])
    for i in range(len(spans) - 1):
        if spans[i][1] == spans[i+1][1]:
            raise argparse.ArgumentTypeError("Timestamp is given multiple times!")
    return args

def splitFile(args):
    file_ending = ("." + args.input.split(".")[-1]) if "." in args.input else ""
    cmd = ["ffmpeg", "-i", args.input, "-codec", "copy", "-map", "0", "-f", "segment", "-segment_list", "segment_list.csv", "-segment_times", ",".join(v[0] for v in args.timestamp), "-reset_timestamps", "1", "out%03d" + file_ending]
    proc = subprocess.Popen(cmd)
    proc.wait()

def concatenateFiles(args):
    with open("segment_list.csv", "r") as seg_list:
        segments = seg_list.readlines()
        for i in range(len(segments)):
            segments[i] = segments[i].split(",")[0]
        with open("concat.txt", "w") as fh:
            for idx in args.concat:
                fh.write("file '" + segments[idx] + "'\n")
    cmd = ["ffmpeg", "-y", "-f", "concat", "-i", "concat.txt", "-c", "copy", args.output]
    proc = subprocess.Popen(cmd)
    proc.wait()

def clean(args):
    pass

def executeFFMPEG(args):
    ss_pos, to_pos = 2, 4
    command = ["ffmpeg", "-ss", None, "-to", None, "-i", args.input, "-c", "copy", None]
    file_ending = args.output[-3:]
    temp_filename = str(datetime.datetime.now()).replace(" ", "_").replace(":", "-")
    temp_input_file = "temp_{}.txt".format(temp_filename)
    temp_files = ["temp_{}_{}.{}".format(temp_filename, c, file_ending) for c in range(len(args.timestamp))]
    with open(temp_input_file, "w") as filehandler:
        filehandler.writelines(["file '{}'\n".format(f) for f in temp_files])
    counter = 0
    for timespan in args.timestamp:
        command[ss_pos], command[to_pos], command[-1] = str(timespan[0]), str(timespan[1]), temp_files[counter]
        counter += 1
        proc = subprocess.Popen(command)
        proc.wait()
    proc = subprocess.Popen(["ffmpeg", "-y", "-f", "concat", "-i", temp_input_file, "-c", "copy", args.output])
    proc.wait()
    os.remove(temp_input_file)
    for f in temp_files:
        os.remove(f)

def main():
    args = parseArgs()
    if args is not None:
        status_string = ""
        if args.input is not None:
            status_string = "Splitting file " + args.input + " at timestamps " + ", ".join([v[0] for v in args.timestamp])
        if args.output is not None:
            if args.input is not None:
                status_string += " and c"
            else:
                status_string += "C"
            status_string += "oncatenating segments " + ", ".join([str(v) for v in args.concat]) + " to output file " + args.output
        status_string += "."
        print(status_string)
        if args.input is not None:
            splitFile(args)
        if args.output is not None:
            concatenateFiles(args)
        if args.clean:
            clean()

if __name__ == "__main__":
    main()