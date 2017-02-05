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

});
