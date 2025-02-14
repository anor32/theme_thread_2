import socket

HOST = "127.0.0.1"
PORT = 50432
# кастомное исключение для отработки ошибки  сервера
class EmptyString(Exception):
    pass


if __name__ == '__main__':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serv_sock:
        serv_sock.bind((HOST, PORT)) # cвязываю сокет
        serv_sock.listen()

        while True:
            print('Ожидаю подключения...')
            sock, addr = serv_sock.accept() # принимаю подключеного пользователя
            with sock:
                print("Подключение по", addr)
                while True:
                    try:
                        data = sock.recv(1024) # принимаю данные пользователя

                        if data == b"quit": # для выхода
                            sock.sendall(b"disconect") # я надеюсь что я не порушил концепт сервера
                            #  суть в том что сервер  всегда отвечает то что пользователь написал в верхнем регистре
                            # а тут я возвращаю другой ответ но это нужно чтобы программу отключить у пользователя
                            sock.close()
                            print("Отключение пользователя")
                            break
                        if data == b"stopServer":
                            sock.sendall(b"server stopped")
                            print("Остановка сервера")
                            quit() # полный выход из программы
                        if not data:
                            raise EmptyString
                    except ConnectionError:
                        print(f'Клиент внезапно отключился в процессе отправки данных на сервер')
                        break
                    except EmptyString: # решадет проблему бесконечного цикла
                        print("пользователь ничего не отправил ошибка")
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
