import os, sys
import cv2



def find_files(directory, extensions):
    matching_files = []

    def search_recursively(folder):
        for root, _, files in os.walk(folder):
            for file in files:
                _, file_extension = os.path.splitext(file)
                if file_extension.lower() in extensions:
                    matching_files.append(os.path.join(root, file))

    search_recursively(directory)
    return matching_files


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
    total_frames = count_frames(video_path)
    cap = cv2.VideoCapture(video_path)
    extracted_frames = []
    for index in frame_indexes:
        if index < total_frames:
            cap.set(cv2.CAP_PROP_POS_FRAMES, index)
            ret, frame = cap.read()
            if ret:
                extracted_frames.append(frame)
        else:
            print(f"Skipping index {index} as it's beyond total frame count.")
    
    cap.release()
    return extracted_frames, total_frames


def extract_save_frames_from_videos(input_folder='', desired_extensions = ['.avi', '.mp4', '.mkv'], output_folder='', frame_idx_to_extract=[0]):
    files_list = find_files(input_folder, desired_extensions)

    if len(files_list) > 0:
        output_folder = os.path.join(output_folder, input_folder.split('/')[-1])
        os.makedirs(output_folder, exist_ok=True)

        files = find_files(input_folder, desired_extensions)
        for v_idx, video_path in enumerate(files):
            output_subfolder = os.path.relpath(video_path, input_folder)
            output_subfolder = os.path.join(output_folder, output_subfolder)
            output_subfolder = '/'.join(output_subfolder.split('/')[:-1])
            
            os.makedirs(output_subfolder, exist_ok=True)
            
            frames, num_frames_video = extract_video_frames(video_path, frame_idx_to_extract)

            if len(frames) > 0:
                print(f'input_folder: {input_folder}')
                print(f'    video {v_idx}/{len(files_list)-1}: {video_path}')
                video_name = video_path.split('/')[-1].split('.')[0]
                for f_idx, (frame_idx, frame) in enumerate(zip(frame_idx_to_extract, frames)):
                    frame_filename = f'{video_name}_frame_{frame_idx:04d}.png'
                    frame_output_path = os.path.join(output_subfolder, frame_filename)
                    print(f'        frame {frame_idx}: frame_output_path:', frame_output_path)
                    cv2.imwrite(frame_output_path, frame)
            else:
                raise Exception(f'No frames could be extracted from video \'{video_path}\'')

            print('-------')
        print("Frames extracted successfully!")

    else:
        raise Exception(f'No files found in \'{input_folder}\' containing pattern {desired_extensions}')



