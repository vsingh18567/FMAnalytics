const seasonData = JSON.parse(JSON.parse(document.getElementById('playerseasons').textContent));
const seasons = JSON.parse(JSON.parse(document.getElementById('seasons').textContent));

// PLAYER TABLE
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

// CONSTRUCT TABLE
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


// RATING GRAPH
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
  title: 'Apps & Ave. Rating',
  yaxis: {title: 'Ave. Rating'},
  yaxis2: {
    title: 'Apps',
    overlaying: 'y',
    side: 'right',
  }
}
Plotly.newPlot('ratingChart', [trace12, trace11], layout);


// VALUE, WAGE GRAPH
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
  title: 'Value & Wage',
  yaxis: {title: 'Value (M)'},
  yaxis2: {
    title: 'Wage (K)',
    overlaying: 'y',
    side: 'right'
  }
};
Plotly.newPlot('valueWageChart', data, layout2);

