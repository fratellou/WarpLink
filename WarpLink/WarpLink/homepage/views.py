import os
from io import BytesIO

import paramiko
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, HttpResponse, JsonResponse
from django.shortcuts import render


def home(request):
    return render(request, 'homepage/home.html')


@login_required
def download_config(request):
    SSH_HOST = os.getenv('SSH_HOST')
    SSH_PORT = os.getenv('SSH_PORT')
    SSH_USERNAME = os.getenv('SSH_USERNAME')
    SSH_PASSWORD = os.getenv('SSH_PASSWORD')
    REMOTE_PATH = os.getenv('REMOTE_PATH')

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Подключаемся к серверу
        ssh.connect(SSH_HOST, port=SSH_PORT,
                    username=SSH_USERNAME, password=SSH_PASSWORD)

        # Получаем файл через SCP
        with BytesIO() as file_buffer:
            with ssh.open_sftp() as sftp:
                sftp.getfo(REMOTE_PATH, file_buffer)
            file_buffer.seek(0)
            file_content = file_buffer.read()

        # Отправляем файл пользователю
        response = FileResponse(BytesIO(file_content),
                                content_type='application/ovpn')
        response[
            'Content-Disposition'
        ] = 'attachment; filename="WarpLink.ovpn"'
        return response

    except Exception as e:
        # Обработка ошибок
        return HttpResponse(f'Ошибка при получении файла: {str(e)}',
                            status=500)
    finally:
        # Закрываем соединение
        ssh.close()


def server_status(request):
    remote_ip = request.META.get('REMOTE_ADDR', '')
    if remote_ip.startswith('10.8.0.'):
        return JsonResponse({
            'status': 'vpn_connected',
            'ip': remote_ip
        })

    # Параметры подключения к VPN серверу
    SSH_HOST = os.getenv('SSH_HOST')
    SSH_PORT = int(os.getenv('SSH_PORT'))
    SSH_USERNAME = os.getenv('SSH_USERNAME')
    SSH_PASSWORD = os.getenv('SSH_PASSWORD')

    # Параметры для проверки статуса
    SERVICE_NAME = os.getenv('SERVICE_NAME')
    STATUS_FILE = os.getenv('STATUS_FILE')

    try:
        # Подключение к серверу
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(SSH_HOST, port=SSH_PORT,
                    username=SSH_USERNAME, password=SSH_PASSWORD,
                    timeout=5)

        # Проверка активности сервиса
        stdin, stdout, stderr = ssh.exec_command(
            f'systemctl is-active {SERVICE_NAME}')
        service_status = stdout.read().decode().strip()

        # Подсчет подключенных пользователей
        stdin, stdout, stderr = ssh.exec_command(
            f"grep '^CLIENT_LIST' {STATUS_FILE}")
        clients = stdout.readlines()
        clients_count = len(clients)

        return JsonResponse({
            'status': 'active' if service_status == 'active' else 'inactive',
            'clients_count': clients_count
        })

    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'clients_count': 0,
            'error': str(e)
        })

    finally:
        if ssh:
            ssh.close()
