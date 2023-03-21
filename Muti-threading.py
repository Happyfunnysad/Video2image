import cv2
import os
import threading
import time
import csv

# Открываем видеофайл
cap = cv2.VideoCapture('video.mp4')

# Создаем папку для сохранения кадров
video_name = os.path.splitext(os.path.basename('video.mp4'))[0]
output_folder = video_name + '_' + str(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))) + '_frames'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Задаем начальный кадр
frame_num = 0
lock = threading.Lock()

# Функция для сохранения кадров
def save_frame(frame, frame_num):
    cv2.imwrite(os.path.join(output_folder, 'frame' + str(frame_num) + '.jpg'), frame)
    with lock:
        global saved_frames
        saved_frames += 1
        print('Сохранено кадров:', saved_frames)

# Читаем кадры из видео и сохраняем их в файлы в многопоточном режиме
saved_frames = 0
threads = []
start_time = time.time()
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == False:
        break
    thread = threading.Thread(target=save_frame, args=(frame, frame_num))
    threads.append(thread)
    thread.start()
    frame_num += 1

# Дожидаемся завершения всех потоков
for thread in threads:
    thread.join()

# Освобождаем память и закрываем файл
cap.release()
cv2.destroyAllWindows()

# Записываем время выполнения в CSV-файл
end_time = time.time()
execution_time = end_time - start_time
csv_file = video_name + '_' + str(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))) + '_frames' + '_time.csv'
with open(csv_file, mode='w') as file:
    writer = csv.writer(file)
    writer.writerow(['Video', 'Frames', 'Time'])
    writer.writerow([video_name, int(cap.get(cv2.CAP_PROP_FRAME_COUNT)), execution_time])
print('Время выполнения: {} секунд'.format(execution_time))