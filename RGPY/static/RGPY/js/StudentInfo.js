$(function(){
    var flag = false
    var flag2 = false
    // 默认提交按钮是隐藏的
   $(".submit_userInfo").hide();

   // 默认不显示的项
   $(".hidden_div").hide();

   //  $(".alert_dismissible").show()
    $(".alert-dismissible").hide()

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
        var passwd=$(this).val();
        var username=$("#id_username").val();
        $.ajax({
            url: "/check_passwd?passwd="+passwd+"&username="+username,
            success: function(result){
                if(result == 0){
                    flag = false
                    $(".alert_dismissible1").show();
                }
                else {
                    flag = true
                    $(".alert_dismissible1").hide();
                }
            },
        });

    });

    // 当点击提交按钮时
    $('.submit_userInfo').click(function(){

        var password_new=$("#id_password_new").val();
        var password_new_rep=$("#id_password_new_rep").val();
        if((!password_new && !password_new_rep) || (password_new==password_new_rep)){
            flag2 = true
        }
        if(flag){
            if(flag2){
                $('form').submit();
            }else{
                alert("新密码两次输入不一致");
                return false;
            }
        }else{
            alert("请正确输入旧密码");
            return false;
        }

    });



});
