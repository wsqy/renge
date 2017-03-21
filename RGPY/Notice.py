# -*- coding: utf-8 -*-
from RGPY.models import NEWS
from django.core.mail import send_mail
from django.conf import settings
import sys
import json
import ALIDAYU

req = ALIDAYU.MESSAGE()
req.extend = ""
req.sms_type = "normal"
req.sms_free_sign_name = settings.SMS_FREE_SIGN_NAME


class NOTICE:
    def __init__(self, user, type=1, level=[1], *argv, **kw):
        self.user = user
        self._infotype = type
        self._level = level
        req.rec_num = json.dumps(self.user.phone)

        for k, v in kw.items():
            setattr(self, k, v)

    def get_info(self):
        if self._infotype == 1:
            # 任务申请通知 SMS_56550520, 初始化还需要传入  任务对象
            self._mes_type = "任务申请通知"
            self._info = "您已报名成功:%s,请耐心等待通知" % (self.task.desc),
            req.sms_param = {"task_name": self.task.desc}
            req.sms_template_code = "SMS_56550520"
        elif self._infotype == 2:
            # 任务 (是否)通过申请的通知
            # 初始化还需要传入 任务对象 和 approval(是否通过)
            if self.approval:
                self._mes_type = "任务通过申请的通知"
                self._info = '您申请的任务%s已经通过申请,请务必在%s完成任务' % (self.task, self.task.task_time)
                req.sms_param = {"task_name": self.task.desc, "time": self.task.task_time}
                req.sms_template_code = "SMS_56725384"
            else:
                # SMS_56580449
                self._mes_type = "任务没有通过申请的通知"
                self._info = '您申请的任务%s,没有通过申请,请选择别的任务' % (self.task)
                req.sms_param = {"task_name": self.task.desc}
                req.sms_template_code = "SMS_56580449"
        elif self._infotype == 3:
            # 任务完成通知  SMS_56585420 , 初始化还需要传入  任务对象
            self._mes_type = " 任务完成通知"
            self._info = '您完成的任务:%s已经增加了时长,您现在的总时长为:%s' % (self.task, self.user.score)
            req.sms_param = {"task_name": self.task.desc, "score": self.task.score}
            req.sms_template_code = "SMS_56585420"
        elif self._infotype == 4:
            # 自申请任务通知   SMS_56735410
            self._mes_type = "自申请任务通知"
            self._info = '您申请的加分任务:%s 已经提交成功，请耐心等候审核' % (self.apply.desc,)
            req.sms_param = {"task_name": self.task.desc}
            req.sms_template_code = "SMS_56735410"
        elif self._infotype == 5:
            # 自申请任务修改通知 SMS_56690321
            self._mes_type = "自申请任务修改通知"
            self._info = '您申请的加分任务:%s 修改已经提交成功，请耐心等候审核' % (self.apply.desc,)
            req.sms_param = {"task_name": self.task.desc}
            req.sms_template_code = "SMS_56690321"
        elif self._infotype == 6:
            # 自申请任务  通过 拒绝通知
            if self.agree_id == 1:
                # SMS_56520506
                self._mes_type = "自申请任务通过通知"
                self._info = '您申请的加分任务:%s 已经成功加分' % (self.apply.desc,)
                req.sms_param = {"task_name": self.apply.desc}
                req.sms_template_code = "SMS_56520506"
            else:
                # SMS_56595465
                self._mes_type = "自申请任务拒绝通知"
                self._info = '您申请的加分任务:%s 被管理员拒绝, 如有疑问 请联系班级管理员' % (self.apply.desc,)
                req.sms_param = {"task_name": self.apply.desc}
                req.sms_template_code = "SMS_56595465"
        elif self._infotype == 7:
            # 密码重置 通知  	SMS_56545361
            self._mes_type = "密码重置 通知"
            self._info = '您的密码已通过管理员重置,为了您的账户安全,请尽快修改'
            req.sms_param = ""
            req.sms_template_code = "SMS_56545361"
        elif self._infotype == 8:
            # 密码修改通知   	SMS_56610389
            self._mes_type = "密码修改通知"
            self._info = '您的密码已成功修改,请妥善保管'
            req.sms_param = ""
            req.sms_template_code = "SMS_56610389"
        else:
            pass

    def mess_send(self):
        NEWS.objects.create(reader=self.user, info=self._info)

    def email_send(self):
        if self.user.email:
            print("send email")
            try:
                email_title = "%s-%s" % (settings.SMS_FREE_SIGN_NAME, self._mes_type)
                send_mail(email_title, self._info, settings.EMAIL_HOST_USER, [self.user.email], fail_silently=False)
            except Exception as e:
                print(e)
        else:
            pass

    def phone_send(self):
        if self.user.phone:
            print("send phone")
            req.rec_num = self.user.phone
            try:
                req.SMS_SEND()
            except Exception as e:
                print(e)
        else:
            pass

    def send_notice(self):
        self.get_info()
        print(4)
        if 1 in self._level:
            print(5)
            self.mess_send()
        if 2 in self._level:
            print(6)
            self.email_send()
        if 3 in self._level:
            print(7)
            self.phone_send()
