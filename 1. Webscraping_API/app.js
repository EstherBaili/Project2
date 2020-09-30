function initial() {
  
  var selector=d3.select("#selDataset");

  //updating the dropdown menu

    d3.json("data/job_data.json").then(function(data) {
        jobs=data[0];
        for (const [key] of Object.entries(jobs)) {
            selector
            .append("option")
            .append("value")
            .text(`${key}`)
            .property("value", name)
            
        }

        //updating the initial page 
        jobs_ind_init=data[1].ACT
        jobs_init=data[0].ACT
        jobs_location_init=data[2].ACT
        
        updateBar(jobs_ind_init)
        updateGauge(jobs_init)
        updatePanel(jobs_location_init)


    }); 
  
}

d3.select("#selDataset").on("change", optionChanged);

function optionChanged() {
    var selector=d3.select("#selDataset");
    // Assign the value of the dropdown menu option to a variable
    var dropdown_value = selector.property("value");

    d3.json("data/job_data.json").then(function(data) {
        jobs_ind=data[1]
        jobs_location=data[2]
        jobs_total=data[0]
        for (const [key, value] of Object.entries(jobs_ind)) {
            if (key==dropdown_value){
                var dictionary=value;
                updateBar(dictionary)
                    

            }    
            
        } 

        for (const [key, value] of Object.entries(jobs_location)) {
            if (key==dropdown_value){
                var dictionary2=value;
                updatePanel(dictionary2)
                    

            }    
            
        } 

        for (const [key, value] of Object.entries(jobs_total)) {
            if (key==dropdown_value){
                var dictionary3=value;
                updateGauge(dictionary3)
                    

            } 
            
        } 
    });

    

}

function updateBar(newdata) {
    var industry=[]
    var frequency=[]
    for (const [key, value] of Object.entries(newdata)) {
        industry.push(key) 
        frequency.push(value)
    
    }

    
    var trace1 ={
        x: industry,
        y: frequency,
        name: "Greek",
        type: "bar",
    };
    
    var layout = {
        title: 'Breakdown of Data Analyst Jobs by Sector',
        showlegend: false,
        hovermode: 'closest',
        margin: {t:30}
    };
    
    
    var bar_chart = [trace1];
    
    
    
    Plotly.newPlot("bar", bar_chart, layout);
    



}

function updatePanel(newdata) {
    var panel_select=d3.select("#sample-metadata");
    d3.select("#sample-metadata").html("");
    for (const [key, value] of Object.entries(newdata)) {
        panel_select
        .append("p")
        .text(`${key}: ${value}`)
    }

    



}

function updateGauge(newdata){

    
    
    var data = [
        {
          type: "indicator",
          mode: "gauge+number",
          value: newdata,
          title: { text: "Total Data Analyst Jobs" },
          gauge: {
            axis: { range: [null, 80], tickwidth: 1, tickcolor: "darkblue" },
            bar: { color: "darkblue" },
            borderwidth: 2,
            bordercolor: "gray",
            steps: [
              { range: [0, 40], color: "cyan" },
              { range: [40, 80], color: "royalblue" }
            ],
          }
        }
    ];
      
    var layout = {
        width: 500,
        height: 400,
        margin: { t: 25, r: 25, l: 25, b: 25 },
        paper_bgcolor: "lavender",
        font: { color: "darkblue", family: "Arial" }
    };
      
    Plotly.newPlot('gauge', data, layout);
    
}



initial();
