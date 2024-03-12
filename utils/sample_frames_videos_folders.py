import os, sys
import cv2
import time
import csv
import argparse
import glob
import shutil
import random

import utils


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input-path', type=str, default='/datasets1/bjgbiesseck/liveness/oulu-npu_all-frames_cropped_align')
    parser.add_argument('-o', '--output-path', type=str, default='/datasets1/bjgbiesseck/liveness/oulu-npu_16random-frames_cropped_align')
    parser.add_argument('-n', '--num-frames', type=int, default=16)
    args = parser.parse_args()
    args.input_path = args.input_path.rstrip('/')
    return args


def find_images(folder_path, extensions):
    image_paths = []
    for root, _, files in os.walk(folder_path):
        for ext in extensions:
            pattern = os.path.join(root, '*' + ext)
            matching_files = glob.glob(pattern)
            image_paths.extend(matching_files)
    return sorted(image_paths)


def find_subfolders_videos(dataset_path, img_types=('.jpg', '.png')):
    subfolders = []
    for root, dirs, files in os.walk(dataset_path):
        if any(file.lower().endswith(img_types) for file in files):
            subfolders.append(root)
    subfolders = list(set(subfolders))   # remove repeated subfolders
    return sorted(subfolders)


def main(args):
    types = ('.jpg', '.png')
    print('Searching images of type', types, '...')
    subfolders_videos = find_subfolders_videos(args.input_path, types)
    num_subfolders = len(subfolders_videos)
    print('Found', num_subfolders, 'video folders')

    if args.output_path in args.input_path:
        args.output_path = os.path.join(args.output_path, args.input_path.split('/')[-1]+'_sampled_'+str(args.num_frames)+'frames')

    if not os.path.exists(args.output_path):
        os.makedirs(args.output_path, exist_ok=True)

    print('------------------')
    for s, subfolder_video in enumerate(subfolders_videos):
        # print('subfolder_video', str(s)+'/'+str(num_subfolders)+':', subfolder_video)
        image_path_list = find_images(subfolder_video, types)
        num_img_folder = len(image_path_list)
        # print('    Found', num_img_folder, 'images')

        if args.num_frames < num_img_folder:
            image_path_list_sampled = random.sample(image_path_list, args.num_frames)
        else:
            image_path_list_sampled = image_path_list
        num_img_folder_sampled = len(image_path_list_sampled)
        # print('    Sampled', num_img_folder_sampled, 'images')

        for i, img_path in enumerate(image_path_list_sampled):
            print('subfolder_video', str(s)+'/'+str(num_subfolders)+':', subfolder_video)
            print('    Found', num_img_folder, 'images')
            print('    Sampled', num_img_folder_sampled, 'images')
            path_output_image = img_path.replace(args.input_path, args.output_path)
            print('    img_path', str(i)+'/'+str(num_img_folder_sampled)+':', img_path)
            path_dir_output_image = os.path.dirname(path_output_image)
            print('    path_output_image:', path_output_image)
            os.makedirs(path_dir_output_image, exist_ok=True)

            shutil.copyfile(img_path, path_output_image)
            
            print('-----------------------')
            # sys.exit(0)

        # sys.exit(0)
    print('Finished!\n')


if __name__ == '__main__':
    args = parse_args()

    main(args)
