var width = 1500,
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

d3.json("japan_prefecture.geojson", createMap);

function createMap(japan) {
    var aProjection = d3.geoMercator()
        .center([ 139.0, 38.6 ])
        .translate([width/2, height/2])
        .scale(scale);
    var geoPath = d3.geoPath().projection(aProjection);
    var svg = d3.select("svg").attr("width",width).attr("height",height);
    //マップ描画
    var map = svg.selectAll("path").data(japan.features)
    .enter()
    .append("path")
        .attr("d", geoPath)
        .style("stroke", "#797979")
        .style("stroke-width", 0.1)
        .style("fill", "#797979");

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