const seasonData = JSON.parse(JSON.parse(document.getElementById('playerseasons').textContent));
const seasons = JSON.parse(JSON.parse(document.getElementById('seasons').textContent));
const playerData = JSON.parse(JSON.parse(document.getElementById('playerdata_json').textContent));
const percentileData = JSON.parse(JSON.parse(document.getElementById('percentile_data').textContent));
console.log(playerData, percentileData);

const config = {responsive: true}


function radarChart() {
  const stats = ['gls/90', 'shots/90', 'dribbles/90', 'asts/90' , 'key_passes/90', 'interceptions/90', 'tackles/90', 'gls/90'];
  var data = [];
  var text = [];
  for (var stat of stats) {
    data.push(Math.min(1, playerData[stat] / percentileData[stat]));
    text.push(playerData[stat]);
  }
  const labels = ['Goals/90', 'Shots/90', 'Dribbles/90', 'Assists/90', 'Key Passes/90', 'Interceptions/90', 'Tackles/90', 'Goals/90'];
  
  data = [{
    type: 'scatterpolar',
    name: 'Key Stats/90',
    r: data,
    theta: labels,
    fill: 'toself',
    hovertemplate: '<i>Relative:</i> %{r}<br>Actual: %{text: .2f}',
    text: text
  }];
  
  layout = {
    polar: {
      radialaxis: {
        visible: true,
        range: [0, 1],
        tickformat: ',.0%',
  
      }
    },
    title: 'Key Stats/90 (relative to best in save)',
    showlegend: false,
    colorway: ['#3c1361']
  }
  
  Plotly.newPlot("radarChart", data, layout, config);

}

// COLLATE DATA IN GLOBAL FOR LOOP
var cols;
var colnames;
if (seasonData[0]['fields']['best_role'] == "GK" || seasonData[0]['fields']['best_role'] == "SK") {
  var cols = ['season', 'age', 'wage', 'value', 'playing_time',  'determination', 'teamwork', 'leadership', 'best_role', 'appearances', 'minutes', 'average_rating', 'pom', 'clean_sheets', 'conceded', 'goal_mistakes', 'goals', 'assists', 'reds', 'yellows',  "shot_percent", "xG", "penalties", "key_passes", "pass_completion", "dist_per_90", "cr_c", "header_percent", "tackle_ratio", "goals_per_90", "assists_per_90", "shots", "int_per_90", "tackles_per_90"];

  var colNames = ['Season', 'Age', 'Wage (K)', 'Value (M)', 'Playing Time',  'Determination', 'Teamwork', 'Leadership', 'Best Role', 'Apps', 'Minutes', 'Ave Rat.', 'PoM', 'Clean Sheets', 'Conceded', 'Goal Mistakes', 'Gls', 'Asts', 'Reds', 'Yellows', 'Shot on Target %', 'xG', 'Pens', 'Key Passes', 'Pass Completion %', 'Dist/90', 'Crosses', 'Header %', 'Tackle Success %', 'Gls/90', 'Asts/90', 'Shots/90', 'Int/90', 'Tackles/90'];

} else {
  var cols = ['season', 'age', 'wage', 'value', 'playing_time', 'determination', 'teamwork', 'leadership', 'best_role', 'appearances', 'minutes', 'average_rating', 'pom', 'goals', 'assists', 'reds', 'yellows',  "shot_percent", "xG", "penalties", "key_passes", "pass_completion", "dist_per_90", "cr_c", "header_percent", "tackle_ratio", "goals_per_90", "assists_per_90", "shots", "int_per_90", "tackles_per_90"];

  var colNames = ['Season', 'Age', 'Wage (K)', 'Value (M)', 'Playing Time', 'Determination', 'Teamwork', 'Leadership', 'Best Role', 'Apps', 'Minutes', 'Ave Rat.', 'PoM', 'Gls', 'Asts', 'Reds', 'Yellows', 'Shot on Target %', 'xG', 'Pens', 'Key Passes', 'Pass Completion %', 'Dist/90', 'Crosses', 'Header %', 'Tackle Success %', 'Gls/90', 'Asts/90', 'Shots/90', 'Int/90', 'Tackles/90'];
}
var tableData = [];
var seasonsData = []; var wageData = []; var valueData = []; var ratingData = []; var appsData = []; 
for (var i = 0; i < seasonData.length; i++) {
  // TABLE DATA
  var data = seasonData[i]['fields'];
  var pData = {};
  for (var col of cols) {
    dataPiece = data[col];
    // check for floats - stop floating point rounding problems
    if (dataPiece === +dataPiece && dataPiece % 1 !== 0) {
      pData[col] = Number.parseFloat(dataPiece).toFixed(2);
    } else if (col == 'season') {
      pData[col] = seasons[dataPiece];
    }
    else if (col == "shots") {
      pData[col] = Number.parseFloat(90 * dataPiece / (data['minutes'])).toFixed(2);
    } else if (col == "value") {
      var millionsValue = data[col] / (10**6);
      // different precision based on magnitude
      if (millionsValue < 1) {
        pData[col] = Number.parseFloat(millionsValue).toFixed(3);
      } else {
        pData[col] = Number.parseFloat(millionsValue).toFixed(1);
      }
    } else if (col == "wage") {
      var thousandsvalue = data[col] / (10**3);
      if (thousandsvalue < 1) {
        pData[col] = Number.parseFloat(thousandsvalue).toFixed(2);
      } else {
        pData[col] = Number.parseFloat(thousandsvalue).toFixed(0);
      }
    } else {
      pData[col] = data[col];
    }
  }
  tableData.push(pData);

  // WAGE VALUE DATA
  var thousandsvalue = data['wage'] / (10**3);
  if (thousandsvalue < 1) {
    wageData.push(Number.parseFloat(thousandsvalue).toFixed(2));
  } else {
    wageData.push(Number.parseFloat(thousandsvalue).toFixed(0));
  }
  var millionsValue = data['value'] / (10**6);
  if (millionsValue < 1) {
    valueData.push(Number.parseFloat(millionsValue).toFixed(3));
  } else {
    valueData.push(Number.parseFloat(millionsValue).toFixed(1));
  }
  seasonsData.push(seasons[data['season']]);
  ratingData.push(data['average_rating']);
  appsData.push(data['appearances']);
}

function dataTable() {
  var tableColumns = [];
  for (var i = 0; i < cols.length; i++) {
    if (i == 0) {
      tableColumns.push({title:colNames[i], field:cols[i], frozen:true});
    } else {
      tableColumns.push({title:colNames[i], field:cols[i]});
    }
  }
  var table = new Tabulator("#player-table", {
    height: (seasonData.length + 1) * 36,
    data:tableData,
    columns: tableColumns,
    layout:"fitData",
  });
}

function ratingChart() {
  var trace11 = {
    x: seasonsData,
    y: appsData,
    name: 'Appearances',
    yaxis: 'y2',
    type: 'scatter'
  }
  var trace12 = {
    x: seasonsData,
    y: ratingData,
    name: 'Rating',
    type: 'scatter'
  };
  var layout = {
    colorway: ['#3c1361', '#a262a9'],
    title: 'Apps & Ave. Rating',
    yaxis: {title: 'Ave. Rating'},
    yaxis2: {
      title: 'Apps',
      overlaying: 'y',
      side: 'right',
    }
  }
  Plotly.newPlot('ratingChart', [trace12, trace11], layout, config);
}

function wageValueChart() {
  var trace21 = {
    x: seasonsData,
    y: valueData,
    name: 'Value (M)',
    type: 'scatter'
  };
  var trace22 = {
    x: seasonsData,
    y: wageData,
    name: 'Wage (K)',
    yaxis: 'y2',
    type: 'scatter'
  };
  var data = [trace21, trace22];
  var layout2 = {
    colorway: ['#3c1361', '#a262a9'],
    title: 'Value & Wage',
    yaxis: {title: 'Value (M)'},
    yaxis2: {
      title: 'Wage (K)',
      overlaying: 'y',
      side: 'right'
    }
  };
  Plotly.newPlot('valueWageChart', data, layout2, config);
}

function dropdownMenu() {
  var cols2 = [];
  for (var i=0; i < cols.length; i++) {
    var disallowed = ['season', 'best_role', 'playing_time'];
    if (!(disallowed.includes(cols[i]))) {
      cols2.push({index: i, val: cols[i]});
    }
  }
  var sortedCols = cols2.sort((a, b) => (a.val > b.val) ? 1 : -1);
  console.log(sortedCols);
  var statdropdown1 = document.getElementById('stat-dropdown1');
  var statdropdown2 = document.getElementById('stat-dropdown2');
  for (var sortedCol of sortedCols) {
    var option = document.createElement('option');
    option.value = sortedCol.val;
    option.innerHTML = colNames[sortedCol.index];
    var option2 = document.createElement('option');
    option2.value = sortedCol.val;
    option2.innerHTML = colNames[sortedCol.index];
    statdropdown1.appendChild(option);
    statdropdown2.appendChild(option2);
  }
}

function customChart() {
  var layout = {
    title: 'Custom Chart',
    yaxis: {title: '?'},
    xaxis: {title: 'Season'},
    yaxis2: {
      title: '?',
      overlaying: 'y',
      side: 'right',
    }
  }
  Plotly.newPlot('customChart', [], layout, config);
}

function generateChart() {
  var sel1 = document.getElementById('stat-dropdown1');
  var option1 = sel1.value;
  var sel2 = document.getElementById('stat-dropdown2');
  var option2 = sel2.value;
  var option1data = [];
  var option2data = [];
  for (var i = 0; i < seasonData.length; i++) {
    var data = seasonData[i]['fields'];
    option1data.push(data[option1]);
    option2data.push(data[option2]);
  }

  var op1trace = {
    x: seasonsData,
    y: option1data,
    name: sel1.options[sel1.selectedIndex].innerHTML,
    type: 'scatter'
  };
  var op2trace = {
    x: seasonsData,
    y: option2data,
    name: sel2.options[sel2.selectedIndex].innerHTML,
    yaxis: 'y2',
    type: 'scatter'
  };
  var data = [op1trace, op2trace];

  // Delete graph data
  var graphDiv = document.getElementById('customChart');
  while (graphDiv.data.length > 0) {
    Plotly.deleteTraces('customChart', 0);
  }

  Plotly.addTraces('customChart', data);


  for (var sortedCol of sortedCols) {

  }

  var layoutUpdate = {
    title: sel1.options[sel1.selectedIndex].innerHTML + ' + ' + sel2.options[sel2.selectedIndex].innerHTML,
    yaxis: {title: sel1.options[sel1.selectedIndex].innerHTML},
    xaxis: {title: 'Season'},
    yaxis2: {
      title: sel2.options[sel2.selectedIndex].innerHTML,
      overlaying: 'y',
      side: 'right',
    }, 
    colorway: ['#3c1361', '#a262a9']
  }

  Plotly.update('customChart', {}, layoutUpdate);

}

radarChart(); dataTable(); ratingChart(); wageValueChart(); dropdownMenu(); customChart();