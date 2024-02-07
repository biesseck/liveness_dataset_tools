import utils


if __name__ == '__main__':

    # dataset OULU-NPU
    input_folder_path = ['/datasets1/bjgbiesseck/liveness/oulu-npu/train',
                         '/datasets1/bjgbiesseck/liveness/oulu-npu/test',
                         '/datasets1/bjgbiesseck/liveness/oulu-npu/dev']
    desired_extensions = ['.avi']
    # output_folder_path = '/datasets1/bjgbiesseck/liveness/oulu-npu_frames'
    output_folder_path = '/datasets1/bjgbiesseck/liveness/oulu-npu_all-frames'
    

    # # dataset replay-attack
    # input_folder_path = ['/experiments/BOVIFOCR_project/datasets/bjgbiesseck/liveness/replay-attack/train',
    #                      '/experiments/BOVIFOCR_project/datasets/bjgbiesseck/liveness/replay-attack/devel',
    #                      '/experiments/BOVIFOCR_project/datasets/bjgbiesseck/liveness/replay-attack/test']
    # desired_extensions = ['.mov']
    # output_folder_path = '/experiments/BOVIFOCR_project/datasets/bjgbiesseck/liveness/replay-attack_frames'

    

    # # dataset OULU-NPU (diolkos)
    # input_folder_path = ['/nobackup/unico/datasets/liveness/oulu-npu/train',
    #                      '/nobackup/unico/datasets/liveness/oulu-npu/test',
    #                      '/nobackup/unico/datasets/liveness/oulu-npu/dev']
    # desired_extensions = ['.avi']
    # output_folder_path = '/nobackup/unico/datasets/liveness/oulu-npu/oulu-npu_all-frames'

    # frame_idx_to_extract=[0]
    frame_idx_to_extract=[-1]   # all frames

    for input_folder in input_folder_path:
        utils.extract_save_frames_from_videos(input_folder, desired_extensions,
                                              output_folder_path, frame_idx_to_extract)
