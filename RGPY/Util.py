def get_user_info(request):
    try:
        u = request.user.ouruser.level
        res = {
            "type": u.level,
            "username": u.username,
            "name": u.username,
            "_U": u,
        }
        # 如果设置了姓名  则用姓名替换 username
        if u.first_name:
            res["name"] = u.first_name
    except Exception as e:
        res = {
            "type": '-1',
            "username": '-1',
            "name": '-1',
        }
    finally:
        return res
