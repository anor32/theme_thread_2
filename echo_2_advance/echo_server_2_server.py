import socket

HOST = "127.0.0.1"
PORT = 50432


if __name__ == '__main__':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serv_sock:
        serv_sock.bind((HOST, PORT))
        serv_sock.listen()

        while True:
            print('Ожидаю подключения...')
            sock, addr = serv_sock.accept()
            with sock:
                print("Подключение по", addr)

                while True:
                    try:
                        data = sock.recv(1024)
                    except ConnectionError:
                        print(f'Клиент внезапно отключился в процессе отправки данных на сервер')
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
