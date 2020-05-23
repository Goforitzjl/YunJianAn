from django.db import models
from django.contrib.auth.models import AbstractUser


class User(models.Model):
    nid = models.AutoField(primary_key=True)
    tel = models.CharField(verbose_name="联系电话", max_length=32, null=True)
    address = models.CharField(verbose_name="家庭住址", max_length=64, null=True)
    userid = models.CharField(verbose_name="员工编号", max_length=32, null=True)
    name = models.CharField(verbose_name="姓名", max_length=32, null=True)
    personid = models.IntegerField(verbose_name="员工编号", null=True)
    idcard = models.CharField(verbose_name="身份证号码", max_length=256, null=True)
    salaryid = models.CharField(verbose_name="工资卡卡号", max_length=256, null=True)
    bank = models.CharField(verbose_name="工资卡所属银行", max_length=256, null=True)
    gender = models.CharField(verbose_name="性别", max_length=10, null=True)
    introducerid = models.IntegerField(verbose_name="引入人号码", default=0, null=True)
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True, null=True)
    department = models.ForeignKey(verbose_name="所属部门", to="Departmemt", to_field="nid", on_delete=models.CASCADE,
                                   null=True)

    userwork = models.ManyToManyField(
        to="Userwork",
        through="Usertowork",
        through_fields=("user", "userwork")
    )

    project = models.ManyToManyField(
        to="Project",
        through="Usertoproject",
        through_fields=("user", "project")
    )

    company = models.ForeignKey(to="Company", to_field="nid", on_delete=models.CASCADE, null=True, default=1)


class MonitorInfomation(models.Model):
    nid = models.AutoField(primary_key=True)
    reporteduser = models.CharField(verbose_name="被举报人", max_length=32, null=True)
    placename = models.CharField(verbose_name="场地名称", max_length=64, null=True)
    placeid = models.CharField(verbose_name="场地ID", max_length=256, null=True)
    createdate = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    reportdate = models.CharField(verbose_name="举报时间", max_length=32, null=True)
    reportuser = models.CharField(verbose_name="举报人", max_length=32, null=True)
    monitorimg = models.FileField(verbose_name="监控图片", upload_to="MonitorImg/", default="MonitorImg/default.png",
                                  null=True)


class Notice(models.Model):
    nid = models.AutoField(primary_key=True)
    msg = models.CharField(verbose_name="通知", max_length=256, null=True)
    create_date = models.DateTimeField(verbose_name="发布时间", auto_now_add=True, null=True)


class UserLogin(AbstractUser):
    nid = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="名字", max_length=32, null=True)
    createtime = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    avatar = models.FileField(verbose_name="头像", upload_to="avatars/", default="avatars/default.png", null=True)
    user = models.OneToOneField(to="User", to_field="nid", on_delete=models.CASCADE, null=True)
    is_firmuser = models.BooleanField(verbose_name="是否是企业账号", null=True)


class Userwork(models.Model):
    nid = models.AutoField(primary_key=True)
    # workplaceid = models.IntegerField(verbose_name="工作场地号码", default=0, null=True)
    projectplace = models.ForeignKey(verbose_name="工作的场地编号", to="Projectplace", to_field="nid",
                                     on_delete=models.CASCADE, null=True)
    bossid = models.CharField(verbose_name="责任人号码", null=True, max_length=256)
    begintime = models.DateTimeField(verbose_name="工作开始时间", null=True)
    endtime = models.DateTimeField(verbose_name="工作结束时间", null=True)
    description = models.CharField(verbose_name="工作简介", max_length=256, null=True)


class Usertowork(models.Model):
    nid = models.AutoField(primary_key=True)
    user = models.ForeignKey(verbose_name="用户", to="User", to_field="nid", on_delete=models.CASCADE, null=True)
    userwork = models.ForeignKey(verbose_name="用户工作", to="Userwork", to_field="nid", on_delete=models.CASCADE,
                                 null=True)

    class Meta:
        unique_together = [
            ("user", "userwork")
        ]


class Departmemt(models.Model):
    nid = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="部门名称", max_length=256, null=True)
    bossid = models.CharField(verbose_name="部门负责人号码", max_length=256, null=True)
    project = models.ForeignKey(verbose_name="所属项目", to="Project", to_field="nid", on_delete=models.CASCADE, null=True)
    bossname = models.CharField(verbose_name="部门负责人名字", max_length=32, null=True)
    departmentid = models.CharField(verbose_name="部门编号", max_length=64, null=True)


class Project(models.Model):
    nid = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="项目名称", max_length=256, null=True)
    bossid = models.CharField(verbose_name="项目负责人", max_length=256, null=True)
    address = models.CharField(verbose_name="项目地址", max_length=256, null=True)
    description = models.CharField(verbose_name="项目简介", max_length=1024, null=True)
    begintime = models.DateTimeField(verbose_name="项目开始时间", null=True)
    endtime = models.DateTimeField(verbose_name="项目结束时间", null=True)
    company = models.ForeignKey(verbose_name="所属公司", to="Company", to_field="nid", on_delete=models.CASCADE, null=True)


class Usertoproject(models.Model):
    nid = models.AutoField(primary_key=True)
    user = models.ForeignKey(verbose_name="用户", to="User", to_field="nid", on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(verbose_name="项目", to="Project", to_field="nid", on_delete=models.CASCADE, null=True)

    class Meta:
        unique_together = [
            ("user", "project")
        ]


class Company(models.Model):
    nid = models.AutoField(primary_key=True)
    cname = models.CharField(verbose_name="公司中文名称", max_length=256, null=True)
    ename = models.CharField(verbose_name="公司英文名称", max_length=256, null=True)
    address = models.CharField(verbose_name="公司地址", max_length=256, null=True)
    tel = models.CharField(verbose_name="公司电话", max_length=256, null=True)
    email = models.EmailField(verbose_name="公司邮箱", max_length=256, null=True)
    createtime = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    shortname = models.CharField(verbose_name="简称", max_length=32, null=True)
    createaddress = models.CharField(verbose_name="注册地点", max_length=32, null=True)

class Salary(models.Model):
    basicsalary = models.IntegerField(verbose_name="基本工资", null=True)
    performance = models.IntegerField(verbose_name="绩效", null=True)
    publishment = models.IntegerField(verbose_name="罚款", null=True)
    socialsecurity = models.IntegerField(verbose_name="社保扣款", null=True)
    insurances = models.IntegerField(verbose_name="五险一金", null=True)
    tax = models.IntegerField(verbose_name="税收", null=True)
    finalsalary = models.IntegerField(verbose_name="实发工资", null=True)
    belongmonth = models.DateTimeField(verbose_name="工资归属月", null=True)
    releasedate = models.DateTimeField(verbose_name="发放日期", null=True)
    sickleave = models.IntegerField(verbose_name="病假", null=True)

    company = models.ForeignKey(to="Company", to_field="nid", on_delete=models.CASCADE, null=True)
    user = models.OneToOneField(to="User", to_field="nid", on_delete=models.CASCADE, null=True)


class Projectplace(models.Model):
    nid = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="场地名称", max_length=256, null=True)
    bossid = models.CharField(verbose_name="责任人", max_length=256, null=True)
    address = models.CharField(verbose_name="场地地址", max_length=256, null=True)
    pictures = models.FileField(verbose_name="场地照片", upload_to="propictures/", default="propictures/default.png")
    description = models.CharField(verbose_name="场地详情", max_length=1024, null=True)
    project = models.ForeignKey(to="Project", to_field="nid", on_delete=models.CASCADE, null=True)


class Camera(models.Model):
    nid = models.AutoField(primary_key=True)
    projectplace = models.ForeignKey(to="Projectplace", to_field="nid", on_delete=models.CASCADE, null=True)


class Image(models.Model):
    nid = models.AutoField(primary_key=True)
    createdata = models.DateTimeField(verbose_name="拍摄时间", null=True)
    # projectplace = models.ForeignKey(to="Projectplace", to_field="nid", on_delete=models.CASCADE, null=True)
    camera = models.ForeignKey(to="Camera", to_field="nid", on_delete=models.CASCADE, null=True)
    safenumber = models.IntegerField(verbose_name="安全人数", default=0, null=True)
    dangernumber = models.IntegerField(verbose_name="危险人数", default=0, null=True)
