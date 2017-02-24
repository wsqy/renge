$(function(){
    $("button[name='user_del']").click(function(){
        var user = $(this).parents("tr");
        var id = user.attr("id");
        var username = user.children("td:first-child").text();
        // alert(username);
        // alert(id);
        $.ajax({url:"/user_del/"+id, success:function(result){
            if(result==1){
                alert("删除用户 "+username+" 成功");
                window.location.reload();
            }else{
                alert("重置失败,非法操作");
            }
        }});
    });
});
