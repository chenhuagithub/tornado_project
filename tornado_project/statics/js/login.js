$('#sub').click(function() {
	//获取信息
	var mobile = document.getElementById('mobile').value;
	var imagecode = document.getElementById('imagecode').value;
	var messagecode = document.getElementById('messagecode').value;
	var password = document.getElementById('password').value;
	var passwordagain = document.getElementById('passwordagain').value;

	//判断信息
	if (mobile == "") {
		alert("号码不能为空");
	} else if (imagecode == "") {
		alert("请输入图片验证码");
	} else if (messagecode == "") {
		alert("请输入手机验证码");
	} else if (password == "") {
		alert("请输入密码");
	} else if (passwordagain == "") {
		alert("请再次输入密码");
	} else if (passwordagain != password) {
		alert("两次密码不一致");
	} else {
		$(function () {
			$.ajax({
				type:"post",
				url:"http://192.168.202.143:8888/login",
				data:{
					mobile: document.getElementById('mobile').value,
					imagecode: document.getElementById('imagecode').value,
					messagecode: document.getElementById('messagecode').value,
					password: document.getElementById('password').value,
					passwordagain: document.getElementById('passwordagain').value,
				},
				dataType:"json",
				success: function (data) {
					alert("提交成功");
				}

			})
		});
		//发送请求
		// $.post(
		// 	'http://192.168.202.143:8888/login',
		// 	{
		// 		mobile: document.getElementById('mobile').value,
		// 		imagecode: document.getElementById('imagecode').value,
		// 		messagecode: document.getElementById('messagecode').value,
		// 		password: document.getElementById('password').value,
		// 		passwordagain: document.getElementById('passwordagain').value,
		// 	},
		// 	function(data, status) {
		// 		alert(status);
		// 	    alert('提交成功');
		// 		// if(data.code==200){
		// 		//     window.location.href="first_page.html";
        //         // }else if(data.code==300){
		// 		//     alert("注册失败");
        //         // }
		// 	}
		// );
	}


});

$('#img').click(function() {
	var code = document.getElementById('img');
	code.src += '?';
});

$("#get_code").click(function() {
	$.post(
		"http://192.168.202.143:8888/mobile", {
			mobile: document.getElementById("mobile").value,
		},
		function(data, status) {
			alert(status);
		}
	);
});

$("#login_now").click(function (e) {
    window.location.href="register.html";
});