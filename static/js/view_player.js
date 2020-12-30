const seasonData = JSON.parse(JSON.parse(document.getElementById('playerseasons').textContent));



function seasonsTable() {

  console.log(seasonData[0]['fields']);

  if (seasonData[0]['fields']['best_role'] == "GK" || seasonData[0]['fields']['best_role'] == "SK") {
    console.log("GK");
  }


  var colNames = ['season', 'age', 'wage', 'playing_time', 'value', 'determination', 'teamwork', 'leadership', 'best_role', 'appearances', 'minutes', 'average_rating', 'pom', 'goals', 'assists', 'reds', 'yellows', ""];

}

seasonsTable();