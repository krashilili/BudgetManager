// When the browser window is resized, makeResponsive() is called.
d3.select(window).on("resize", makeResponsive);

// When the browser loads, makeResponsive() is called.
makeResponsive();


// The code for the chart is wrapped inside a function that
// automatically resizes the chart
function makeResponsive() {
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

    // Configure a parseTime function which will return a new Date object from a string
    var parseTime = d3.timeParse("%Y-%m-%d");

    // Load data from miles-walked-this-month.csv
    // var file = "miles-walked-this-month.csv";
    // d3.csv(file).then(successHandle, errorHandle);
    d3.json('/api/bs/?format=json').then(handleData, errorHandle);

    // Throw an error if one occurs
    function errorHandle(error) {
        throw error;
    }

    function handleData(bankData) {
        // if the SVG area isn't empty when the browser loads,
        var parsedBankDataDict = {};
        var parsedBankData = [];
        var parsedBankDataDictDetails = {};

        bankData.forEach(function (data) {

            if (data.amount > 0) {
                data.amounts = +data.amount;
                if (data.date in parsedBankDataDict) {
                    parsedBankDataDict[data.date] += data.amounts;
                    parsedBankDataDictDetails[data.date].push({'description': data.description, 'amount': data.amounts})
                } else {
                    parsedBankDataDict[data.date] = data.amounts;
                    parsedBankDataDictDetails[data.date] = [{'description': data.description, 'amount': data.amounts}]
                }
            }

        });
        // console.log(parsedBankDataDictDetails);
        Object.keys(parsedBankDataDict).forEach(function (key) {
            parsedBankData.push({
                'date': parseTime(key),
                'amount': parsedBankDataDict[key],
                'description': parsedBankDataDictDetails[key]
            })
        });

        // Configure a time scale with a range between 0 and the chartWidth
        // Set the domain for the xTimeScale function
        // d3.extent returns the an array containing the min and max values for the property specified
        // console.log(parsedBankData);

        // Create scales
        var xTimeScale = d3.scaleTime()
            .range([0, chartWidth])
            .domain(d3.extent(parsedBankData, function (d) {
                return d.date;
            }));
        var yLinearScale = d3.scaleLinear()
            .range([chartHeight, 0])
            .domain([0, d3.max(parsedBankData, d => d.amount)]);

        // Create axes
        var xAxis = d3.axisBottom(xTimeScale);
        var yAxis = d3.axisLeft(yLinearScale);
        // Append axes
        chartGroup.append("g").call(yAxis);
        chartGroup.append("g").attr("transform", `translate(0, ${chartHeight})`).call(xAxis);

        // Generate line
        var drawLine = d3.line()
            .x(data => xTimeScale(data.date))
            .y(data => yLinearScale(data.amount));

        // Append line
        chartGroup.append("path")
            .data([parsedBankData])
            .attr("class", "line")
            .attr("d", drawLine);

        // Append circles to data points
        var circlesGroup = chartGroup.selectAll("dot")
            .data(parsedBankData)
            .enter()
            .append("circle")
            .attr("cx", d => xTimeScale(d.date))
            .attr("cy", d => yLinearScale(d.amount))
            .attr("r", "3")
            .attr("fill", "gold")
            .attr("stroke-width", "1")
            .attr("stroke", "black");

        // date formatter to display dates nicely
        var dateFormatter = d3.timeFormat("%d-%b");

        // Step 1: Append tooltip div
        var toolTip = d3.select("body")
            .append("div")
            .classed("tooltip", true);

        // Step 2: Create "mouseover" event listener to display tooltip
        circlesGroup.on("mouseover", function (d, i) {
            toolTip.style("display", "block");
            toolTip.html(`<strong>${dateFormatter(parsedBankData[i].date)}</strong>
                           <br/>$${parsedBankData[i].amount}<br/>${parsedBankData[i].description[0].description}`)
                .style("left", d3.event.pageX + "px")
                .style("top", d3.event.pageY + "px");
        })
        // Step 3: Create "mouseout" event listener to hide tooltip
            .on("mouseout", function () {
                toolTip.style("display", "none");
            });


    }
}