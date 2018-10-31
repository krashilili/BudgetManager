var svgWidth = 1500;
var svgHeight = 500;

// When the browser window is resized, makeResponsive() is called.
d3.select(window).on("resize", makeResponsive);

// When the browser loads, makeResponsive() is called.
makeResponsive();

// The code for the chart is wrapped inside a function that
// automatically resizes the chart
function makeResponsive() {

    // if the SVG area isn't empty when the browser loads,
    // remove it and replace it with a resized version of the chart
    var svgArea = d3.select("body").select("svg");

    // clear svg is not empty
    if (!svgArea.empty()) {
        svgArea.remove();
    }

    // SVG wrapper dimensions are determined by the current width and
    // height of the browser window.
    var svgWidth = window.innerWidth;
    var svgHeight = window.innerHeight;

    var margin = {
        top: 50,
        bottom: 50,
        right: 50,
        left: 50
    };

    var chartHeight = svgHeight - margin.top - margin.bottom;
    var chartWidth = svgWidth - margin.left - margin.right;

    // Append SVG element
    var svg = d3
        .select(".chart")
        .append("svg")
        .attr("height", svgHeight)
        .attr("width", svgWidth);

    // Append group element
    var chartGroup = svg.append("g")
        .attr("transform", `translate(${margin.left}, ${margin.top})`);


    // Load data from miles-walked-this-month.csv
    // var file = "miles-walked-this-month.csv";
    // d3.csv(file).then(successHandle, errorHandle);
    d3.json('/api/bs/?format=json').then(handleData, errorHandle);

    // Throw an error if one occurs
    function errorHandle(error) {
        throw error;
    }

    function handleData(bankData) {
         // Configure a parseTime function which will return a new Date object from a string
        var parseTime = d3.timeParse("%Y-%m-%d");


        var parsedBankDataDict = {};
        var parsedBankData = [];

        bankData.forEach(function (data) {

            if (data.amount > 0) {
                data.amounts = +data.amount;
                if (data.date in parsedBankDataDict) {
                    parsedBankDataDict[data.date] += data.amounts;
                } else {
                    parsedBankDataDict[data.date] = data.amounts;
                }
            }

        });

        Object.keys(parsedBankDataDict).forEach(function (key) {
            parsedBankData.push({
                'date': parseTime(key),
                'amount': parsedBankDataDict[key]
            })
        });

        // Configure a time scale with a range between 0 and the chartWidth
        // Set the domain for the xTimeScale function
        // d3.extent returns the an array containing the min and max values for the property specified
        console.log(parsedBankData);
        var xTimeScale = d3.scaleTime()
            .range([0, chartWidth])
            .domain(d3.extent(parsedBankData, function (d) {
                return d.date;
            }));

        // console.log(d3.extent(parsedBankData, data => data.date));

        // Configure a linear scale with a range between the chartHeight and 0
        // Set the domain for the xLinearScale function
        var yLinearScale = d3.scaleLinear()
            .range([chartHeight, 0])
            .domain(d3.extent(parsedBankData, function (d) {
                return d.amount;
            }));

        // console.log());
        // Create two new functions passing the scales in as arguments
        // These will be used to create the chart's axes
        var bottomAxis = d3.axisBottom(xTimeScale);
        var leftAxis = d3.axisLeft(yLinearScale);

        // Append an SVG group element to the SVG area, create the left axis inside of it
        chartGroup.append("g")
            .call(leftAxis);

        // Append an SVG group element to the SVG area, create the bottom axis inside of it
        // Translate the bottom axis to the bottom of the page
        chartGroup.append("g")
            .call(bottomAxis);

        // Configure a drawLine function which will use our scales to plot the line's points
        var drawLine = d3
            .line()
            .x(data => xTimeScale(data.date))
            .y(data => yLinearScale(data.amount));

        // Append an SVG path and plot its points using the line function
        chartGroup.append("path")
        // The drawLine function returns the instructions for creating the line for milesData
            .data([parsedBankData])
            .attr("class", "line")
            .attr("d", drawLine);

        // append circles
        var circlesGroup = chartGroup.selectAll("circle")
            .data(parsedBankData)
            .enter()
            .append("circle")
            .attr("cx", d => xTimeScale(d.date))
            .attr("cy", d => yLinearScale(d.amount))
            .attr("r", "10")
            .attr("fill", "gold")
            .attr("stroke-width", "1")
            .attr("stroke", "black");

        // date formatter to display dates nicely
        var dateFormatter = d3.timeFormat("%d-%b");

        // Step 1: Append tooltip div
        var toolTip = d3.select("body")
            .append("div")
            .style("display", "none")
            .classed("tooltip", true);

        // Step 2: Create "mouseover" event listener to display tooltip
        circlesGroup.on("mouseover", function (d) {
            toolTip.style("display", "block")
                .html(
                    `<strong>Hello<strong>`)
                .style("left", d3.event.pageX + "px")
                .style("top", d3.event.pageY + "px");
        })
        // Step 3: Create "mouseout" event listener to hide tooltip
            .on("mouseout", function () {
                toolTip.style("display", "none");
            });


    }
}