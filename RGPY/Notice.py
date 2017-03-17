from RGPY.models import NEWS


class NOTICE:
    def __init__(self, user, type=1, *argv, **kw):
        self.user = user
        self._infotype = type

        for k, v in kw.items():
            setattr(self, k, v)

    def get_info(self):
        if self._infotype == 1:
            # 任务申请通知, 初始化还需要传入  任务对象
            self._info = "您已报名成功:%s,请耐心等待通知" % (self.task.desc),
        elif self._infotype == 2:
            # 任务 (是否)通过申请的通知
            # 初始化还需要传入 任务对象 和 approval(是否通过)
            if self.approval:
                self._info = '您申请的任务%s已经通过申请,请务必在%s完成任务' % (self.task, self.task.task_time)
            else:
                self._info = '您申请的任务%s,没有通过申请,请选择别的任务' % (self.task)
        elif self._infotype == 3:
            # 任务完成通知, 初始化还需要传入  任务对象
            self._info = '您完成的任务:%s已经增加了时长,您现在的总时长为:%s' % (self.task, self.user.score)
        elif self._infotype == 4:
            # 自申请任务通知
            self._info = '您申请的加分任务:%s 已经提交成功，请耐心等候审核' % (self.apply.desc,)
        else:
            pass

    def mess_send(self):
        NEWS.objects.create(reader=self.user, info=self._info)

    def email_send(self):
        pass

    def phone_send(self):
        pass

    def send_notice(self):
        self.get_info()
        self.mess_send()
        self.email_send()
        self.phone_send()
