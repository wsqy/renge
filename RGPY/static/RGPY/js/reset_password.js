$(function(){
    $("button").click(function(){
        var user = $(this).parents("tr");
        var id = user.attr("id")
        var username = user.children("td:first-child").text()
        alert(username)
        // alert(id);
        $.ajax({url:"/reset_password?userId="+id, success:function(result){
            if(result==1){
                alert("请通知 "+username+" ta的密码已经重置成功！！！新密码为：123456,请尽快修改" + status);
            }else{
                alert("重置失败,非法操作");
            }
        }});
    });
});
