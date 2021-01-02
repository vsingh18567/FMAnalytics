const playerData = JSON.parse(JSON.parse(document.getElementById('playerdata').textContent));
const seasonData = JSON.parse(JSON.parse(document.getElementById('seasondata').textContent));
const saveNo = JSON.parse(JSON.parse(document.getElementById('save_no').textContent));
const ratingWages = JSON.parse(JSON.parse(document.getElementById('rating_wages').textContent));
console.log(ratingWages);

function playerTable() {
  var cols = ['name', 'nationality', 'seasons', 'appearances', 'goals', 'assists', 'average_rating', 'pom', 'best_role', 'minutes','minutes_per_season', 'max_value', 'yellows', 'reds', 'home_grown_status', 'xG', 'goals_per_xG','goals_per_90', 'shots_per_90','assists_per_90', 'key_passes_per_90', 'pass_completion', 'dribbles_per_90', 'int_per_90', 'tackles_per_90'];

  var colNames = ['Name', 'Nat', 'Seasons', 'Apps', 'Gls', 'Asts', 'Ave. Rating', 'PoMs', 'Best Role', 'Minutes', 'Min/Season', 'Max Value (M)', 'Yellows', 'Reds', 'Home-Grown', 'xG', 'Goals/xG', 'Gls/90', 'Shots/90','Asts/90', 'Key Passes/90', 'Pass Completion %', 'Dribbles/90', 'Interceptions/90', 'Tackles/90'];
  
  // construct the data
  var tableData = [];
  for (var i = 0; i < playerData.length; i++) {
    var data = playerData[i]['fields'];
    var pData = {};
    for (var col of cols) {
      dataPiece = data[col];
      // check for floats - stop floating point rounding problems
      if (dataPiece === +dataPiece && dataPiece % 1 !== 0) {
        pData[col] = Number.parseFloat(dataPiece).toFixed(2);
      } else if (col == "max_value") {
        var millionsValue = data[col] / (10**6);
        // different precision based on magnitude
        if (millionsValue < 1) {
          pData[col] = Number.parseFloat(millionsValue).toFixed(3);
        } else {
          pData[col] = Number.parseFloat(millionsValue).toFixed(1);
        }
      } else {
        pData[col] = data[col];
      }
      
    }
    tableData.push(pData)
  }
  
  var tableColumns = [];
  for (var i = 0; i < cols.length; i++) {
    if (i == 0) {
      tableColumns.push({title:colNames[i], field:cols[i], frozen:true});
    } else if (i == 14) {
      tableColumns.push({title:colNames[i], field:cols[i], formatter:"tickCross"});
    } else {
      tableColumns.push({title:colNames[i], field:cols[i]});
    }
  }

  var height;
  if (tableData.length == 0) {
    height = 30;
  } else {
    height = 500;
  }
  
  var table = new Tabulator("#player-table", {
    height:height,
    data:tableData,
    columns: tableColumns,
    layout:"fitData",
    rowClick: function(e, row) {
      
      var preName = row.getData()['name'];
      var name = preName.replace(" ", "_");
      window.location.href = "/fm/save/".concat(saveNo).concat("/").concat(name);
    }
  });
  return table;
}
var table = playerTable();

// document.getElementById("filter-btn").onclick = function () {
//   table.clearFilter();
//   console.log("hi");
//   var num = document.getElementById("apps-filter").value;
//   table.addFilter("appearances", ">=", num);
// }

var trace = {
  x: ratingWages['wages'],
  y: ratingWages['ratings'],
  mode: 'markers',
  type: 'scatter',
  text: ratingWages['labels']
}

var layout = {
  hovermode: 'closest'
}

Plotly.newPlot('wage-rating-chart', [trace], layout);
