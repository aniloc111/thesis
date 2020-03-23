import os
import glob
import sys
import cv2
from multiprocessing import Pool, current_process

import argparse
out_path = ""


def dump_frames(vid_path, out_path):
    import cv2
    v_ = vid_path[0]
    video = cv2.VideoCapture(v_)
    vid_name = v_.split("\\")[-1].split(".")[0]
    out_full_path = os.path.join(out_path, vid_name)

    fcount = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

    try:
        os.mkdir(out_full_path)
    except OSError:
        pass

    file_list = []

    for i in range(fcount):
        ret, frame = video.read()
        resize_frame = cv2.resize(frame, (new_size[0], new_size[1]))

        assert ret
        
        cv2.imwrite("{}/frame_{:06d}.jpg".format(out_full_path, i), resize_frame)
        access_path = "{}/frame_{:06d}.jpg".format(vid_name, i)
        file_list.append(access_path)

    print("{} done".format(vid_name))
    sys.stdout.flush()

    return file_list


def dump_frames_temp(vid_path, out_path):
    v_ = vid_path
    video = cv2.VideoCapture(v_)
    vid_name = v_.split("\\")[-1].split(".")[0]
    out_full_path = os.path.join(out_path, vid_name)

    fcount = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

    try:
        os.mkdir(out_full_path)
    except OSError:
        pass

    file_list = []

    for i in range(fcount):
        ret, frame = video.read()
        resize_frame = cv2.resize(frame, (new_size[0], new_size[1]))

        assert ret
        
        cv2.imwrite("{}/frame_{:06d}.jpg".format(out_full_path, i), resize_frame)
        access_path = "{}/frame_{:06d}.jpg".format(vid_name, i)
        file_list.append(access_path)

    print("{} done".format(vid_name))
    sys.stdout.flush()

    return file_list


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = "extract optical flows")
    parser.add_argument("src_dir")
    parser.add_argument("out_dir")
    parser.add_argument("--num_worker", type=int, default=8)
    parser.add_argument("--flow_type", type=str, default='frame', help = 'frame')
    parser.add_argument("--ext", type=str, default='avi', choices=['avi','mp4'], help='video file extensions')
    parser.add_argument("--new_width", type=int, default=224, help='resize image width')
    parser.add_argument("--new_height", type=int, default=224, help='resize image height')

    args = parser.parse_args()

    out_path = args.out_dir
    src_path = args.src_dir
    num_worker = int(args.num_worker)
    flow_type = args.flow_type

    ext = args.ext
    new_size = (int(args.new_width), int(args.new_height))

    if not os.path.isdir(out_path):
        print("Creating output folder: " + out_path)
        os.makedirs(out_path)
    
    #vid_list = glob.glob(src_path+'/*/*.'+ext)
    vid_list = glob.glob(src_path + "/*." + ext)
    
    # for i in range(len(vid_list)):
    #     print(vid_list[i])

    print("Number of Videos: ", len(vid_list))
    print("\(sss\)")

    i = 0
    for vid in vid_list:
        dump_frames_temp(vid, out_path)
        print("{} out of {}".format(i, len(vid_list)))
        i += 1
    # pool = Pool(num_worker)
    # a = pool.map(dump_frames, zip(vid_list, range(len(vid_list))), out_path)
    
    print("Done")
