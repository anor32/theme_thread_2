import socket
import threading
import time

HOST = "127.0.0.1"
PORT = 50432

class EmptyString(Exception):
    pass
class TimeOff(Exception):
    pass
def handle_connection(sock, addr):
    with sock:
        print("Подключение по", addr)

        while not event_stop.is_set():
            try:
                data = sock.recv(1024)
                if not data:
                    raise EmptyString
                if data == b"quit":  # для выхода
                    sock.sendall(b"disconect")
                    sock.close()
                    break
                if data == b"stopServer":
                    sock.sendall(b"server stopped")
                    event_stop.set()
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                        sock.connect((HOST, PORT))
                        # честно говоря не  доволен таким решением
                    break
                    # я подключаюсь к самому себе чтобы попасть в блок while
                    # иначе он не выключиться


            except ConnectionError:
                print(f'Клиент внезапно отключился в процессе отправки данных на сервер')
                break
            except EmptyString:
                print("Отправлена пустая строка ошибка")
                break

            print(f'Received: {data}, from {addr}')
            data = data.upper()

            print(f'Send: {data}, to: {addr}')
            try:
                sock.sendall(data)
            except ConnectionError:
                print(f'Клиент внезапно отключился не могу отправить данные')
                break
        print("Отключение по", addr)

# ну я реализовал отключение сервера пользователем
#но он отключится только если все пользователи напишут что то ему
# правильнее было бы чтобы он отключался сразу от первой команды
# но у меня никак не получается выйти за пределы потока
# только пока все потоки не завершаться и новый пользователь не подключиться
# сервер не выключиться
# я бы очень хотел посмотреть как это реализовать правильно
# потому что у меня только так получилось

if __name__ == '__main__':
    event_stop = threading.Event()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serv_sock:
        serv_sock.bind((HOST, PORT))
        serv_sock.listen(1)
        while not event_stop.is_set():
            print('Waiting for connection...')
            my_sock, my_addr = serv_sock.accept()
            thread = threading.Thread(target=handle_connection, args=(my_sock, my_addr))
            thread.start()



