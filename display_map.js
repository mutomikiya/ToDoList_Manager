var pointdata = {
        "type":"LineString",
        "coordinates": []
    }
var elements = document.getElementById("plot-stations");
var color = elements.attributes['color'].value

var width = elements.attributes['width'].value,
    height = elements.attributes['height'].value;

var most_east = 0
var most_west = 180
var most_north = 0
var most_south = 90

for (const child of elements.children) {
    var point = child.attributes.item(0).value.split(',');
    var lon = Number.parseFloat(point[0])
    var lat = Number.parseFloat(point[1])
    pointdata["coordinates"].push([lon, lat])

    if (most_east < lon) {
        most_east = lon
    }
    if (lon < most_west) {
        most_west = lon
    }
    if (most_north < lat) {
        most_north = lat
    }
    if (lat < most_south){
        most_south = lat
    }
}

var center = [most_west + (most_east - most_west)/2, most_south + (most_north - most_south)/2]

elements.remove();

var svg = d3.select("svg").attr("width",width).attr("height",height);

var featureCollection = {
    "type":"FeatureCollection",
    "features": []
}

pointdata["coordinates"].forEach(point => {
    featureCollection["features"].push(
        {   "type": "Feature",
            "properties": {},
            "geometry": {
                "type": "Point",
                "coordinates": point
            }
        }
    )
});

var aProjection = d3.geoMercator()
    .center(center)
    .translate([width/2, height/2])
    .fitExtent([[width * 0.1, height * 0.1], [width * 0.9, height * 0.9]], featureCollection);
    
var geoPath = d3.geoPath().projection(aProjection);

d3.json("japan_prefecture.geojson", createMap);
// d3.json("japan_train_railroad.geojson", displayRailload);

function createMap(japan) {
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
            .style("stroke",color)
            .style("stroke-width",4.0)
            .style("fill","none");

    var point = svg.selectAll(".point").data(pointdata.coordinates)
        .enter()
        .append("circle")
            .attr("cx",function(d) { return aProjection(d)[0]; })
            .attr("cy",function(d) { return aProjection(d)[1]; })
            .attr("r",5)
            .style("stroke","black")
            .style("fill","white")
}
// function displayRailload(railload_data) {
//     var railload = svg.selectAll(".ilne").data(railload_data.features)
//     .enter()
//     .append("path")
//         .attr("d",geoPath)
//         .style("stroke","black")
//         .style("stroke-width",2.0)
//         .style("fill","none");
// }