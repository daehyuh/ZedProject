import os
import pyzed.sl as sl
from PIL import Image
import cv2
import numpy as np
import threading
from datetime import datetime
from glob import glob
from tqdm import tqdm
import shutil

count = 0
status = False
zed = sl.Camera()
runtime = sl.RuntimeParameters()
next_frame = False
dst_path = 'saved_imgs'
save_path = 'saved_imgs'
frm_path = ''

import queue  # 큐 자료구조 선언

queue_list = []  # 리스트 생성

for i in range(4):  # 4번 반복
    queue_list.append(queue.Queue())  # 큐리스트에 큐 형태 생성


def distance_undefined(nd_array):
    nd_array[nd_array != nd_array] = 0
    nd_array[nd_array == np.float32('-inf')] = -1
    nd_array[nd_array == np.float32('inf')] = 2000.0000
    return nd_array


# def file_mover(folder_path, to_path):
#     folder_name = os.path.basename(folder_path)
#     to_path_list = glob(to_path + '/*')
#     if folder_name in list(map(os.path.basename, to_path_list)):
#         path = os.path.join(to_path, folder_name + '_Copy')
#         shutil.move(folder_path, to_path)
#     else:
#         shutil.move(folder_path, to_path)

# def file_watcher(from_path, to_path):
#     write_frm_path = os.path.join(from_path, frm_path)
#     from_path_list = glob(from_path)
#     if len(from_path_list) > 0:
#         if write_frm_path in from_path_list:
#             from_path_list.remove(write_frm_path)
#         for folder in from_path_list:
#             file_mover(folder, to_path)


def file_writer():
    while True:
        global queue_list

        for queue in queue_list:
            item = queue.get()
            if 'left' in item:
                item = item['left']
                cv2.imwrite(item[0], item[1])
            elif 'right' in item:
                item = item['right']
                cv2.imwrite(item[0], item[1])

            elif 'depth_img' in item:
                item = item['depth_img']
                cv2.imwrite(item[0], item[1])
            elif 'depth' in item:
                item = item['depth']
                np.savez_compressed(item[0], x=item[1])


def record():
    global count, zed, runtime, status, next_frame, queue_list
    while True:
        if status:
            path = os.path.join(dst_path, frm_path)

            img = sl.Mat()
            zed.retrieve_measure(img, sl.MEASURE.DEPTH, sl.MEM.CPU)

            distance = distance_undefined(img.get_data())

            zed.retrieve_image(img, sl.VIEW.LEFT, sl.MEM.CPU)
            left = img.get_data()
            zed.retrieve_image(img, sl.VIEW.RIGHT, sl.MEM.CPU)
            right = img.get_data()
            zed.retrieve_image(img, sl.VIEW.DEPTH, sl.MEM.CPU)
            depth = img.get_data()

            if queue_list[0].qsize() > 15:
                continue
            elif queue_list[1].qsize() > 15:
                continue
            elif queue_list[2].qsize() > 15:
                continue
            elif queue_list[3].qsize() > 15:
                continue

            queue_list[0].put({'left': [os.path.join(path, f'left_{str(count).zfill(4)}.png'), left]})
            queue_list[1].put({'right': [os.path.join(path, f'right_{str(count).zfill(4)}.png'), right]})
            queue_list[2].put({'depth': [os.path.join(path, f'distance_{str(count).zfill(4)}.npz'), distance]})
            print(distance, type(distance))
            queue_list[3].put({'depth_img': [os.path.join(path, f'depth_{str(count).zfill(4)}.png'), depth]})

            count += 1
        else:
            count = 0


def main():
    global count, zed, runtime, status, next_frame, frm_path

    init_params = sl.InitParameters()  # camera 객체 생성
    init_params.camera_resolution = sl.RESOLUTION.HD1080  # Use HD1080 video mode
    init_params.camera_fps = 60  # Set fps at 30
    init_params.coordinate_units = sl.UNIT.METER

    err = zed.open(init_params)
    if err != sl.ERROR_CODE.SUCCESS:
        print('failed')
    else:
        print('Camera Opened!')

    left = sl.Mat()

    image_size = zed.get_camera_information().camera_resolution
    print(image_size.width, image_size.height)
    image_size.width = image_size.width / 2
    image_size.height = image_size.height / 2
    print(image_size.width, image_size.height)

    while True:
        if zed.grab(runtime) == sl.ERROR_CODE.SUCCESS:
            next_frame = True

            # Video show
            zed.retrieve_image(left, sl.VIEW.LEFT)
            resized_left = cv2.resize(left.get_data(), (image_size.width, image_size.height))

            cv2.putText(resized_left, str(count), (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 3)
            cv2.imshow('ZED_depth', resized_left)

        else:
            break

        key = cv2.waitKey(5)  # Esc K
        if key == 27:
            break

        elif key == 32:  # 스페이스바 누르면 경로생성후 파일저장
            status = not status
            if status:
                frm_path = datetime.today().strftime('%Y%m%d_%H%M%S%f')
                root_path = os.path.join(dst_path, frm_path)
                os.makedirs(root_path, exist_ok=True)
            else:
                count = 0
                frm_path = ''

    cv2.destroyAllWindows()
    zed.close()


if __name__ == "__main__":
    save_imgs = threading.Thread(target=record, args=(), daemon=True)
    save_imgs.start()
    thread_list = []

    for i in range(4):  # 파일 저장 스레드 4개
        thread = threading.Thread(target=file_writer, args=())
        thread.start()
        thread_list.append(thread)
    main()

    for thread in thread_list:
        thread.join()

    save_imgs.join()

    # file_watcher = threading.Thread(target=file_watcher, args=(os.path.join(save_path, '*'), dst_path), daemon=True)
    # file_watcher.start()
    # file_watcher.join()