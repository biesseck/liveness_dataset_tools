import utils


if __name__ == '__main__':

    # dataset OULU-NPU
    input_folder_path = ['/experiments/BOVIFOCR_project/datasets/bjgbiesseck/liveness/oulu-npu/train',
                         '/experiments/BOVIFOCR_project/datasets/bjgbiesseck/liveness/oulu-npu/test',
                         '/experiments/BOVIFOCR_project/datasets/bjgbiesseck/liveness/oulu-npu/dev']
    desired_extensions = ['.avi']

    output_folder_path = '/experiments/BOVIFOCR_project/datasets/bjgbiesseck/liveness/oulu-npu_frames'
    frame_idx_to_extract=[0]

    for input_folder in input_folder_path:
        utils.extract_save_frames_from_videos(input_folder, desired_extensions,
                                              output_folder_path, frame_idx_to_extract)