function changepic(){
    var reads=new FileReader();
    f=document.getElementById('up_img').files[0];
    reads.readAsDataURL(f);
    reads.onload=function(e){
        document.getElementById('show_blogs_ico').src=this.result;
    };
    // $(".show-blogs")
}

// $(".topnav").autoHidingNavbar({
//     // 配置参数
//     animationDuration=400
//   });