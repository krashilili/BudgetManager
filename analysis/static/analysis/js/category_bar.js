var margin = {top: 50, right: 20, bottom: 170, left: 100},
    width = 800 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

// Parse the date / time
// var	parseDate = d3.time.format("%Y-%m").parse;

var x = d3.scaleBand().rangeRound([0, width]);

var y = d3.scaleLinear().range([height, 0]);

var xAxis = d3.axisBottom(x);

var yAxis = d3.axisLeft(y);

var svg = d3.select("body").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform",
        "translate(" + margin.left + "," + margin.top + ")");

d3.json("/api/bs?format=json").then(successHandle,errorHandle);

function errorHandle(error) {
        throw error;
    }

function successHandle(raw_data) {
    // console.log(raw_data);
    var spend_cat = {};
    var data = [];

    raw_data.forEach(function(d) {
        d.amount = +d.amount;
        if (d.category in spend_cat){
            spend_cat[d.category] += d.amount;
        }else{
            spend_cat[d.category] = d.amount;
        }
    });

    // console.log(spend_cat);
    Object.keys(spend_cat).forEach(function (cat) {
        data.push({
            'category': cat,
            'amount': spend_cat[cat]
        })
    });

    console.log(data);
    x.domain(data.map(function(d) { return d.category; }));
    y.domain([0, d3.max(data, function(d) { return d.amount; })]);

    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis)
        .selectAll("text")
        .style("text-anchor", "end")
        .attr("dx", "-.8em")
        .attr("dy", "-.55em")
        .attr("transform", "rotate(-90)" );

    svg.append("g")
        .attr("class", "y axis")
        .call(yAxis)
        .append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 6)
        .attr("dy", ".71em")
        .style("text-anchor", "end")
        .text("Value ($)");

    svg.selectAll("bar")
        .data(data)
        .enter().append("rect")
        .style("fill", "steelblue")
        .attr("x", function(d) { return x(d.category); })
        .attr("width", x.bandwidth())
        .attr("y", function(d) { return y(d.amount); })
        .attr("height", function(d) { return height - y(d.amount); });

}