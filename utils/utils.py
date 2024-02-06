import os, sys
import cv2
import time



def find_files(directory, extensions):
    matching_files = []

    def search_recursively(folder):
        for root, _, files in os.walk(folder):
            for file in files:
                _, file_extension = os.path.splitext(file)
                if file_extension.lower() in extensions:
                    matching_files.append(os.path.join(root, file))

    search_recursively(directory)
    return sorted(matching_files)


def count_frames(video_path):
    try:
        cap = cv2.VideoCapture(video_path)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        cap.release()
        return total_frames
    except Exception as e:
        cap = cv2.VideoCapture(video_path)
        total_frames = 0
        while cap.isOpened():
            ret, _ = cap.read()
            if not ret:
                break
            total_frames += 1
        cap.release()
        return total_frames


def extract_video_frames(video_path, frame_indexes):
    print('Counting frames...', end='\r')
    total_frames = count_frames(video_path)
    cap = cv2.VideoCapture(video_path)
    extracted_frames = [None] * total_frames
    extracted_frames_idx = [None] * total_frames

    if frame_indexes == -1 or -1 in frame_indexes:
        frame_indexes = list(range(total_frames))

    num_copied_frames = 0
    for index in frame_indexes:
        if index >= 0 and index < total_frames:
            cap.set(cv2.CAP_PROP_POS_FRAMES, index)
            ret, frame = cap.read()
            if ret:
                num_copied_frames += 1
                print(f'Copying frames to memory: {num_copied_frames}/{total_frames}', end='\r')
                # extracted_frames.append(frame)
                # extracted_frames_idx.append(index)
                extracted_frames[num_copied_frames-1] = frame
                extracted_frames_idx[num_copied_frames-1] = index
        else:
            print(f"Skipping index {index} as it's beyond total frame count.")
    print('')
    
    cap.release()
    return extracted_frames, extracted_frames_idx, total_frames


def extract_save_frames_from_videos(input_folder='', desired_extensions = ['.avi', '.mp4', '.mov', '.mkv'], output_folder='', frame_idx_to_extract=[0]):
    print('Searching video files with pattern:', desired_extensions, '...')
    files_list = find_files(input_folder, desired_extensions)
    print(f'Found {len(files_list)} files')

    if len(files_list) > 0:
        output_folder = os.path.join(output_folder, input_folder.split('/')[-1])
        os.makedirs(output_folder, exist_ok=True)

        # files = find_files(input_folder, desired_extensions)
        for v_idx, video_path in enumerate(files_list):
            start_time = time.time()
            print(f'Extracting frames - video {v_idx+1}/{len(files_list)}: {video_path}')
            frames, extracted_frames_idx, num_frames_video = extract_video_frames(video_path, frame_idx_to_extract)

            if len(frames) > 0:
                output_subfolder = os.path.relpath(video_path, input_folder)
                output_subfolder = os.path.join(output_folder, output_subfolder)
                output_subfolder = '/'.join(output_subfolder.split('/')[:-1])

                video_name = video_path.split('/')[-1].split('.')[0]
                output_video_folder = os.path.join(output_subfolder, video_name)
                os.makedirs(output_video_folder, exist_ok=True)

                # print(f'input_folder: {input_folder}')
                # print(f'Video {v_idx+1}/{len(files_list)}: {video_path}')
                # video_name = video_path.split('/')[-1].split('.')[0]
                for f_idx, (frame_idx, frame) in enumerate(zip(extracted_frames_idx, frames)):
                    frame_filename = f'{video_name}_frame_{frame_idx:04d}.png'
                    frame_output_path = os.path.join(output_video_folder, frame_filename)
                    print(f'    Saving frame {frame_idx+1}/{len(frames)}: frame_output_path: {frame_output_path}', end='\r')
                    cv2.imwrite(frame_output_path, frame)
                spent_time = time.time()-start_time
                print('\n    Elapse time: %.2fs - (%.2fm)    -    Estimated time: %.2fh' % (spent_time, spent_time/60.0, (spent_time*len(files_list)-v_idx+1)/3600.0))
            else:
                raise Exception(f'No frames could be extracted from video \'{video_path}\'')

            print('-------')
        print("Frames extracted successfully!")

    else:
        raise Exception(f'No files found in \'{input_folder}\' containing pattern {desired_extensions}')



