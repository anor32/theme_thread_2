import socket

HOST = "127.0.0.1"
PORT = 50432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((HOST, PORT))
    while True:

        data_to_send = input("Message to send:")
        if data_to_send =="": # отработка зависания программы если пустая
            # строка передана на сервере это никак не отработать или я незнаю как
            print("Строка не может быть пустой")
            continue
        data_bytes_send = data_to_send.encode()

        sock.sendall(data_bytes_send)
        try:
            data_bytes_received = sock.recv(1024)

            data_received = data_bytes_received.decode()
            print("Received:", data_received)
            if data_received == "disconect": # получили ответ  и выключаемся
                print('Disconected from server')
                break

        except ConnectionAbortedError: # на случай выключения сервера чтобы не упасть с ошибкой
            print("Программа на вашем хост-компьютере разорвала установленное подключение")
            break

# по условию особо не понятно можно ли менять клиентский код и обрабатывать ошибки в нем
# ну я думаю что да иначе как мне отработать исключения