import os
import pyzed.sl as sl
import cv2
import numpy as np
import threading
from datetime import datetime
import sys

zed = sl.Camera()
runtime = sl.RuntimeParameters()
count = 0  # 사진 카운트
status = False  # 키 입력 확인
next_frame = False  # 카메라 확인
save_path = 'saved_imgs'
frm_path = ''


# import queue  # 큐 자료구조 선언
# queue_list = []  # 리스트 생성
# for i in range(4):  # 4번 반복
#     queue_list.append(queue.Queue())  # 큐 리스트에 큐 형태 생성


def distance_undefined(nd_array):
    nd_array[nd_array != nd_array] = 0
    nd_array[nd_array == np.float32('-inf')] = -1
    nd_array[nd_array == np.float32('inf')] = 2000.0000
    return nd_array


# def file_writer():
#     while True:
#         global queue_list
#         for queue in queue_list:
#             item = queue.get()
#             if 'left' in item:
#                 item = item['left']
#                 cv2.imwrite(item[0], item[1])
#             elif 'right' in item:
#                 item = item['right']
#                 cv2.imwrite(item[0], item[1])
#             elif 'depth_img' in item:
#                 item = item['depth_img']
#                 cv2.imwrite(item[0], item[1])
#             elif 'depth' in item:
#                 item = item['depth']
#                 np.savez_compressed(item[0], x=item[1])


def record():
    global count, zed, runtime, status, next_frame, queue_list
    while True:
        if status:
            path = os.path.join(save_path, frm_path)
            left = sl.Mat()
            right = sl.Mat()
            depth = sl.Mat()
            dis = sl.Mat()
            runtime_parameters = sl.RuntimeParameters()

            if zed.grab(runtime_parameters) == sl.ERROR_CODE.SUCCESS:
                zed.retrieve_image(left, sl.VIEW.LEFT)
                zed.retrieve_image(right, sl.VIEW.RIGHT)
                zed.retrieve_image(depth, sl.VIEW.DEPTH)
                zed.retrieve_measure(dis, sl.MEASURE.DEPTH)
                dis = distance_undefined(dis.get_data())
                # print(dis)

                cv2.imwrite(os.path.join(path, f'left_{str(count).zfill(4)}.jpg'), left.get_data())  # to do def
                cv2.imwrite(os.path.join(path, f'right_{str(count).zfill(4)}.jpg'), right.get_data())
                cv2.imwrite(os.path.join(path, f'depth_{str(count).zfill(4)}.jpg'), depth.get_data())
                # np.savez_compressed(os.path.join(path, f'distance_{str(count).zfill(4)}'), x=dis)
                # cv2.imwrite(os.path.join(path, f'distance_{str(count).zfill(4)}.nqz'), dis.get_data())

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

    image_size = zed.get_camera_information().camera_resolution  # zed카메라 가로세로 크기
    print(f'original width : {image_size.width}px\noriginal height : {image_size.height}px')
    # resizing
    image_size.width = image_size.width / 2
    image_size.height = image_size.height / 2
    print(f'resized width : {image_size.width}px\nresized height : {image_size.height}px')
    left = sl.Mat()  # for show

    while True:
        if zed.grab(runtime) == sl.ERROR_CODE.SUCCESS:
            next_frame = True

            # Show Camera
            zed.retrieve_image(left, sl.VIEW.LEFT)
            resized_left = cv2.resize(left.get_data(), (image_size.width, image_size.height))

            cv2.putText(resized_left, str(count), (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 3)
            cv2.imshow('ZED_depth', resized_left)

        else:
            cv2.destroyAllWindows()
            zed.close()
            break

        key = cv2.waitKey(5)  # Ese to exit program
        if key == 27:
            break

        elif key == 32:  # Space bar to save Image Event
            status = not status
            if status:
                frm_path = datetime.today().strftime('%Y%m%d_%H%M%S%f')
                root_path = os.path.join(save_path, frm_path)
                os.makedirs(root_path, exist_ok=True)
            else:
                count = 0
                frm_path = ''

    cv2.destroyAllWindows()
    zed.close()
    sys.exit(0)


if __name__ == "__main__":
    save_imgs = threading.Thread(target=record, args=(), daemon=True)
    save_imgs.start()
    main()
    save_imgs.join()
    # file_watcher = threading.Thread(target=file_watcher, args=(os.path.join(save_path, '*'), dst_path), daemon=True)
    # file_watcher.start()

    # thread_list = []
    # for i in range(4):
    #     thread = threading.Thread(target=file_writer, args=())
    #     thread.start()
    #     thread_list.append(thread)

    # for thread in thread_list:
    #     thread.join()

    # file_watcher.join()
