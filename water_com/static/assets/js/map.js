var site = GetRequest(),lng,lat,zoom
if(site && site['lng']){
    lng = site['lng']
    lat = site['lat']
    zoom = 18
}else{
    lng = 121.392499
    lat = 31.258801
    zoom = 13
}
var map = new AMap.Map('mapCon',{
    resizeEnable: true,
    // mapStyle: 'amap://styles/60248a57a90f1d96733c4e7fb9c48cad',//样式URL
    zoom:zoom,
    center: new AMap.LngLat(lng,lat),
});

//模拟数据
var that = this,markers

getData()
setInterval(function () {
    getData()
},30000)

function getData() {
    $.ajax({
        type:'get',
        url:'http://39.104.85.167:8087/all/',
        success:function (rep) {
            var data
            map.clearMap()
            renderMap(map)
            if(rep&&typeof rep == 'object'&& Object.keys(rep).length != 0 ){
                data = rep.center || [],eleData = rep.right || []
                setEle(eleData)
                if(map.getZoom() < 14){
                    markers = createMarkers(map,data,true)
                }else{
                    markers = createMarkers(map,data,false)
                }
                map.add(markers)

                AMap.event.addListener(map, 'zoomend', function () {
                    that.onZoomEnd(map,markers)
                });
            }
        },
        error:function (rep) {

        }
    })
}

function setEle(data) {
    var ele = $("#alarmList"),_html = ''
    var imgObj = {
        "烟感":'smoke.png',
        "水压":'water.png',
        "门禁":'Elevator.png',
    }
    if(data){
        for(var i=0;i<data.length;i++){
            _html+='<li><img src="/static/assets/img/'+imgObj[data[i].type]+'">'
                    +'<div class="Alarm_equipment">【'+data[i].type+'】</div>'
                    +'<div class="Alarm_position"><a href="/details?lat='+data[i].lat+'&lng='+data[i].lng+'">'+data[i].name+'</a></div>'
                    +'<div class="Alarm_data">'+data[i].num+'</div>'
                +'</li>'
        }
    }
    ele.html(_html)
}


function renderMap(map) {
    AMap.service('AMap.DistrictSearch', function() {
        var opts = {
            subdistrict: 1,   //返回下一级行政区
            extensions: 'all',  //返回行政区边界坐标组等具体信息
            level: 'city'  //查询行政级别为 市
        };
        //实例化DistrictSearch
        district = new AMap.DistrictSearch(opts);
        district.setLevel('district');
        //行政区查询
        district.search('普陀区', function(status, result) {
            var bounds = result.districtList[0].boundaries;
            var polygons = [];
            if (bounds) {
                for (var i = 0, l = bounds.length; i < l; i++) {
                    //生成行政区划polygon
                    var polygon = new AMap.Polygon({
                        map: map,
                        strokeWeight: 2,
                        path: bounds[i],
                        fillOpacity: 0.1,
                        fillColor: '#000',
                        strokeColor: '#556678'
                    });
                    polygons.push(polygon);
                }
                // map.setFitView();//地图自适应
            }

        })

    })

}
function createMarkers(map,data,hide) {//创建圆点

    var markers = [],zoom = map.getZoom()   //provinces见Demo引用的JS文件
    for(var i = 0; i < data.length; i++) {
        var marker, className;
            className = 'level'+data[i].level

        marker = new AMap.Marker({
            position: [data[i]['lng'], data[i]['lat']],
            clickable: true,
            visible:hide,
            title: '',
            map: map,
            content: "<div class='circleCon " + className + "'></div><div class='nameInfo'>"+ (data[i].name||"")+"</div>"
        });
        marker.subMarkers = [];
        if(data[i].child&&data[i].child.length){
            if(zoom >= 14){
                marker.subMarkers = createMarkers(map,data[i].child,true);
            }else{
                marker.subMarkers = createMarkers(map,data[i].child,false);
            }
        }

        if(!!data[i].data_type){
            (function (i,marker) {
                var site2 = data[i]
                AMap.event.addListener(marker, 'mousemove',function (){
                    openInfo(map,site2,marker,'parent')
                });
            })(i,marker)

        }else{
            (function (i,marker) {
                var site = data[i]
                AMap.event.addListener(marker, 'mousemove',function (){
                    openInfo(map,site,marker,'child')
                });
            })(i,marker)

        }
        markers.push(marker);


    }
    return markers
}
function onZoomEnd(map,markers){//缩放事件
    if(map.getZoom() < 14) {
        for(var i=0;i<markers.length;i++){
            markers[i].show()
            if(markers[i].subMarkers&&markers[i].subMarkers.length){
                toggleCircle(markers[i].subMarkers,true)
            }
        }
    }else{
        for(var i=0;i<markers.length;i++){
            markers[i].hide()
            if(markers[i].subMarkers&&markers[i].subMarkers.length){
                toggleCircle(markers[i].subMarkers,false)
            }
        }
    }
}
function toggleCircle(array,hide) {
    for(var i=0;i<array.length;i++){
        if(hide){
            array[i].hide()
        }else{
            array[i].show()
        }
    }
}

function GetRequest() {
    var url = location.search; //获取url中"?"符后的字串
    var theRequest = new Object();
    if (url.indexOf("?") != -1) {
        var str = url.substr(1);
        strs = str.split("&");
        for(var i = 0; i < strs.length; i ++) {
            theRequest[strs[i].split("=")[0]]=unescape(strs[i].split("=")[1]);
        }
    }
    return theRequest;
}

function openInfo(map,todo,marker,type) {
    var infoWindow,_html='',levelPx = 10
    todo.currPtotal = todo.currPtotal || ''

    if(type == 'child'){
        levelPx = 180
        var _str = '',showMore = 'none'
        for(var i=0;i<todo.focus_list.length;i++){
            _str += '<p>'+todo.focus_list[i]+'</p>'
            if(i==3){
                showMore = 'block'
                break;
            }else{
                showMore = 'none'
            }
        }
        if(_str){
            _str = '<li><span class="tit">报警位置：</span><div style="overflow:hidden;word-break: break-all;">'+_str+'</div></li>'
        }
        _html = '<div class="popBox">' +
            '<ul>' +
            // '<li class="clsoeIcon"><i class="iconfont icon-close"></i></li>'+
            '<li><span class="tit">传感器总数：</span>'+todo.count+'</li>'+
            '<li><span class="tit">传感器类型：</span>'+todo.sensor_type+'</li>'+
            '<li><span class="tit">传感器状态：</span>'+todo.sensor_status+'</li>'+
            '<li><span class="tit">报警类型：</span>'+todo.status+'</li>'+

            '<li><span class="tit">区域：</span>'+todo.area+'</li>'+
            '<li><span class="tit">街道：</span>'+todo.street_name+'</li>'+
            '<li><span class="tit">居委会：</span>'+todo.village+'</li>'+
            '<li><span class="tit">地址：</span>'+todo.address+'</li>'+
            _str+
            '<li class="fontBlue" style="display: '+showMore+'" onclick="showAlert(\''+todo.focus_list+'\')">查看更多</li>'+

            '</ul>'+
            '</div>'
    }else{
        var _str = ''
        levelPx = (todo.data_type.length) * 25
        for(var i=0;i<todo.data_type.length;i++){
            _str+=
                // '<li class="clsoeIcon"><i class="iconfont icon-close"></i></li>'+
                '<li><span class="tit">'+todo.data_type[i].type_name+'：</span>'+todo.data_type[i].type_num+'</li>'
        }
        _html = '<div class="popBox">' +
            '<ul>' +_str+'</div>'
    }

    infoWindow = new AMap.InfoWindow({
        isCustom:true,
        content: _html,
        offset:new AMap.Pixel(-180,levelPx)
    });
    infoWindow.open(map, [todo['lng'],todo['lat']]);
    $(".clsoeIcon").click(function () {
        infoWindow.close()
    })
    AMap.event.addListener(marker, 'mouseout',function (){
        infoWindow.close()
    });
    AMap.event.addListener(marker, 'click',function (){
        location.href = '/details?lat='+todo['lat']+'&lng='+todo['lng']
    });


}
function showAlert(info) {
    var array = info.split(","),str = ''
        for(var i=0;i<array.length;i++){
            str+='<p>'+array[i]+'</p>'
        }
    $('.alertInfoCon2').html(str)
    $('.alertInfo').css('z-index','9999')
}


