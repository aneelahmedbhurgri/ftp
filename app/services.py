import uuid
from os import listdir
from os.path import isfile, join
from django.core.files.storage import FileSystemStorage
from ftpserver import settings
from zipfile import ZipFile
from win10toast import ToastNotifier


def token_generator():
    token = uuid.uuid1()
    return token.hex

def ftps_files():
    media_path = settings.MEDIA_ROOT
    myfiles = [f for f in listdir(media_path) if isfile(join(media_path, f))]
    return myfiles

def get_files(files):
    path_files = []
    fsystem = FileSystemStorage()
    for file in files:
        if fsystem.exists(file):
            path_files.append(fsystem.path(file))
    return path_files

def convert_to_zip(files):
    file_name = token_generator()
    zipObj = ZipFile(file_name+'.zip', 'w')
    for file in files:
        zipObj.write(file)
    zipObj.close()
    return file_name+'.zip'

def user_notify(notification, mssg):
    toast = ToastNotifier()
    toast.show_toast(notification,mssg,duration=20,icon_path="icon.ico")