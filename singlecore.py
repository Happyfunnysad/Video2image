import cv2
import os
import csv
import time

# Открываем видеофайл
video_path = 'video.mp4'
cap = cv2.VideoCapture(video_path)

# Получаем количество кадров в видео
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# Создаем папку для сохранения кадров
output_dir = 'frames'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Считываем кадры и сохраняем их в файлы
start_time = time.time()
for i in range(frame_count):
    ret, frame = cap.read()
    if ret:
        frame_name = f'{video_path}_{i}.jpg'
        frame_path = os.path.join(output_dir, frame_name)
        cv2.imwrite(frame_path, frame)
        print(f'Saved frame {i}/{frame_count}')
    else:
        print(f'Error reading frame {i}/{frame_count}')
end_time = time.time()

# Освобождаем ресурсы
cap.release()
cv2.destroyAllWindows()

# Создаем .csv файл с информацией о времени обработки
csv_path = f'{video_path}.csv'
with open(csv_path, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Video', 'Frame count', 'Time'])
    writer.writerow([video_path, frame_count, end_time - start_time])