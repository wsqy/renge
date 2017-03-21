import ALIDAYU
req = ALIDAYU.MESSAGE()
req.extend = ""
req.sms_type = "normal"
req.sms_free_sign_name = "人格培养管理平台"
req.sms_param = {"task_name": "test任务"}
req.rec_num = "18450098280,18450098187,13061968923"
req.sms_template_code = "SMS_56550520"
req.SMS_SEND()
