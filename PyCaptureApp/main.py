import cv2
import os
import time
import pyttsx3
import pickle


def delete_photos(img_folder, kind, prefix, start_ind, end_ind):
    for file_ind in range(start_ind, end_ind):
        del_img_path = f"{img_folder}/{kind}{prefix}{file_ind}.jpg"
        if os.path.exists(del_img_path):
            os.remove(del_img_path)


def collect_photos(num_img: int, wait_time: float, kind: str, main_dir: str, prefix: str, eng: pyttsx3.init(),
                   cap: cv2.VideoCapture()):

    img_folder = f"{main_dir}/{kind}"
    count_filepath = f"{main_dir}/{kind}/count.p"

    eng.say(f"{kind} photos")
    eng.runAndWait()

    eng.say(f"Collecting in")
    eng.runAndWait()

    for t in reversed(range(5)):
        eng.say(f"{t}")
        eng.runAndWait()

        time.sleep(0.2)

    if not os.path.exists(img_folder):
        os.makedirs(img_folder)

    if os.path.exists(count_filepath):
        last_num = pickle.load(open(count_filepath, "rb"))
        pickle.dump(last_num + num_img, open(count_filepath, "wb"))
    else:
        last_num = 0
        pickle.dump(num_img, open(count_filepath, "wb"))

    max_num = last_num + num_img
    try:
        while last_num < max_num:

            percent = int(100 * (last_num - (max_num - num_img)) / num_img)
            print(f"{kind} {percent}%")
            if percent % 20 == 0:
                eng.say(f"{percent} percent")
                eng.runAndWait()

            ret, frame = cap.read()
            if ret is True:
                cv2.imwrite(f"{img_folder}/{kind}{prefix}{last_num}.jpg", frame)
                time.sleep(wait_time)
                last_num += 1
            else:
                eng.say(f"Camera not ready")
                eng.runAndWait()

                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break

    except cv2.error:
        eng.say(f"CV Error")
        eng.runAndWait()
        delete_photos(img_folder=img_folder, kind=kind, prefix=prefix, start_ind=max_num-num_img, end_ind=last_num)
        pickle.dump(max_num - num_img, open(count_filepath, "wb"))
        print("Directory successfully restored")
        raise RuntimeError

    eng.say(f"Collecting finished")
    eng.runAndWait()


cam = cv2.VideoCapture(0)
engine = pyttsx3.init()


main_folder_path = 'Zbior_zdj2'
if not os.path.exists(main_folder_path):
    os.makedirs(main_folder_path)

num_img = 100  # ilość zdjęć
wait_time = 0.5  # czas pomiędzy zdjęciami
prefix = "antek"  # wpiszcie swoje imie

main_dir = main_folder_path
eng = engine
cap = cam

# serie zdjęć
collect_photos(num_img=num_img, wait_time=wait_time, kind='Senny', main_dir=main_folder_path, prefix=prefix, eng=engine, cap=cam)
collect_photos(num_img=num_img, wait_time=wait_time, kind='Skupiony', main_dir=main_folder_path, prefix=prefix, eng=engine, cap=cam)
collect_photos(num_img=num_img, wait_time=wait_time, kind='Telefon_left_hand', main_dir=main_folder_path, prefix=prefix, eng=engine, cap=cam)
collect_photos(num_img=num_img, wait_time=wait_time, kind='Telefon_right_hand', main_dir=main_folder_path, prefix=prefix, eng=engine, cap=cam)
#
# collect_photos(num_img=100, wait_time=0.5, kind='Senny', main_dir=main_folder_path, prefix="antek", eng=engine, cap=cam)
# collect_photos(num_img=100, wait_time=0.5, kind='Skupiony', main_dir=main_folder_path, prefix="antek", eng=engine, cap=cam)
# collect_photos(num_img=100, wait_time=0.5, kind='Telefon_left_hand', main_dir=main_folder_path, prefix="antek", eng=engine, cap=cam)
# collect_photos(num_img=100, wait_time=0.5, kind='Telefon_right_hand', main_dir=main_folder_path, prefix="antek", eng=engine, cap=cam)

cam.release()
