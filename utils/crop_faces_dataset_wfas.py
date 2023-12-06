import os, sys
import numpy as np
import cv2
import argparse
import time
from insightface.utils import face_align

import utils

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input',  type=str, default='/home/rgpa18/original_datasets/wfas/data/train')
    parser.add_argument('-o', '--output', type=str, default='/experiments/BOVIFOCR_project/datasets/bjgbiesseck/liveness/wfas_align_crop')
    parser.add_argument('-e', '--ext', type=str, default='jpg')
    parser.add_argument('-os', '--output_size', type=int, default=224)
    parser.add_argument('-da', '--dontalign', action='store_true')
    parser.add_argument('-dr', '--draw_bbox_lmk', action='store_true', help='')
    args = parser.parse_args()
    return args
    

def find_files(directory, extension):
    matching_files = []
    def search_recursively(folder):
        for root, _, files in os.walk(folder):
            for file in files:
                _, file_extension = os.path.splitext(file)
                if extension in file_extension.lower() or extension == file_extension.lower():
                    matching_files.append(os.path.join(root, file))
    search_recursively(directory)
    return matching_files


'''
Train/spoof/2D-Display-Phone/000001/000001.txt
    192 148 (bbox left top)
    234 203 (bbox right bottom)
    216 171 (landmark left eye)
    230 168 (landmark right eye)
    231 180 (landmark nose)
    218 190 (landmark left mouth )
    229 188 (landmark right mouth )
'''
def load_face_annotations(annot_path):
    with open(annot_path) as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
        # print('lines:', lines)
        face_coords = [(int(line.split(' ')[0]), int(line.split(' ')[1])) for line in lines]
        # print('face_coords:', face_coords)
        # sys.exit(0)
        return face_coords


def crop_face(img, face_coords, args):
    bbox = face_coords[:2]
    lmks = face_coords[2:]
    crop_face = img[bbox[0][1]:bbox[1][1], bbox[0][0]:bbox[1][0], :]
    print('bbox:', bbox, '    crop_face.shape:', crop_face.shape)

    # align_crop_face = crop_face
    if not args.dontalign:
        print(f'Aligning and cropping to size {args.output_size}x{args.output_size} ...')
        _lmks = np.array(lmks)
        crop_face = face_align.norm_crop(img, landmark=_lmks, image_size=args.output_size)
        print('crop_face.shape:', crop_face.shape, '(after alignment)')

    return crop_face


def draw_bbox(img, bbox):
    result_img = img.copy()
    # print('bbox:', bbox)
    x1, y1, x2, y2 = bbox[0][0], bbox[0][1], bbox[1][0], bbox[1][1]
    color = (0, 255, 0)  # Green color
    thickness = 2
    cv2.rectangle(result_img, (int(round(x1)), int(round(y1))),
                              (int(round(x2)), int(round(y2))), color, thickness)
    return result_img


def draw_lmks(img, lmks):
    result_img = img.copy()
    for l in range(lmks.shape[0]):
        color = (0, 0, 255)
        if l == 0 or l == 3:
            color = (0, 255, 0)
        cv2.circle(result_img, (int(round(lmks[l][0])), int(round(lmks[l][1]))), 1, color, 2)
    return result_img



def crop_save_faces(files_list, args, annotation_ext='txt'):
    if not os.path.isdir(args.output):
        os.makedirs(args.output, exist_ok=True)

    num_files = len(files_list)
    for i, img_path in enumerate(files_list):
        start_time = time.time()

        annot_path = img_path.replace('.'+args.ext, '.'+annotation_ext)
        print(f'i: {i}/{num_files-1}   img_path: \'{img_path}\'   annot_path: \'{annot_path}\'')
        assert os.path.exists(img_path), f'Error, no such file: \'{img_path}\''
        assert os.path.exists(annot_path), f'Error, no such file: \'{annot_path}\''

        face_coords = load_face_annotations(annot_path)
        # print('face_coords:', face_coords)

        img = cv2.imread(img_path)
        cropped_face = crop_face(img, face_coords, args)

        output_crop_name = img_path.split('/')[-1]
        output_crop_name = output_crop_name.replace('.'+args.ext, '.png')
        output_crop_dir = os.path.dirname(img_path.replace(args.input.rstrip('/'), args.output.rstrip('/')))
        output_crop_path = os.path.join(output_crop_dir, output_crop_name)
        if not os.path.exists(output_crop_path):
            os.makedirs(output_crop_dir, exist_ok=True)

        print(f'Saving \'{output_crop_path}\'')
        cv2.imwrite(output_crop_path, cropped_face)

        if args.draw_bbox_lmk:
            bbox = np.array(face_coords[:2])
            lmks = np.array(face_coords[2:])

            face_img_copy = draw_bbox(img, bbox)
            face_img_copy = draw_lmks(face_img_copy, lmks)
            # face_name = '%s_bbox.png'%(input_img_path.split('/')[-1].split('.')[0])
            output_bbox_lmk_path = output_crop_path.replace('.png', '_bbox_lmk.png')
            print(f'Saving \'{output_bbox_lmk_path}\'')
            cv2.imwrite(output_bbox_lmk_path, face_img_copy)

        end_time = time.time()
        exec_time = end_time - start_time
        remaining_files = (num_files-1) - i
        exec_remaining_files = exec_time * remaining_files
        # print(f'Elapsed time: {exec_time}s    [Will take: {remaining_files}s/{remaining_files/60}m/{remaining_files/3600}h')
        print('Elapsed time: {:.6f}s    [Will take: {:.3f}s/{:.3f}m/{:.3f}h]'.format(exec_time, exec_remaining_files, exec_remaining_files/60, exec_remaining_files/3600))
        print('------------------')
        # sys.exit(0)

    print('')


if __name__ == '__main__':
    args = parse_args()
    # print('args:', args)

    print(f'Searching files \'*.{args.ext}\' in \'{args.input}\' ...')
    files_list = find_files(args.input, args.ext)
    # print('files_list:', files_list)
    print(f'Found {len(files_list)} files')

    print(f'Cropping faces from \'{args.input}\' ...')
    crop_save_faces(files_list, args)
