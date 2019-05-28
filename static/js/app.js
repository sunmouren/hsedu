
var tips = function ($msg, $type, $icon, $from, $align) {
	$type  = $type || 'info';
	$from  = $from || 'top';
	$align = $align || 'center';
	$enter = $type === 'success' ? 'animated fadeInUp' : 'animated shake';

	jQuery.notify({
		icon: $icon,
		message: $msg
	},
	{
		element: 'body',
		type: $type,
		allow_dismiss: true,
		newest_on_top: true,
		showProgressbar: false,
		placement: {
			from: $from,
			align: $align
		},
		offset: 20,
		spacing: 10,
		z_index: 10800,
		delay: 3000,
		timer: 1000,
		animate: {
			enter: $enter,
			exit: 'animated fadeOutDown'
		}
	});
};

/**
 * 页面加载等待
 * @param $mode 'show', 'hide'
 * @author sunmouren
 */
var pageLoader = function ($mode) {
	var $loadingEl = jQuery('#loader-wrapper');
	$mode          = $mode || 'show';

	if ($mode === 'show') {
		if ($loadingEl.length) {
			$loadingEl.fadeIn(250);
		} else {
			jQuery('body').prepend('<div id="loader-wrapper"><div id="loader"></div></div>');
		}
	} else if ($mode === 'hide') {
		if ($loadingEl.length) {
			$loadingEl.fadeOut(250);
		}
	}

	return false;
};

function vwp(player, progress, cid, vid, url) {
    var t0;
    var t1=0, t2=progress;
    var isUpdate = true;
    var isAchieve = false;

    function timer() {
        t1 += 1;
        if (t1 >= t2){
            updateProgress();
        }
    }

    function updateProgress() {
        t2 += 1;
        var t4 = parseInt(t2 / parseInt(player.duration) * 100);
        if (t4 <= 100){
            $('#vwp').text(t4);
        }
        if (t2 % 60 === 0) {
            submitProgress();
        }

    }

    player.on('play', function () {
        t0 = setInterval(function () {
            if (isUpdate && !isAchieve){
                timer();
            }
        }, 1000);
    });



    player.on('pause', function () {
        window.clearInterval(t0);
    });

    player.on('seeked', function () {
       var t5 = parseInt(player.currentTime);
       if (t5 <= t2){
           t1 = t5;
           isUpdate = true;
       }else{
           isUpdate = false;
       }
    });

    player.on('ended', function () {
        if (isUpdate){
             submitProgress();
        }
    });



    function submitProgress() {
        if (t1 > parseInt(player.duration)){
            t1 = parseInt(player.duration)
        }
        $.ajax({
            cache: false,
            type: 'POST',
            url: url,
            data: {'duration': parseInt(player.duration), 'progress': t1, 'cid': cid, 'vid':vid},
            async: true,
            success: function(data){
                if (data['msg'] === 'ok'){
                    isAchieve = true;
                }
            }
        });
    }


}

$(document).ready(function () {
    // 登录
    $('button.user-login').click(function () {
        var username =  $.trim($('input.username').val());
        var password =  $.trim($('input.password').val());

        // var isEmail = /^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$/;
        // if (!(isEmail.test(username))){
        //     tips('邮箱格式不正确~', 'danger');
        //     return false;
        // }

        if (username === '' || password === ''){
            tips('邮箱或用户名、密码都不能为空', 'danger');
            return false;
        }

        $.ajax({
            cache: false,
            type: 'POST',
            url: '/user/login/',
            data: {'username': username, 'password': password},
            async: true,
            success: function (data) {
                if (data['msg'] === 'ok'){
                    tips('登录成功，页面即将刷新~', 'success');
                    setTimeout(function () {
                        location.reload();
                    }, 1500);
                    return true;
                } else {
                    tips('登录失败，请检查用户名或邮箱、密码，再试一次吧。', 'danger');
                    return false;
                }
            }
        });
    });
    // 注册
    $('button.user-register').click(function () {
        var email =  $.trim($('input.register-email').val());
        var password1 =  $.trim($('input.register-password1').val());
        var password2 =  $.trim($('input.register-password2').val());
        var isEmail = /^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$/;
        if (!(isEmail.test(email))){
            tips('邮箱格式不正确~', 'danger');
            return false;
        }

        if (email === '' || password1 === '' || password2 === ''){
            tips('邮箱、密码、确认密码都不能为空', 'danger');
            return false;
        }

        $.ajax({
            cache: false,
            type: 'POST',
            url: '/user/register/',
            data: {'email': email, 'password1': password1, 'password2': password2},
            async: true,
            success: function (data) {
                if (data['msg'] === 'ok'){
                    tips('注册成功，页面即将刷新~', 'success');
                    setTimeout(function () {
                        location.reload();
                    }, 1500);
                    return true;
                }
                if (data['msg'] === 'ko'){
                    tips('诶呀~，注册失败，请重新检查邮箱和密码，再试一次吧。', 'danger');
                    return false;
                }

                if (data['msg'] === 'exists'){
                    tips('诶呀~，邮箱已经被注册。', 'danger');
                    return false;
                }

                 if (data['msg'] === 'mismatch'){
                    tips('诶呀~，两次密码不一致。', 'danger');
                    return false;
                }
            }
        });
    });


    // 订阅班级
    $('#subscribe-modal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget);
        var title = button.data('title');
        var cgid = button.data('cgid');
        var modal = $(this);
        var submitSignInBtn = modal.find('.modal-body button');

        modal.find('.modal-title').text(title);
        submitSignInBtn.data('cgid', cgid);
    });

    $('button.subscribe').click(function () {
        var cgid = $(this).data('cgid');
        var code = $.trim($('input.subscribe-code').val());
        if (code === ''){
            tips('签到码不能为空~', 'danger');
            return false;
        }
        $.ajax({
            cache: false,
            type: 'POST',
            url: '/course/subscribe/',
            data: {'cgid':cgid, 'code': code},
            async: true,
            success: function (data) {
                if(data['msg'] === 'ok'){
                    tips('订阅成功, 页面即将刷新~', 'success');
                    setTimeout(function () {
                        location.reload();
                    }, 1500);
                    return true;
                } else {
                    tips('订阅失败, 请检查邀请码是否正确~', 'danger');
                    return false;
                }
            }
        });
    });

    // 喜欢评论
    $('button.like').click(function () {
        var $this = $(this);
        var cid = $this.data('cid');
        var action = $this.data('action');
        var likeCount = parseInt($this.find('span.like-count').text());
        $.ajax({
            cache: false,
            type: 'POST',
            url: '/comment/like/',
            data: {'cid': cid, 'action': action},
            async: true,
            success: function (data) {
                if (data['msg'] === 'ok'){
                    $this.data('action', action === 'like' ? 'unlike' : 'like');
                    if (action === 'like'){
                        $this.find('span.like-heart').html('<i class="fa fa-heart" aria-hidden="true"></i>');
                        $this.find('span.like-count').text(likeCount + 1);
                    } else {
                        $this.find('span.like-heart').html('<i class="fa fa-heart-o" aria-hidden="true"></i>');
                        $this.find('span.like-count').text(likeCount - 1);
                    }
                }
            }
        });
    });

    // 标记未读通知未已读
     $('a.mark-unread').click(function () {
        var nid = $(this).data('nid');
        $.ajax({
            cache: false,
            type: 'POST',
            url: '/comment/notifications/',
            data: {'nid': nid},
            async: true,
            success: function (data) {
                if (data['msg'] === 'ok'){
                    tips('标记成功, 页面即将刷新~', 'success');
                    setTimeout(function () {
                        location.reload();
                    }, 1500);
                    return true;
                } else {
                    tips('操作失败，请稍后在重试', 'danger');
                    setTimeout(function () {
                        location.reload();
                    }, 1500);
                    return false;
                }
            }
        });
     });
});


// 判断是否为空文本
function isEmptyText() {
    for (var i = 0; i < arguments.length; i++){
        if ($.trim(arguments[i]) === ''){
            return true;
        }
    }
}


// 预览图片
function imgPreview(id_img, id_preview) {
    $(id_img).on('change', function (e) {
    //获取图片资源
        var file = e.target.files[0];
        // 只选择图片文件
        if (!file.type.match('image.*')) {
            tips('选择文件为图片类型', 'danger');
            return false;
        }

        var reader = new FileReader();
        // 读取文件
        reader.readAsDataURL(file);
        // 渲染文件
        reader.onload = function(arg) {
            var img = '<img class="img-warp rounded box-shadow" src="' + arg.target.result + '" alt="preview"/>';
            $(id_preview).empty().append(img);
        }
    });
}


// 上传图片到七牛云
function uploadImage(kargs) {
    pageLoader('show');
    var imgUrl;
    var md5_name = hex_md5(new Date().getTime() + kargs.file.name);
    var key = 'image/' + kargs.username + '/' + md5_name + '.' + kargs.file.name.split('.')[1];
    var putExtra = {
      fname: "",
      params: {},
      mimeType: [] || null
    };

    var config = {
      useCdnDomain: false,
      region: null
    };

    var next = function (res) {
        // 暂无相关操作, 原本是用来显示加载圈圈的
    };
    var error = function (err) {
        pageLoader('hide');
    };
    var complete = function (res) {
        imgUrl = res.key;
        kargs.saveUpload(imgUrl);
    };
    var observer = {
        next: next,
        error: error,
        complete: complete
    };

    var observable = qiniu.upload(kargs.file, key, kargs.token, putExtra, config);
    var subscription = observable.subscribe(observer);
}

// 上传视频到七牛云
function uploadVideo(kargs) {
    pageLoader('show');
    var vdieoUrl;
    var md5_name = hex_md5(new Date().getTime() + kargs.file.name);
    var key = 'video/' + kargs.username + '/' + md5_name + '.' + kargs.file.name.split('.')[1];
    console.log(key);
    var putExtra = {
        fname: "",
        params: {},
        mimeType: null
    };
    var config = {
      useCdnDomain: true,
      retryCount: 6,
    };

    var next = function (res) {
        // 暂无相关操作, 原本是用来显示加载圈圈的
    };
    var error = function (err) {
        pageLoader('hide');
    };
    var complete = function (res) {
        vdieoUrl = res.key;
        kargs.saveUpload(vdieoUrl);
    };
    var observer = {
        next: next,
        error: error,
        complete: complete
    };

    var observable = qiniu.upload(kargs.file, key, kargs.token, putExtra, config);
    var subscription = observable.subscribe(observer);
}


// 上传视频到七牛云
function uploadResource(kargs) {
    pageLoader('show');
    var resourceUrl;
    var md5_name = hex_md5(new Date().getTime() + kargs.file.name);
    var key = 'resource/' + kargs.username + '/' + md5_name + '.' + kargs.file.name.split('.')[1];
    console.log(key);
    var putExtra = {
        fname: "",
        params: {},
        mimeType: null
    };
    var config = {
      useCdnDomain: true,
      retryCount: 6,
    };

    var next = function (res) {
        // 暂无相关操作, 原本是用来显示加载圈圈的
    };
    var error = function (err) {
        pageLoader('hide');
    };
    var complete = function (res) {
        resourceUrl = res.key;
        kargs.saveUpload(resourceUrl);
    };
    var observer = {
        next: next,
        error: error,
        complete: complete
    };

    var observable = qiniu.upload(kargs.file, key, kargs.token, putExtra, config);
    var subscription = observable.subscribe(observer);
}
