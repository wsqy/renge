$(function(){
    var flag = false
    var flag2 = false

    $(".alert-dismissible").hide()

    // 异步验证密码是否正确
    $("#id_password").blur(function(){
        var passwd=$(this).val();
        var username=$("#id_username").val();
        $.ajax({
            url: "/check_passwd?passwd="+passwd+"&username="+username,
            success: function(result){
                console.log(result)
                if(result == 0){
                    flag = false
                    $(".alert-dismissible").show();
                }
                else {
                    flag = true
                    $(".alert-dismissible").hidden();
                }
            },
        });

    });

    // 当点击提交按钮时
    $('.change_password').click(function(){

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
