function getcity(s) {
    $.get("/getcity", {'procode': s}, function (ret) {
        var content = '';
        $.each(ret, function (i, item) {
            content += '<option value=' + item.fields.code + '>' + item.fields.name + '</option>'
        });
        $('#city').html(content)
    })
}

function getarea(s) {
    $.get("/getarea", {'cityno': s}, function (ret) {
        var content = '';
        $.each(ret, function (i, item) {
            content += '<option value=' + item.fields.name + '>' + item.fields.name + '</option>'
        });
        $('#area').html(content)
    })
}

function getarea2(s) {
    $.get("/getarea", {'cityno': s}, function (ret) {
        var content = '';
        $.each(ret, function (i, item) {
            content += '<option value=' + item.fields.code + '>' + item.fields.name + '</option>'
        });
        $('#area').html(content)
    })
}

function getsecondindustry(s) {
    $.get("/getsecondindustry", {'code': s}, function (ret) {
        var content = '';
        $.each(ret, function (i, item) {
            content += '<option value=' + item.fields.code + '>' + item.fields.name + '</option>'
        });
        $('#dustry2').html(content)
    })
}

$(function () {
    var options = {
        bootstrapMajorVersion: 3,//版本号。3代表的是第三版本
        currentPage: 2, //当前页数
        numberOfPages: 5, //显示页码数标个数
        totalPages: 21, //总共的数据所需要的总页数
        itemTexts: function (type, page, current) {
            //图标的更改显示可以在这里修改。
            switch (type) {
                case "first":
                    return "<<";
                case "prev":
                    return "<";
                case "next":
                    return ">";
                case "last":
                    return ">>";
                case "page":
                    return page;
            }
        },
        tooltipTitles: function (type, page, current) {
            //如果想要去掉页码数字上面的预览功能，则在此操作。例如：可以直接return。
            switch (type) {
                case "first":
                    return "Go to first page";
                case "prev":
                    return "Go to previous page";
                case "next":
                    return "Go to next page";
                case "last":
                    return "Go to last page";
                case "page":
                    return (page === current) ? "Current page is " + page : "Go to page " + page;
            }
        },
        onPageClicked: function (e, originalEvent, type, page) {
            //单击当前页码触发的事件。若需要与后台发生交互事件可在此通过ajax操作。page为目标页数。
            //console.log(e);
            //console.log(originalEvent);
            // console.log(type);
        }
    };
    $("#test").bootstrapPaginator(options);	//进行初始化
});