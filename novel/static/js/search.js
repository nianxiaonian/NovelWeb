var currentCid = 1; // 当前分类 id
var cur_page = 1; // 当前页
var total_page = 1;  // 总页数
var data_querying = true;   // 是否正在向后台获取数据

$(function () {


	$('.search_con').submit(function (event) {
	        event.preventDefault()
	        $(this).ajaxSubmit({
	            url: '/search',
	            type: 'get',
	            // headers: {'X-CSRFToken': getCookie('csrf_token')},
	            success: function (result) {
                    if (result.errno == 0) {
                        alert(result)
                        updatenovelsData1(result)
                    } else {
                        alert(result.errmsg)
                    }
                }})
        })
    })



function updatenovelsData1(resp) {
    alert(resp.data)
            // novel_list
                $('.list_con').html("");
            for (var i=0;i<resp.data.novel_list.length;i++) {
                var novels = resp.data.novel_list[i]
                var content = '<li id="novel_list">'
                content += '<a href="/' + novels['_id'] + '" class="novels_pic fl"><img src="../../static/images/test.png" height="168" width="168"></a>'
                content += '<a href="/' + novels['_id']+ '" class="novels_title fl">' + novels['name'] + '</a>'
                content += '<a href="/' + novels['_id'] + '" class="novels_detail fl">' + novels['content'].slice(0,300) + '</a>'
                content += '<div class="author_info fl" >'
                content += '<div class="time fl">' + novels['update_time'] + '</div>'
                content += '</div>'
                content += '</li>'
                $(".list_con").append(content)


        }


}



