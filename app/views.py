from django.shortcuts import redirect, render
from django.http import HttpResponse
from .forms import *
from .models import *
from .services import *
from django.core.files.storage import FileSystemStorage
import json
from django.http import FileResponse
from django.contrib.auth import login,logout
from datetime import datetime
from django.contrib import messages #import messages
import time
from django.contrib.auth.decorators import login_required

# Create your views here.


def upload(request):

    if request.method == 'POST':
        if request.GET.get('token') == None:
            return render(request, 'forbiden.html')
        else:
            try:
                get_token = UploadPermission.objects.get(Token = request.GET.get('token'))
            except:
                return render(request, 'forbiden.html')
            try:
                myfile = request.FILES['file'] # this is my file
                fs = FileSystemStorage()
                filename = fs.save(myfile.name, myfile)
                user_notify("File Upload", "New File Have been Uploaded.")
                uploaded_file_url = fs.url(filename)
                get_token.delete()
            except:
                return HttpResponse("File Could not uploaded.")
            return render(request, 'fileuploaded.html')
    else:
        if request.GET.get('token') == None:
            return render(request, 'forbiden.html')
        else:
            try:
                get_token = UploadPermission.objects.get(Token = request.GET.get('token'))
            except:
                return render(request, 'forbiden.html')
            return render(request, 'globalpage.html')


@login_required(login_url='/authlogin/')
def permitUpload(request):
    
    if request.method == 'GET':
        param_token = request.GET.get('token')
        print(param_token)
        if param_token == 'None':
            return HttpResponse("Invalid Request")
        else:
            checkuser = User.objects.filter(UserToken = param_token)
            if checkuser.count() == 0:
                return HttpResponse("Not Authorized user")
            
        token_permission = UploadPermission(1,str(token_generator()))
        token_permission.save()
        return HttpResponse("upload/?token="+token_permission.Token)
    else:
        pass


def permitDownload(request):

    if request.method == 'GET':
        if request.GET.get('filetoken') == None and request.GET.get('token')!= None:
            files = request.GET['filelist']
            file_list = get_files(files.split(","))
            file_name = convert_to_zip (file_list)
            file_downloader = DownloadPermit(1,"D:\\ftpserver\\ftpserver\\"+file_name, False,False,file_name)
            file_downloader.save()
            return HttpResponse("permitdownload/?filetoken="+file_name)
        elif request.GET.get('filetoken') != None:
            try:
                checkfiletoken = DownloadPermit.objects.filter(FileToken=request.GET.get('filetoken'))
                if checkfiletoken.count() == 0:
                    return HttpResponse("Sorry No FIle Found")
                else:
                    checkfiletoken[0].Downloaded += True
                    checkfiletoken[0].save()
                    download_path = checkfiletoken[0].Filename
                    response = HttpResponse(content_type='application/zip')
                    response['Content-Disposition'] = 'attachment; filename={}'.format(download_path)
                    return response
            except:
                return HttpResponse("Sorry Server Crashed")
        else:
            return render(request, 'forbiden.html')
    else:
        return render(request, 'forbiden.html')


@login_required(login_url='/authlogin/')
def indexAuth(request):

    if request.method == 'GET':
        if request.user.is_authenticated:
            checkuser = User.objects.filter(Email = request.user)
            get_all_files = ftps_files()
            return render(request,'index.html',{'files_data':get_all_files,'token_info':checkuser[0].UserToken, 'size':len(get_all_files)})
        else:
            messages.error(request, "Not Authorized User")
            return redirect('/authlogin/')
 

def authUser(request):

    if request.method == 'POST':
        login_form = AuthUserForm(request.POST)
        if login_form.is_valid():
            email = login_form.cleaned_data['Email']
            password = login_form.cleaned_data['Password']
            try:
                checkuser = User.objects.filter(Email = email,password=password)
                login(request,checkuser[0])
                if checkuser.count() == 0:
                    messages.error(request, "Not Authorized User" )
                    return redirect('/authlogin/')
            except Exception as e:
                print(e)
                messages.error(request, "Not Authorized User" )
                return redirect('/authlogin/')
            return redirect('/authindex/')

        else:
            return HttpResponse("Invalid Information")
    elif request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/authindex/')
        form = AuthUserForm()
        return render(request,'privatesign.html', {'form':form})


@login_required
def authlogout(request):
    try:
        if request.user.is_authenticated:
            logout(request) 
            messages.info(request, "Logged Out" )
            return redirect('/authlogin/')
        else:
            return redirect('/authlogin/')
    except:
        return redirect('/authlogin/')


def authregisteration(request):

    if request.method == 'GET':
        form = AuthRegForm()
        return render(request,'authregisteration.html', {'form':form})
    elif request.method == 'POST':
        login_form = AuthRegForm(request.POST)
        if login_form.is_valid():
            try:
                email = login_form.cleaned_data['Email']
                name = login_form.cleaned_data['Name']
                password = login_form.cleaned_data['Password']
                security = login_form.cleaned_data['SecurityCode']
                print(request.POST)
                if str(security) != '2faD231Hz':
                    messages.error(request, "Not Authorized User, Can not Register Your self" )
                    return redirect('/authregister/')
                #try:
                token = '92e549862eba11ec860b9d982c80c480'
                create_auth_user = User(1,password,datetime.now(),email,name,token) 
                create_auth_user.save()
                #login(request,create_auth_user)
            except Exception as e:
                print(e)
                return HttpResponse("Authorization Failed")
            messages.success(request, "Authorization was Scuccesfull" )
            return redirect('/authlogin/')