
var tips = function ($msg, $type, $icon, $from, $align) {
	$type  = $type || 'info';
	$from  = $from || 'top';
	$align = $align || 'center';
	$enter = $type == 'success' ? 'animated fadeInUp' : 'animated shake';

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
 * @author yinq
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
                if (data['msg'] == 'ok'){
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

        if (username == '' || password == ''){
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
                if (data['msg'] == 'ok'){
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
        var email =  $.trim($('input.register-emial').val());
        var password1 =  $.trim($('input.register-password1').val());
        var password2 =  $.trim($('input.register-password2').val());
        var isEmail = /^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$/;
        if (!(isEmail.test(email))){
            tips('邮箱格式不正确~', 'danger');
            return false;
        }

        if (email == '' || password1 == '' || password2 == ''){
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
                if (data['msg'] == 'ok'){
                    tips('注册成功，页面即将刷新~', 'success');
                    setTimeout(function () {
                        location.reload();
                    }, 1500);
                    return true;
                }
                if (data['msg'] == 'ko'){
                    tips('诶呀~，注册失败，请重新检查邮箱和密码，再试一次吧。', 'danger');
                    return false;
                }

                if (data['msg'] == 'exists'){
                    tips('诶呀~，邮箱已经被注册。', 'danger');
                    return false;
                }

                 if (data['msg'] == 'mismatch'){
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
        // var cga = $('a#cg-'+cgid);

        if (code == ''){
            tips('签到码不能为空~', 'danger');
            return false;
        }

        // var subscibeCount = parseInt($('span#subscribe-count-'+cgid).text());

        $.ajax({
            cache: false,
            type: 'POST',
            url: '/course/subscribe/',
            data: {'cgid':cgid, 'code': code},
            async: true,
            success: function (data) {
                if(data['msg'] == 'ok'){
                    tips('订阅成功, 页面即将刷新~', 'success');
                    // cga.html('<i class="fa fa-check"></i> 已订阅');
                    // cga.addClass('text-success');
                    // cga.data('target', '');
                    // cga.data('toggle', '');
                    // $('span#subscribe-count-'+cgid).text(subscibeCount + 1);
                    // $('div#subscribe-modal').modal('hide');
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

    // $('div.class-grade-list').find('a.class-grade-item').click(function () {
    //     $this = $(this);
    //     // var login = $this.data('login');
    //     // if (login == 'unlogin'){
    //     //     console.log('unlogin');
    //     //     return false;
    //     // }
    //     var classId = $this.data('cgid');
    //     // var action = $this.data('action');
    //     var subscibeCount = parseInt($('span#subscribe-count-'+classId).text());
    //     $.ajax({
    //         cache: false,
    //         type: 'POST',
    //         url: '/course/subscribe/',
    //         data: {'classId': classId, 'action': action},
    //         async: true,
    //         success: function (data) {
    //             if(data['msg'] == 'ok'){
    //                 $this.data('action', action == 'subscribe' ? 'unsubscribe' : 'subscribe');
    //                 if (action == 'subscribe'){
    //                     $this.html('<i class="fa fa-check"></i> 已订阅');
    //                     $('span#subscribe-count-'+classId).text(subscibeCount + 1);
    //                 } else {
    //                     $this.html('<i class="fa fa-plus"></i> 订阅');
    //                      $('span#subscribe-count-'+classId).text(subscibeCount - 1);
    //                 }
    //             }
    //         }
    //     });
    // });


    // 问答模态
    $('#review-modal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget);
        var title = button.data('title');
        var pid = button.data('pid');
        var vid = button.data('vid');
        var modal = $(this);
        var sendReviewBtn = modal.find('.modal-body button');

        modal.find('.modal-title').text(title);
        sendReviewBtn.data('pid', pid);
        sendReviewBtn.data('vid', vid);
    });
    $('button.send-review').click(function () {
        var $this = $(this);
        var pid = $this.data('pid');
        var vid = $this.data('vid');
        var content = $.trim($('textarea.review-content').val());

        if (content == ''){
            tips('内容不能为空~', 'danger');
            return false;
        }

        $.ajax({
            cache: false,
            type: 'POST',
            url: '/comment/add/',
            data: {'pid': pid, 'vid': vid, 'content': content},
            async: true,
            success: function (data) {
                if (data['msg'] == 'ok'){
                    var reviewCount = $('span.review-count');
                    reviewCount.text(parseInt(reviewCount.text()) + 1);
                    $('div.review-list').prepend(data['cmt']);
                    $('textarea.review-content').val("");
                    $('div#review-modal').modal('hide');
                    $('p.no-review').remove();
                    tips('发布成功~', 'success');
                    return true;
                } else {
                    tips('发布失败, 请刷新后重试', 'danger');
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
                if (data['msg'] == 'ok'){
                    $this.data('action', action == 'like' ? 'unlike' : 'like');
                    if (action == 'like'){
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

     // 订阅者进行签到模态
    $('#sub-sign-modal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget);
        var title = button.data('title');
        var sid = button.data('sid');
        var modal = $(this);
        var submitSignInBtn = modal.find('.modal-body button');

        modal.find('.modal-title').text(title);

        submitSignInBtn.data('sid', sid);
    });
    $('button.sub-sign').click(function () {
        var $this = $(this);
        var sid = $this.data('sid');
        var code = $.trim($('input.sub-sign-code').val());
        if (code == ''){
            tips('签到码不能为空~', 'danger');
            return false;
        }
        $.ajax({
            cache: false,
            type: 'POST',
            url: '/course/sub/sign/',
            data: {'sid': sid, 'code': code},
            async: true,
            success: function (data) {
                if(data['msg'] == 'ok'){
                    tips('签到成功，页面即将刷新~', 'success');
                    setTimeout(function () {
                        location.reload();
                    }, 1500);
                    return true;
                } else {
                    tips('签到失败, 请检查签到码是否正确~', 'danger');
                    return false;
                }
            }
        });
    });

    // 改变签到状态
    $('button.cos-sign').click(function () {
       var $this = $(this);
       var sid = $this.data('sid');
       var action = $this.data('action');
       $.ajax({
           cache: false,
           type: 'POST',
           url: '/course/cos/sign/',
           data: {'sid': sid, 'action': action},
           async: true,
           success: function (data) {
               if (data['msg'] == 'ok') {
                   location.reload();
                   return true;
               } else {
                   tips('哎呀~操作失败了, 请再试一次吧。', 'danger');
                   return false;
               }
           }
       });
    });
    // 添加签到
    $('button.add-sign').click(function () {
        var $this = $(this);
        var cgid = $this.data('cgid');
        var code = $('input.sign-code').val();
        if (code == ''){
            tips('签到码不能为空~', 'danger');
            return false;
        }
        $.ajax({
            cache: false,
            type: 'POST',
            url: '/course/add/sign/',
            data: {'cgid': cgid, 'code': code},
            async: true,
            success: function (data) {
                if (data['msg'] == 'ok'){
                    tips('签到成功，页面即将刷新~', 'success');
                    setTimeout(function () {
                        location.reload();
                    }, 1500);
                } else {
                    tips('哎呀~操作失败了, 请刷新后再试一次吧。', 'danger');
                }
            }
        });
    });

    // 提交选择题
    $('button.sc-submit').click(function () {
        var $this = $(this);
        var scid = $this.data('scid');
        var answer = $('input.sc'+scid+ ':checked').val();
        if(null == answer){
            tips('选项不能为空', 'danger');
            return false;
        }
        $.ajax({
            cache: false,
            type: 'POST',
            url: '/test/sub/sc/',
            data: {'scid': scid, 'answer': answer},
            async: true,
            success: function (data) {
                if(data['msg'] == 'ok'){
                    tips('提交成功~', 'success');
                    $('div#singlechoice-'+scid).remove();
                    return true;
                }else {
                    tips('提交出错, 请检查后在试一次吧~', 'danger');
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
                if (data['msg'] == 'ok'){
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
