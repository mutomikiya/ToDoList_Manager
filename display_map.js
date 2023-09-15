var width = 1200,
    height = 800;
var scale =10000;
var pointdata = {
        "type":"LineString",
        "coordinates": []
    }

var elements = document.getElementById("plot-stations");
for (const child of elements.children) {
    point = child.attributes.item(0).value.split(',');
    pointdata["coordinates"].push([Number.parseFloat(point[0]), Number.parseFloat(point[1])])
}
elements.remove();

d3.json("japan_prefecture.geojson", createMap);

function createMap(japan) {
    var featureCollection = {
        "type":"FeatureCollection",
        "features": [
            {   "type": "Feature",
                "properties": {"id": 1, "name": "新潟駅" },
                "geometry": {
                    "type": "Point",
                    "coordinates": [139.0592001,37.9120388]
                }
            },
            {   "type": "Feature",
                "properties": {"id": 2, "name": "秋田駅" },
                "geometry": {
                    "type": "Point",
                    "coordinates": [139.8433199,38.9222392]
                }
            },
            {   "type": "Feature",
                "properties": {"id": 3, "name": "函館駅" },
                "geometry": {
                    "type": "Point",
                    "coordinates": [140.7236888,41.7675754]
                }
            },
        ]
    }
    var aProjection = d3.geoMercator()
        .center([ 139.5, 38.6 ])
        .translate([width/2, height/2])
        .fitExtent([[width * 0.1, height * 0.1], [width * 0.9, height * 0.9]], featureCollection);
        
    var geoPath = d3.geoPath().projection(aProjection);
    var svg = d3.select("svg").attr("width",width).attr("height",height);
    //マップ描画
    var background = svg
        .append("rect")
        .attr("width",width)
        .attr("height",height)
        .attr("fill", "#a9ceec");
    var map = svg.selectAll("path").data(japan.features)
        .enter()
        .append("path")
            .attr("d", geoPath)
            .style("stroke", "#797979")
            .style("stroke-width", 0.1)
            .style("fill", "#FFEDB3");

    var line = svg.selectAll(".ilne").data([pointdata])
        .enter()
        .append("path")
            .attr("d",geoPath)
            .style("stroke","red")
            .style("stroke-width",4.0)
            .style("fill","none");

    var point = svg.selectAll(".point").data(pointdata.coordinates)
        .enter()
        .append("circle")
            .attr("cx",function(d) { return aProjection(d)[0]; })
            .attr("cy",function(d) { return aProjection(d)[1]; })
            .attr("r",3)
            .style("stroke","black")
            .style("fill","white")
}