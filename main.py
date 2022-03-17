import random
import keyboard
import multiprocessing as mp
import time


def sleep(queue, f_sleep, end):
    while 1:
        if keyboard.is_pressed("q"):
            print('Завершение программы')
            f_sleep.value = True
            end.value = True
            break
        else:
            if queue.qsize() >= 100 and not f_sleep.value:
                print('Блокировка производителей')
                f_sleep.value = True
            elif queue.qsize() <= 80 and f_sleep.value:
                print('Запуск производителей')
                f_sleep.value = False


def consumer(queue, end):
    while 1:
        time.sleep(2)
        if end.value and queue.qsize() == 0: break
        print('Получено значение ', queue.get())


def manufacturer(queue, f_sleep, end):
    while 1:
        time.sleep(0.5)
        if end.value: break
        if not f_sleep.value:
            x = random.randint(1, 100)
            queue.put(x)
            print('Записано значение ', x)


if __name__ == '__main__':
    queue = mp.Queue(200)
    manager = mp.Manager()
    f_sleep = manager.Value('b', False)
    end = manager.Value('b', False)
    control_thread = mp.Process(target=sleep, args=(queue, f_sleep, end,))
    manufacturer1_thread = mp.Process(target=manufacturer, args=(queue, f_sleep, end,))
    manufacturer2_thread = mp.Process(target=manufacturer, args=(queue, f_sleep, end,))
    manufacturer3_thread = mp.Process(target=manufacturer, args=(queue, f_sleep, end,))
    consumer1_thread = mp.Process(target=consumer, args=(queue, end,))
    consumer2_thread = mp.Process(target=consumer, args=(queue, end,))

    control_thread.start()
    manufacturer1_thread.start()
    manufacturer2_thread.start()
    manufacturer3_thread.start()
    consumer1_thread.start()
    consumer2_thread.start()

    control_thread.join()
    manufacturer1_thread.join()
    manufacturer2_thread.join()
    manufacturer3_thread.join()
    consumer1_thread.join()
    consumer2_thread.join()
