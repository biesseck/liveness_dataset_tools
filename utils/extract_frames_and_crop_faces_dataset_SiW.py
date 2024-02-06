import os, sys
import cv2
import time
import csv
import argparse

import utils


def load_bboxes_dataset_SiW(file_path):
    try:
        data = []
        with open(file_path, 'r') as file:
            reader = csv.reader(file, delimiter=' ')
            for row in reader:
                if '' in row:
                    row.remove('')
                if '\n' in row:
                    row.remove('\n')
                for idx, value in enumerate(row):
                    if value.isnumeric():
                        row[idx] = int(value)
                    else:
                        row = [0, 0, 0, 0]    # In dataset SiW, this means the frame has no face. This frame will be ignored.
                        break
                data.append(row)
        return data
    except Exception as e:
        print(f"Error: {e}")
        return None


def find_substring_in_list(paths_list=[''], substring=''):
    for idx, path in enumerate(paths_list):
        if substring in path:
            return idx
    return -1


def extract_frames_crop_faces_from_videos_dataset_SiW(args, input_folder='', desired_extensions = ['.avi', '.mp4', '.mov', '.mkv'], output_folder='', frame_idx_to_extract=[0]):
    print('Searching video files with pattern:', desired_extensions, '...')
    files_list = utils.find_files(input_folder, desired_extensions)
    print(f'Found {len(files_list)} files')

    if len(files_list) > 0:
        output_folder = os.path.join(output_folder, input_folder.split('/')[-1])
        os.makedirs(output_folder, exist_ok=True)

        start_idx = 0
        end_idx = len(files_list)
        if args.start_string != '':
            start_idx = find_substring_in_list(files_list, args.start_string)
            print(f'start_idx: {start_idx} - string to find \'{args.start_string}\'')
        if args.end_string != '':
            end_idx = find_substring_in_list(files_list, args.end_string)
            print(f'end_idx: {end_idx} - string to find \'{args.end_idx}\'')
        files_list = files_list[start_idx:end_idx+1]
        print('')

        # files = find_files(input_folder, desired_extensions)
        for v_idx, video_path in enumerate(files_list):
            start_time = time.time()
            print(f'Extracting frames - video {v_idx+1}/{len(files_list)}: {video_path}')
            frames, extracted_frames_idx, num_frames_video = utils.extract_video_frames(video_path, frame_idx_to_extract)

            if len(frames) > 0:
                output_subfolder = os.path.relpath(video_path, input_folder)
                output_subfolder = os.path.join(output_folder, output_subfolder)
                output_subfolder = '/'.join(output_subfolder.split('/')[:-1])

                video_name = video_path.split('/')[-1].split('.')[0]
                output_video_folder = os.path.join(output_subfolder, video_name)
                os.makedirs(output_video_folder, exist_ok=True)

                bboxes_frames_video_file_name = video_name + '.face'
                path_bboxes_frames_video_file_name = os.path.join('/'.join(video_path.split('/')[:-1]), bboxes_frames_video_file_name)
                bboxes_frames = load_bboxes_dataset_SiW(path_bboxes_frames_video_file_name)
                assert len(bboxes_frames) <= num_frames_video, f'Error, len(bboxes_frames) ({len(bboxes_frames)}) != num_frames_video ({num_frames_video})'
                # print('bboxes_frames:', bboxes_frames)
                # print('len(bboxes_frames):', len(bboxes_frames))
                # print('num_frames_video:', num_frames_video)
                # sys.exit(0)

                # print(f'input_folder: {input_folder}')
                # print(f'Video {v_idx+1}/{len(files_list)}: {video_path}')
                # video_name = video_path.split('/')[-1].split('.')[0]
                for f_idx, (frame_idx, frame, bbox_frame) in enumerate(zip(extracted_frames_idx, frames, bboxes_frames)):
                    frame_filename = f'{video_name}_frame_{frame_idx:04d}.png'
                    frame_output_path = os.path.join(output_video_folder, frame_filename)
                    if sum(bbox_frame) > 0:   # if frame contains a face (frames without faces have bbox = [0, 0, 0, 0])
                        face_frame = frame[max(bbox_frame[1],0):min(bbox_frame[3],frame.shape[0]), max(bbox_frame[0],0):min(bbox_frame[2],frame.shape[1])]
                        print(f'    Saving frame {frame_idx+1}/{len(bboxes_frames)}: frame_output_path: {frame_output_path}', end='\r')
                        cv2.imwrite(frame_output_path, face_frame)
                    # elif os.path.exists(frame_output_path):  # 
                    #     print(f'\n    Deleting frame {frame_idx+1}/{len(frames)}: frame_output_path: {frame_output_path}')
                    #     os.remove(frame_output_path)

                spent_time = time.time()-start_time
                print('\n    Elapse time: %.2fs - (%.2fm)    -    Estimated time: %.2fh' % (spent_time, spent_time/60.0, (spent_time*len(files_list)-v_idx+1)/3600.0))
            else:
                raise Exception(f'No frames could be extracted from video \'{video_path}\'')

            print('-------')
        print("Frames extracted successfully!")

    else:
        raise Exception(f'No files found in \'{input_folder}\' containing pattern {desired_extensions}')


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input',  type=str, default='/datasets1/bjgbiesseck/liveness/SiW/SiW_release/Train')
    parser.add_argument('-o', '--output', type=str, default='/datasets1/bjgbiesseck/liveness/SiW_all-frames_cropped/SiW_release')
    parser.add_argument('-f', '--frame_idx', type=int, default=-1)
    # parser.add_argument('-e', '--ext', type=str, default='png')
    # parser.add_argument('-os', '--output_size', type=int, default=224)
    # parser.add_argument('-da', '--dontalign', action='store_true')
    # parser.add_argument('-dr', '--draw_bbox_lmk', action='store_true', help='')
    parser.add_argument('-s', '--start_string',  type=str, default='')
    parser.add_argument('-e', '--end_string',  type=str, default='')
    args = parser.parse_args()
    return args


if __name__ == '__main__':

    args = parse_args()

    # dataset SiW (duo)
    # input_folder_path = ['/datasets1/bjgbiesseck/liveness/SiW/SiW_release/Train']
    # input_folder_path = ['/datasets1/bjgbiesseck/liveness/SiW/SiW_release/Test']
    # output_folder_path = '/datasets1/bjgbiesseck/liveness/SiW_all-frames_cropped/SiW_release'
    input_extensions = ['.mov', '.mp4']
    
    extract_frames_crop_faces_from_videos_dataset_SiW(args, args.input, input_extensions, args.output, args.frame_idx)
