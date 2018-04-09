var svgWidth=470;
var svgHeight=400;
var spacing=10;

var margin = {
    'top':50,
    'right':5,
    'left':40,
    'bottom':35
}

function getXAxisData(data){
    return Array.from(data, function(d) { return d._id})
}

function makeBarChart(data, criteria , svgWidth, svgHeight, margin, spacing, name) {
    d3.select("svg").remove();
    
    var svg = d3.select("#charts").append("svg")
                            .attr("width", svgWidth)
                            .attr("height", svgHeight)
                            .style("background-color", "white")

    var canvasWidth = svgWidth - margin.left - margin.right;
    var canvasHeight = svgHeight - margin.bottom - margin.top;
                    
    var y_scale = d3.scale.linear()
                    .domain([0, d3.max(data,function(d){return d[criteria]})])
                    .range([0, canvasHeight]);
                    
    var yAxisScale = d3.scale.linear()
                    .domain([0, d3.max(data, function(d) {return d[criteria];})])
                    .range([canvasHeight , 0]);
    
    var xAxisScale = d3.scale.ordinal()
                    .domain(getXAxisData(data))
                    .rangeRoundBands([0,canvasWidth],0.3);
                    
    var xAxis = d3.svg.axis()
                    .scale(xAxisScale)
                    .orient("bottom")
                    .ticks(5)
                    
    var yAxis = d3.svg.axis()
                .scale(yAxisScale)
                .orient("left")
                .ticks(5);
    
    var canvas = svg.append('g')
                    .attr("width", canvasWidth)
                    .attr('height', canvasHeight)
                    .attr("class", "canvas")
                    
   svg.append('text')
                .attr("x", (svgWidth / 2))  
                .attr("y", (margin.top / 2))
                .attr("text-anchor", "middle") 
                .attr("class", "svg-title")  
                .text(name);
    
    svg.append('g')
        .attr("class","axis") 
        .attr('transform', 'translate('+(margin.left-2)+','+(margin.top)+')')
        .call(yAxis)
    
    var rectangles = canvas.append('g')
                        .attr('transform', 'translate('+(margin.left)+','+(margin.top)+')')
                        .selectAll("rect")
                        .data(data)
                        .enter()
                        .append("rect");
                          
                    
    var rectAttributes = rectangles
                        .attr("x", function (d, i) { return i * (canvasWidth / data.length); })
                        .attr('width', (canvasWidth / data.length) - spacing)
                        .attr("y", function (d) { return canvasHeight-y_scale(d[criteria])})
                        .attr("height", 0)
                        .transition().duration(1000)
                        .attr("height", function (d) { return y_scale(d[criteria])})
                        .attr("class", 'rectangles')
    
    svg.append('g')
         .attr('class', 'axis')
         .attr("transform", "translate(" + (margin.left -2) + "," + (svgHeight - margin.bottom) + ")")
         .call(xAxis)
}

function valueToTitle(value){
    return value.split("_").map(function(word){ return word.charAt(0).toUpperCase() + word.substr(1)}).join(" ")
}

function chooseData(event) {
    event.preventDefault();
    var value = $("#getData").val()
    
    switch(value){
        case 'videos_by_category':
        case 'videos_by_body_part': 
        case 'videos_by_language':
            margin["left"] = 35;
            makeBarChart(data[value], 
                    'number_of_videos',
                    svgWidth, 
                    svgHeight, 
                    margin, 
                    spacing,
                    valueToTitle(value))
            break;
            
        case 'likes_by_category':
        case 'likes_by_body_part':
        case 'likes_by_language':
            margin["left"] = 35;
            makeBarChart(data[value], 
                    'number_of_likes',
                    svgWidth, 
                    svgHeight, 
                    margin, 
                    spacing,
                    valueToTitle(value))
            break;
                    
        case 'youtube_views_by_category':
        case 'youtube_views_by_body_part':
        case 'youtube_views_by_language':
            margin["left"] = 60;
            makeBarChart(data[value], 
                    'number_of_views',
                    svgWidth, 
                    svgHeight, 
                    margin, 
                    spacing,
                    valueToTitle(value))
            break;
        
        case 'duration_by_category':
        case 'duration_by_body_part':
        case 'duration_by_language' :
        default:
            margin["left"] = 40;
            makeBarChart(data[value], 
                    'duration',
                    svgWidth, 
                    svgHeight, 
                    margin, 
                    spacing,
                    valueToTitle(value))
            break;
    };
}

// Initialize with a first graph on load.  
makeBarChart(data['videos_by_category'], 
                    'number_of_videos',
                    svgWidth, 
                    svgHeight, 
                    margin, 
                    spacing,
                    'Videos By Category');