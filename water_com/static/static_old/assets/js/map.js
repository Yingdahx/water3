
var map = new AMap.Map('map-service',{
    resizeEnable: true,
    // mapStyle: 'amap://styles/60248a57a90f1d96733c4e7fb9c48cad',//样式URL
    zoom:2,
    center: new AMap.LngLat(118.767413,32.041544),
});
//模拟数据
var data=[
    {
        name:'桃浦',
        lng:121.348664,
        lat:31.28211,
        level:1,
        child:[
            {
            lng:121.37147,
            lat:31.281584,
            level:2, // model(info_type)里是4
            },{
            lng:121.337309,
            lat:31.284885,
            level:1,// model(info_type)里是1
            // model(info_type)里是7 ， 这是3 
            }
        ]
    },{
        name:'真如',
        lng:121.409235,
        lat:31.251504,
        level:2,
        child:[
            {
            lng:121.427689,
            lat:31.26207,
            level:2,
            },
            {
            lng:121.416128,
            lat:31.25058,
            level:3,
            }
        ]
    },{
        name:'宜川',
        lng:121.437517,
        lat:31.246661,
        level:3,
        child:[
            {
            lng:121.432649,
            lat:31.24051,
            level:3,
            },{
            lng:121.447155,
            lat:31.246967,
            level:3,
            }
        ]
    },{
        name:'梅川',
        lng:121.405141,
        lat:31.238088,
        level:2,
        child:[
            {
            lng:121.387974,
            lat:31.235226,
            level:3,
            },{
            lng:121.400592,
            lat:31.229942,
            level:2,
            }
        ]
    }
]
var that = this
var markers = createMarkers(map,data,true)
renderMap(map)
map.add(markers)

AMap.event.addListener(map, 'zoomend', function () {
    that.onZoomEnd(map,markers)
});

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
                map.setFitView();//地图自适应
            }

        })

    })

}
function createMarkers(map,data,hide) {//创建圆点
    var markers = []   //provinces见Demo引用的JS文件
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
            marker.subMarkers = createMarkers(map,data[i].child,false);
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



