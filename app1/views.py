from django.contrib import auth
from django.http import JsonResponse
from django.shortcuts import render, redirect, HttpResponse
from app1.self_functions.forms_functions import UserForm
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from app1.models import *
from datetime import datetime


def login(request):
    if request.method == "POST":
        response = {"user": None, "msg": None}
        user = request.POST.get("user")
        pwd = request.POST.get("pwd")
        valid_code_user = request.POST.get("valid_code")
        # print("user:",user," pwd:",pwd," valid:",valid_code_user)
        valid_code_service = request.session.get("valid_code_str")
        print("valid_user", valid_code_user)
        print("valid_service", valid_code_service)
        if valid_code_user.upper() == valid_code_service.upper():
            user = auth.authenticate(username=user, password=pwd)
            if user:
                auth.login(request, user)
                response["user"] = user.username
            else:
                response["msg"] = "用户名或者密码错误"
        else:
            response["msg"] = "验证码输入错误"
        return JsonResponse(response)
    return render(request, "login.html")


def updatecode(request):
    if request.method == "POST":
        print("here")
        response = {"user": None, "msg": None}
        old_pwd = request.POST.get("old_pwd")
        new_pwd = request.POST.get("new_pwd")
        print("new_pwd", new_pwd)
        print("old_pwd", old_pwd)
        valid_code_user = request.POST.get("valid_code")
        print("code", valid_code_user)
        valid_code_service = request.session.get("valid_code_str")
        if valid_code_user.upper() == valid_code_service.upper():
            user = auth.authenticate(username=request.user.username, password=old_pwd)
            if user:
                mpwd = make_password(new_pwd, None, 'pbkdf2_sha256')
                user = UserLogin.objects.filter(nid=request.user.nid).update(password=mpwd)
                response["user"] = user
                auth.logout(request)
            else:
                response["msg"] = "旧密码输入错误"
        else:
            response["msg"] = "验证码错误"
        return JsonResponse(response)
    return render(request, "updatecode.html")


def logout(request):
    auth.logout(request)
    return redirect("/login/")


def get_valid_image(request):
    from app1.self_functions.valid_image_function import get_valid_image_function
    data = get_valid_image_function(request)
    print(type(data))
    return HttpResponse(data)


def register(request):
    if request.method == "POST":
        response = {"user": None, "msg": None}
        formdata = UserForm(request.POST)
        if formdata.is_valid():
            response["user"] = formdata.cleaned_data.get("user")
            username = formdata.cleaned_data.get("user")
            pwd = formdata.cleaned_data.get("pwd")
            email = formdata.cleaned_data.get("email")
            avatar_obj = request.FILES.get("avatar")
            extral = {}
            if avatar_obj:
                extral = {"avatar": avatar_obj}
            print("here")
            UserLogin.objects.create_user(username=username, password=pwd, email=email, **extral)
        else:
            response["msg"] = formdata.errors
        return JsonResponse(response)
    form = UserForm()
    return render(request, "register.html", {"form": form})


def index(request):
    user = UserLogin.objects.filter(username=request.user.username).first()
    if user.is_firmuser:
        return render(request, "firm/project.html")
    elif user.is_superuser:
        return render(request, "administrator/projmanage.html")
    else:
        return render(request, "staff/monitor.html", {"user": user})


def staff(request, keyword):
    loginUser = request.user
    print("keyword", keyword)
    if keyword == "monitor/":
        if request.method == "POST":
            reporteduser = request.POST.get("reporteduser")
            reportuser = request.POST.get("reportuser")
            placename = request.POST.get("placename")
            placeid = request.POST.get("placeid")
            reportdate = request.POST.get("reporttime")
            monitorimg = request.FILES.get("monitorimg")
            info = MonitorInfomation.objects.create(reporteduser=reporteduser, reportuser=reportuser,
                                                    placename=placename, placeid=placeid,
                                                    reportdate=reportdate, monitorimg=monitorimg)
            print(info.nid)
        return render(request, "staff/monitor.html", {"user": loginUser})
    elif keyword == "salary/":
        salary = Salary.objects.filter(user__userlogin__nid=loginUser.nid).first()

        print(type(salary))
        print("here")
        # print("salary",salary.basicsalary)
        return render(request, "staff/salary.html", {"user": loginUser, "salary": salary})
    elif keyword == "set/":
        userinfo = User.objects.filter(nid=loginUser.user_id).first()
        department = Departmemt.objects.filter(nid=userinfo.company_id).first()
        # print(type(userinfo))
        return render(request, "staff/set.html", {"user": loginUser, "userinfo": userinfo, "department": department})
    elif keyword == "inform/":
        datas = Notice.objects.all()
        notices = datas[datas.count() - 5:datas.count()]  # 获取最新的五条通知
        return render(request, "staff/inform.html", {"user": loginUser, "notices": notices})


def administrator(request, keyword):
    # print("keyword", keyword)
    loginUser = request.user
    if keyword == "projmanage/":
        print("here")
        userinfo = User.objects.filter(nid=loginUser.user_id).first()
        project = userinfo.project.first()
        departments = Departmemt.objects.filter(project_id=project.nid).all()
        department = departments.first()
        print("departmenttype", type(departments))
        departmentslist = []
        for department in departments:
            departmentslist.append(department)
        projectplace = Projectplace.objects.filter(project_id=project.nid).first()

        return render(request, "administrator/projmanage.html",
                      {"user": loginUser, "project": project, "department": department,
                       "departmentslist": departmentslist, "userinfo": userinfo, "projectplace": projectplace})
    elif keyword == "staffmonitor/":
        if request.method == "POST":
            reporteduser = request.POST.get("reporteduser")
            reportuser = request.POST.get("reportuser")
            placename = request.POST.get("placename")
            placeid = request.POST.get("placeid")
            reportdate = request.POST.get("reporttime")
            monitorimg = request.FILES.get("monitorimg")
            info = MonitorInfomation.objects.create(reporteduser=reporteduser, reportuser=reportuser,
                                                    placename=placename, placeid=placeid,
                                                    reportdate=reportdate, monitorimg=monitorimg)
            print(info.nid)
        return render(request, "administrator/staffMonitor.html", {"user": request.user})
    elif keyword == "staffmanage/":
        if request.method == "POST":

            response = {"msg": None}
            noticeinfo = request.POST.get("noticeinfo")

            notice = Notice.objects.create(msg=noticeinfo)
            if notice:
                response["msg"] = "T"
            else:
                response["msg"] = None
            return JsonResponse(response)
        userdict1 = []
        userdict2 = []
        userList1 = User.objects.filter(department_id=1).all()
        userList2 = User.objects.filter(department_id=2).all()
        for user1 in userList1:
            userdict1.append(user1)
        for user2 in userList2:
            userdict2.append(user2)

        datas = Notice.objects.all()
        notices = datas[datas.count() - 5:datas.count()]  # 获取最新的五条通知
        return render(request, "administrator/staffManage.html",
                      {"user": loginUser, "notices": notices, "userdict1": userdict1, "userdict2": userdict2})

    elif keyword == "reportInfo/":
        infoList=MonitorInfomation.objects.all()
        return render(request,"administrator/reportList.html",{"infoList":infoList})

    elif keyword == "user/":
        print("keyword",keyword)
        reportinfo = MonitorInfomation.objects.filter(reporteduser="user").first()
        return render(request, "administrator/reportInfo.html", {"user": request.user, "reportinfo": reportinfo})
    elif keyword == "firmuser/":
        print("keyword",keyword)
        reportinfo = MonitorInfomation.objects.filter(reporteduser="firmuser").first()
        return render(request, "administrator/reportInfo.html", {"user": request.user, "reportinfo": reportinfo})

    # elif keyword == "reportInfo/":
    #     reportinfo = MonitorInfomation.objects.all().first()
    #     return render(request, "administrator/reportInfo.html", {"user": request.user, "reportinfo": reportinfo})

    elif keyword == "set/":
        userinfo = User.objects.filter(nid=loginUser.user_id).first()
        users = User.objects.filter(nid=loginUser.nid).first()
        projects = users.project.all()
        # for project in projects:
        #     print(project.name)
        return render(request, "administrator/set.html",
                      {"user": request.user, "projects": projects, "userinfo": userinfo})


def firm(request, keyword):
    print("keyword", keyword)
    loginUser = request.user
    # salarylist = []
    if keyword == "project/":
        projects = Project.objects.filter(company_id=loginUser.user.company_id)
        userlist = User.objects.filter(company_id=loginUser.user.company_id)
        print(type(projects))
        return render(request, "firm/project.html", {"user": loginUser, "projects": projects, "userlist": userlist})

    elif keyword == "salary/":
        if request.method == "POST":
            # print("here")
            # salarylist.clear()
            date = request.POST.get("date")
            # print(type(date))
            # salarydate = datetime.strptime(date, "%Y-%m-%d")

            # print(type(salarydate))
            # salaryinfos = Salary.objects.filter(belongmonth=salarydate)

            # for salaryinfo in salaryinfos:
            #     salarylist.append(salaryinfo)
            # print("length", len(salarylist))
            request.session["date"] = date
            return redirect("/firm/salarydetail/")
        return render(request, "firm/salary.html", {"user": request.user})
    elif keyword == "set/":
        company = Company.objects.filter(nid=loginUser.user.company_id).first()
        # print(company.cname)
        return render(request, "firm/set.html", {"user": loginUser, "company": company})
    elif keyword == "salarydetail/":
        date = request.session.get("date")
        salarydate = datetime.strptime(date, "%Y-%m-%d")
        salaryinfos = Salary.objects.filter(belongmonth=salarydate)
        return render(request, "firm/salarydetail.html", {"salaryinfos": salaryinfos})
    elif keyword == "user/":
        print("keyword", keyword)
        publishdetail = MonitorInfomation.objects.filter(reporteduser="user").first()
        print("publishdetail", type(publishdetail))
        return render(request, "firm/publishdetail.html", {"reportinfo": publishdetail})
        # return HttpResponse("ok")
    elif keyword == "firmuser/":
        publishdetail = MonitorInfomation.objects.filter(reporteduser="firmuser").first()
        print("publishdetail", type(publishdetail))
        return render(request, "firm/publishdetail.html", {"reportinfo": publishdetail})


def introduce(request):
    return render(request, "introduce.html")
