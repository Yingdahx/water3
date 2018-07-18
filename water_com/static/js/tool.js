

if (typeof $ != "undefined"){
;$(function(){

var win = $(window);
var isIE = !!window.ActiveXObject;
var isIE6 = isIE && !window.XMLHttpRequest;
var isIE8 = isIE && !!document.documentMode;
var isIE7 = isIE && !isIE6 && !isIE8;

	
//通知
$('.ann_li').hover(function(){
$(this).children('.sec_ann').fadeIn();
},function(){
$(this).children('.sec_ann').fadeOut();
});
//

//删除文件
$('.file_del a').click(function(){
$(this).parents().siblings('.file_ok').fadeOut();
});
//
	
//下拉选择
        (function () {
            $(".divselect").click(function () {
                $(this).toggleClass("divselect_open");
            });
            $(".divselect li").click(function () {
                $(this).closest(".divselect").find("cite").text($(this).text());
            });
            // 点击其它地方搜索消失
            $(window).on("click", function (e) {
                if ($(e.target).parents(".divselect").length == 0) {
                    $(".divselect").removeClass("divselect_open");
                } else {
                    e.stopPropagation();
                }
            });
        })();
        //end 下拉选择

//点击高亮
$('.click_ul li').click(function(){
$(this).addClass('on').siblings().removeClass('on');
});
//



});

//文本框
function placeholder(input){
	var placeholder = input.attr("placeholder"),
		defaultValue = input.defaultValue;
	if(!defaultValue){
		input.val() == "" ?	input.val(placeholder).addClass("phcolor") : 0;
	}
	input.focus(function(){
		input.val() == placeholder ? $(this).val("") : 0;
	});
	input.blur(function(){
		input.val() == "" ? $(this).val(placeholder).addClass("phcolor") : 0;
	});
	input.keydown(function(){
		$(this).removeClass("phcolor");
	});
}
;$(function(){
	supportPlaceholder="placeholder"in document.createElement("input");
	if(!supportPlaceholder){
		$("input").each(function(){
			var type = $(this).attr("type");
			text = $(this).attr("placeholder");
			if(type == "text" || type == "number" || type == "search" || type == "email" || type == "date" || type == "url"){
				placeholder($(this));
			}
		});
	}
});
//end文本框

};
// end jq