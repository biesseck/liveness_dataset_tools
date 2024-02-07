import os, sys
import cv2
import time
import csv
import argparse
import glob
import shutil

import utils


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--videos_path',  type=str, default='/datasets1/bjgbiesseck/liveness/oulu-npu/train') 
    parser.add_argument('-i', '--imgs_path', type=str, default='/datasets1/bjgbiesseck/liveness/oulu-npu_all-frames_cropped_align/train')
    parser.add_argument('-ve', '--video_ext', type=str, default='.avi')
    parser.add_argument('-ie', '--img_ext', type=str, default='.png')
    args = parser.parse_args()
    args.videos_path = args.videos_path.rstrip('/')
    args.imgs_path = args.imgs_path.rstrip('/')
    return args


def organize_frames_into_subfolders(args):
    # videos_paths = load_video_paths(args.videos_path)
    videos_paths = utils.find_files(args.videos_path, [args.video_ext])

    for idx_video, video_path in enumerate(videos_paths):
        print(f'idx_video: {idx_video+1}/{len(videos_paths)} - video_path: {video_path}')
        video_name = video_path.split('/')[-1].split('.')[0]
        print(f'    video_name: {video_name}')

        output_folder = args.imgs_path
        if args.videos_path.split('/')[-1] != output_folder.split('/')[-1]:
            output_folder = os.path.join(output_folder, args.videos_path.split('/')[-1])
        output_video_path = os.path.join(output_folder, video_name)
        print(f'    output_folder: {output_folder}')
        print(f'    output_video_path: {output_video_path}')

        os.makedirs(output_video_path, exist_ok=True)

        frames_pattern = os.path.join(output_folder, f'{video_name}*{args.img_ext}')
        frames_path = glob.glob(frames_pattern)
        assert len(frames_path) > 0, f'Error, no files found with pattern \'{frames_pattern}\''
        frames_path = sorted(frames_path)
        print(f'    frames_pattern: \'{frames_pattern}\' - Found frames: {len(frames_path)}')

        for idx_frame, orig_frame_path in enumerate(frames_path):
            folders_list = orig_frame_path.split('/')
            folders_list.insert(-1, video_name)
            # print('    folders_list:', folders_list)
            dst_frame_path = '/'.join(folders_list)
            print(f'    idx_frame: {idx_frame} - dst_frame_path: {dst_frame_path}', end='\r')
            shutil.move(orig_frame_path, dst_frame_path)
        print('')

        print('-----------------')
        


if __name__ == '__main__':
    args = parse_args()

    organize_frames_into_subfolders(args)
