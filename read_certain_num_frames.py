import os
import numpy as numpy
import glob
import argparse
import re

def natural_sort(l):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]

    return sorted(l, key = alphanum_key)

parser = argparse.ArgumentParser(description = "Read Frames in folder")
parser.add_argument("-src_dir", type = str, default = "dataset_msvd")
parser.add_argument("-rgboutfile", type = str, default = "5frame_list.txt")
parser.add_argument("-flowxoutfile", type = str, default = "25flowx_list.txt")
parser.add_argument("-flowyoutfile", type = str, default = "25flowy_list.txt")
parser.add_argument("-rgb_prefix", type = str, default = "frame_")
parser.add_argument("--flow_x_prefix", type = str, help="prefix of x direction flow images", default = "flow_x_")
parser.add_argument("--flow_y_prefix", type = str, help="prefix of y direction flow images", default = "flow_y_")
parser.add_argument("-modality", type = str, default = "rgb")
parser.add_argument("-framenum", type = int, default = 5)

args = parser.parse_args()

src_dir = args.src_dir
frame_num = int(args.framenum)
rgb_prefix = args.rgb_prefix
flow_x_prefix = args.flow_x_prefix
flow_y_prefix = args.flow_y_prefix

stack_depth = 0

if args.modality == "rgb":
    stack_depth = 1
    rgboutfile = open(args.rgboutfile, "w")
elif args.modality == "flow":
    stack_depth = 5
    flowxoutfile = open(args.flowxoutfile, "w")
    flowyoutfile = open(args.flowyoutfile, "w")


for root, subfolders, filename in os.walk(src_dir):
    subfolders = natural_sort(subfolders)

    for folders in subfolders:
        files = os.listdir(os.path.join(root, folders))
        frame_cnt = 0

        for filenames in sorted(files):
            if "frame" in filenames:
                frame_cnt += 1

        step = int((frame_cnt - stack_depth) / frame_num)
        print("Step ", step)

        if step > 0:
            frame_ticks = range(1, min((2 + step * (frame_num - 1)), frame_cnt + 1), step)
        else:
            frame_ticks = range(frame_cnt)

            print("Frame", frame_ticks)

            frame_ticks = map(lambda x: x + 1, frame_ticks)
            frame_ticks_temp = [1] * (frame_num - frame_cnt)
            frame_ticks = dict(frame_ticks, **frame_ticks_temp)
            #frame_ticks_dict.update([1] * (frame_num - frame_cnt))

        for tick in frame_ticks:
            if args.modality == "rgb":
                name = "{}{:06d}.jpg".format(rgb_prefix, tick)
                rgboutfile.write("%s, %s\n"%(folders, os.path.join(root, folders, name)))
            
            if args.modality == "flow":
                frame_idx = [min(frame_cnt, tick + offset) for offset in range(stack_depth)]

                for idx in frame_idx:
                    flowxname = "{}{:06d}.jpg".format(flow_x_prefix, idx)
                    flowxoutfile.write("%s, %s\n"%(folders, os.path.join(root, folders, flowxname)))
                    flowyname = "{}{:06d}.jpg".format(flow_y_prefix, idx)
                    flowyoutfile.write("%s, %s\n"%(folders, os.path.join(root, folders, flowyname)))
