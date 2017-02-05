$(function(){
    // 默认提交按钮是隐藏的
   $(".submit_userInfo").hide();

   // 默认不显示的项
   $(".hidden_div").hide();

   // 当点击 个人信息修改 按钮时
   $(".editor_userInfo").click(function(){
       //   设置一些学生可修改的属性值
       $('.Student').attr("disabled",false);
       // 显示 默认不显示的项
       $(".hidden_div").show();

      // 隐藏 个人信息修改 按钮
      $(this).hide();
      //   并显示 提交按钮
      $(".submit_userInfo").show();
    });

    // 异步验证密码是否正确
    $("#id_password").blur(function(){
        var passwd=$("#id_password").val();
        var username=$("#id_username").val();
        console.log(passwd)
        $.ajax({
            url: "http://101.200.46.25:8000/check_passwd?passwd="+passwd+"&username="+username,
            success: function(result){
                if(result == 0){
                    flag = false
                    console.log("错误")
                    $("#id_password").after("<font color=\"green\" size=\"2\">  Correct</font>");
                }
                else {
                    flag = true
                    console.log("正确")
                    $("#id_password").after("<font color=\"red\" size=\"2\">  Wrong</font>");
                }
            },
        });

    });

});
