const players = JSON.parse(JSON.parse(document.getElementById('players').textContent));
const playerseasons = JSON.parse(JSON.parse(document.getElementById('playerseasons').textContent));
const bestPlayers = JSON.parse(JSON.parse(document.getElementById('best_players').textContent));
const config = {responsive: true}

const cols = ['name', 'age', 'appearances', 'minutes', 'playing_time', 'best_role', 'wage', 'value', 'average_rating', 'pom', 'goals', 'assists', 'reds', 'yellows', 'xG', 'penalties', 'shots', 'shot_percent', 'key_passes', 'pass_completion', 'dribbles', 'cr_c', 'tackle_ratio', 'dist_per_90', 'int_per_90', 'tackles_per_90', 'goals_per_90', 'assists_per_90', 'determination', 'teamwork', 'leadership', 'clean_sheets', 'conceded'];
const colNames = ['Name', 'Age', 'Apps', 'Mins', 'Playing Time', 'Best Role', 'Wage (K)', 'Value (M)', 'Ave. Rating', 'PoM', 'Goals', 'Assists', 'Reds', 'Yellows', 'xG', 'Pens', 'Shots', 'Shot %age', 'Key Passes', 'Pass Completion %', 'Dribbles', 'Crosses', 'Tackle %age', 'Dist/90', 'Int/90', 'Tackles/90', 'Gls/90', 'Asts/90', 'Det', 'Teamwork', 'Leadership', 'Clean Sheets', 'Conceded'];

function playerTable() {
    var tableData = [];
    for (var i = 0; i < playerseasons.length; i++) {
        var data = playerseasons[i]['fields'];
        var pData = {};
        pData['name'] = players[data['player']];
        console.log(pData['name']);
        for (var col of cols.slice(1)) {
            dataPiece = data[col];
            if (dataPiece === +dataPiece && dataPiece % 1 !== 0) {
                pData[col] = Number.parseFloat(dataPiece).toFixed(2);
            } else if (col == "value") {
                var millionsValue = data[col] / (10 ** 6);
                // different precision based on magnitude
                if (millionsValue < 1) {
                    pData[col] = Number.parseFloat(millionsValue).toFixed(3);
                } else {
                    pData[col] = Number.parseFloat(millionsValue).toFixed(1);
                }
            } else if (col == "wage") {
                var thousandsValue = data[col] / (10 ** 3);
                if (thousandsValue < 1) {
                    pData[col] = Number.parseFloat(thousandsValue).toFixed(2);
                } else {
                    pData[col] = Number.parseFloat(thousandsValue).toFixed(0);
                }
            } else {
                pData[col] = data[col];
            }
        }
        tableData.push(pData);
    }

    var tableColumns = [];
    for (var i = 0; i < cols.length; i++) {
        if (i == 0) {
            tableColumns.push({
                title: colNames[i],
                field: cols[i],
                frozen: true,
                headerFilter: true,
                headerFilterPlaceholder: "Search"
            });
        } else {
            tableColumns.push({title: colNames[i], field: cols[i]});
        }
    }

    var height;
    if (tableData.length == 0) {
        height = 30;
    } else {
        height = 500;
    }
    var table = new Tabulator("#player-table", {
        height: height,
        cellVertAlign: "middle",
        data: tableData,
        columns: tableColumns,
        layout: "fitData",
        initialSort: [{column: 'appearances', dir: 'desc'}]
    });
}

playerTable();

function bestPlayersTable() {
    var def = bestPlayers['def'];
    var cre = bestPlayers['cre'];
    var att = bestPlayers['att'];
    var tableDiv = document.getElementById('best-players-table');
    var tbl = document.createElement('table');
    tbl.style.width = '100%';
    tbl.style.tableLayout = 'auto';
    tbl.className = 'table table-borderless';
    for (var i = 0; i < def.length; i++) {
        var tr = document.createElement('tr');
        var num = document.createElement('th');
        var defPlayer = document.createElement('td');
        var defScore = document.createElement('td');
        var empty1 = document.createElement('td');
        var crePlayer = document.createElement('td');
        var creScore = document.createElement('td');
        var empty2 = document.createElement('td');
        var attPlayer = document.createElement('td');
        var attScore = document.createElement('td');
        if (i == 0) {
            tr.style.fontWeight = 'bold';
            defPlayer.innerHTML = 'Best Defender';
            crePlayer.innerHTML = 'Best Creator';
            attPlayer.innerHTML = 'Best Attacker';
            defScore.innerHTML = 'Score';
            creScore.innerHTML = 'Score';
            attScore.innerHTML = 'Score';
        } else {
            num.innerHTML = i;
            defPlayer.innerHTML = players[def[i - 1][0]];
            crePlayer.innerHTML = players[cre[i - 1][0]];
            attPlayer.innerHTML = players[att[i - 1][0]];
            defScore.innerHTML = Number.parseFloat(def[i - 1][1]).toFixed(1);
            creScore.innerHTML = Number.parseFloat(cre[i - 1][1]).toFixed(1);
            attScore.innerHTML = Number.parseFloat(att[i - 1][1]).toFixed(1);
        }
        for (var x of [num, defPlayer, defScore, empty1, crePlayer, creScore, empty2, attPlayer, attScore]) {
            tr.appendChild(x);
        }
        tbl.appendChild(tr);
    }
    tableDiv.appendChild(tbl);
}

bestPlayersTable();

function valueForMoney() {
    var names = [];
    var xs = [];
    var ys = [];
    for (var i = 0; i < playerseasons.length; i++) {
        var data = playerseasons[i]['fields'];
        var ratio = 1000 * data['appearances'] * data['average_rating'] / data['wage'];
        names.push(players[data['player']] + '<br>Ratio: ' + Number.parseFloat(ratio).toFixed(1));
        xs.push(data['wage']);
        ys.push(data['appearances'] * data['average_rating']);
    }

    var trace = {
        x: xs,
        y: ys,
        hovertemplate: '%{text}',
        text: names,
        name: 'Apps * Ave. Rating / Wage',
        mode: 'markers',
        type: 'scatter'
    }

    var layout = {
        colorway: ['#3c1361', '#a262a9'],
        title: 'Value For Money',
        xaxis: {title: 'Wage'},
        yaxis: {title: 'Apps * Ave. Rating'},
        hovermode: 'closest',

    }

    Plotly.newPlot('valueForMoney', [trace], layout, config);

}

valueForMoney();