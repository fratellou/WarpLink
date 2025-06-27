from django.shortcuts import get_object_or_404, redirect, render
from django.http import FileResponse
from .models import VPNConfig
from django.contrib import messages
import shutil
from django.http import HttpResponse
import paramiko
from io import BytesIO
from django.conf import settings
from django.contrib.auth.decorators import login_required
import os


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
        response['Content-Disposition'] = 'attachment; filename="WarpLink.ovpn"'
        return response

    except Exception as e:
        # Обработка ошибок
        return HttpResponse(f'Ошибка при получении файла: {str(e)}',
                            status=500)
    finally:
        # Закрываем соединение
        ssh.close()


def create_config(request):
    try:
        # Копируем файл из системной папки в MEDIA_ROOT
        src = '~/easy-rsa/client-01.ovpn'
        dst = os.path.join(settings.MEDIA_ROOT, 'ovpn_files',
                           f'client-{request.user.id}.ovpn')

        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)

        # Сохраняем в БД
        VPNConfig.objects.update_or_create(
            user=request.user,
            defaults={'ovpn_file': f'ovpn_files/client-{request.user.id}.ovpn'}
        )

        messages.success(request, 'Конфиг успешно создан!')
    except Exception as e:
        messages.error(request, f'Ошибка: {str(e)}')

    return redirect('download')


@login_required
def download(request):
    return render(request, 'conf_generator/download.html')
