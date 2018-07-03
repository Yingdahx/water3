var site = GetRequest(),lng,lat,zoom
if(site && site['lng']){
    lng = site['lng']
    lat = site['lat']
    zoom = 15
}else{
    lng = 121.392499
    lat = 31.241701
    zoom = 13
}
var map = new AMap.Map('map-service',{
    resizeEnable: true,
    // mapStyle: 'amap://styles/60248a57a90f1d96733c4e7fb9c48cad',//样式URL
    zoom:zoom,
    center: new AMap.LngLat(lng,lat),
});


//模拟数据
var that = this,markers
renderMap(map)
$.ajax({
    type:'get',
    url:'http://39.104.85.167:8087/all/',
    success:function (rep) {
        // rep = "'"+rep +"'"
        // rep = JSON.parse(rep);
        var data
        if(rep&&typeof rep == 'object'&& Object.keys(rep).length != 0 ){
            data = rep
            if(zoom == 15){
                markers = createMarkers(map,data,false)
            }else{
                markers = createMarkers(map,data,true)
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

        markers.push(marker);

    }
    return markers
}
function onZoomEnd(map,markers){//缩放事件
    if(map.getZoom() < 14) {
        for(var i=0;i<markers.length;i++){
            markers[i].show()
            if(markers[i].subMarkers&&markers[i].subMarkers.length){
                console.info(markers[i].subMarkers)
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



