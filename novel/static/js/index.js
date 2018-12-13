var currentCid = 1; // 当前分类 id
var cur_page = 1; // 当前页
var total_page = 1;  // 总页数
var data_querying = true;   // 是否正在向后台获取数据


$(function () {
    // 调用更新新闻
    updatenovelsData()
    // 首页分类切换
    $('.menu li').click(function () {
        var clickCid = $(this).attr('data-cid')
        $('.menu li').each(function () {
            $(this).removeClass('active')
        })
        $(this).addClass('active')

        if (clickCid != currentCid) {
            // 记录当前分类id
            currentCid = clickCid

            // 重置分页参数
            cur_page = 1
            total_page = 1
            updatenovelsData()
        }
    })

    //页面滚动加载相关
    $(window).scroll(function () {

        // // 浏览器窗口高度
        // var showHeight = $(window).height();
        // console.log(showHeight)
        // // 整个网页的高度
        // var pageHeight = $(document).height();
        // console.log(pageHeight)
        //
        // // 页面可以滚动的距离
        // var canScrollHeight = pageHeight - showHeight;
        // console.log("a"+canScrollHeight)
        // // 页面滚动了多少,这个是随着页面滚动实时变化的
        // var nowScroll = $(document).scrollTop();
        // console.log("b"+nowScroll)

//真实内容的高度
      var pageHeight = Math.max(document.body.scrollHeight, document.body.offsetHeight);
      //视窗的高度
      var viewportHeight = window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight || 0;
      //隐藏的高度
      var scrollHeight = window.pageYOffset || document.documentElement.scrollTop || document.body.scrollTop || 0;

        // if ((canScrollHeight - nowScroll) < 100) {
        //     console.log(1)
        if (pageHeight - viewportHeight - scrollHeight < 100) {
            console.log(1)


            // TODO 判断页数，去更新新闻数据
            // 判断页数，去更新新闻数据
            if (!data_querying) {
                console.log(2)

                data_querying = true
                if (cur_page < total_page) {
                    console.log(3)

                    cur_page += 1
                    updatenovelsData()
                }
            }
        }
    })
})

function updatenovelsData() {
    // TODO 更新新闻数据
    // 更新新闻数据
    var params = {
        "cid":currentCid,
        "page":cur_page,
    }
    $.get("/novel_list",params,function(resp){
        data_querying = false
        if (resp.errno == "0"){
            total_page = resp.data.total_page
            if (cur_page == 1){
                $(".list_con").html("")
            }
            // novel_list
            for (var i=0;i<resp.data.novel_list.length;i++) {
                var novels = resp.data.novel_list[i]
                var content = '<li id="novel_list">'
                content += '<a href="/' + novels['_id'] + '" class="novels_pic fl"><img src="../../static/images/test.png" height="168" width="168"></a>'
                content += '<a href="/' + novels['_id']+ '" class="novels_title fl">' + novels['name'] + '</a>'
                // content += '<a href="/' + novels['_id'] + '" class="novels_detail fl">' + novels['content'].slice(0,300) + '</a>'
                content += '<a href="/' + novels['_id'] + '" class="novels_detail fl">' + novels['info'] + '</a>'
                content += '<div class="author_info fl" >'
                content += '<div class="source fl">作者：' + novels.author + '</div>'

                content += '<div class="time fl">' + novels['update_time'] + '</div>'
                content += '</div>'
                content += '</li>'
                $(".list_con").append(content)

            }
        }else {
            alert(resp.errmsg)
        }

})
}



