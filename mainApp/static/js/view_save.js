const playerData = JSON.parse(JSON.parse(document.getElementById('playerdata').textContent));
const seasonData = JSON.parse(JSON.parse(document.getElementById('seasondata').textContent));
const saveNo = JSON.parse(JSON.parse(document.getElementById('save_no').textContent));
const seasonPositions = JSON.parse(JSON.parse(document.getElementById('season_positions').textContent));
const config = {responsive: true}
const bestPlayers = JSON.parse(JSON.parse(document.getElementById('best_players').textContent));

console.log(seasonData);

function seasonsChart() {
    if (seasonPositions == null) {
        return;
    }
    var coreData = seasonPositions['pos'];

    var trace = {
        x: coreData['seasons'],
        y: coreData['ys'],
        hovertemplate: '%{text}',
        text: coreData['labels'],
        name: 'Position'
    };
    var layout = {
        xaxis: {
            range: [0, Math.max(coreData['seasons'])],
            dtick: 1,
            title: 'Seasons'
        },
        yaxis: {
            range: [0, seasonPositions['max']],
            tickvals: coreData['tickvals'],
            ticktext: coreData['ticktext']
        },
        colorway: ['#3c1361', '#a262a9'],
        title: 'League Positions'
    };

    Plotly.newPlot('seasonPositions', [trace], layout, config);

}

seasonsChart();

function seasonDropdown() {
    var dropdown = document.getElementById('season-dropdown');
    for (var i = seasonData.length - 1; i >= 0; i--) {
        var option = document.createElement('option');
        var season = seasonData[i];
        option.value = season.pk;
        option.innerHTML = (season.year - 1) + '-' + season.year;
        dropdown.appendChild(option);
    }
    if (seasonData.length > 0) {
        document.getElementById("season-btn").disabled = false;
    }
}

seasonDropdown();

function viewSeason() {
    var seasonPk = document.getElementById('season-dropdown').value;

    window.location.href = "/fm/save/".concat(saveNo).concat("/season/").concat(seasonPk);
}

function playerTable() {
    var cols = ['name', 'nationality', 'seasons', 'appearances', 'goals', 'assists', 'average_rating', 'pom', 'best_role', 'minutes', 'minutes_per_season', 'max_value', 'yellows', 'reds', 'home_grown_status', 'xG', 'goals_per_xG', 'goals_per_90', 'shots_per_90', 'assists_per_90', 'key_passes_per_90', 'pass_completion', 'dribbles_per_90', 'int_per_90', 'tackles_per_90'];

    var colNames = ['Name', 'Nat', 'Seasons', 'Apps', 'Gls', 'Asts', 'Ave. Rating', 'PoMs', 'Best Role', 'Minutes', 'Min/Season', 'Max Value (M)', 'Yellows', 'Reds', 'Home-Grown', 'xG', 'Goals/xG', 'Gls/90', 'Shots/90', 'Asts/90', 'Key Passes/90', 'Pass Completion %', 'Dribbles/90', 'Interceptions/90', 'Tackles/90'];

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
                var millionsValue = data[col] / (10 ** 6);
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
            tableColumns.push({
                title: colNames[i],
                field: cols[i],
                frozen: true,
                headerFilter: true,
                headerFilterPlaceholder: "Search"
            });
        } else if (i == 3) {
            tableColumns.push({
                title: colNames[i],
                field: cols[i],
                headerFilter: "input",
                headerFilterPlaceholder: "Min Apps",
                headerFilterFunc: ">=",
                width: 100
            })
        } else if (i == 14) {
            tableColumns.push({
                title: colNames[i],
                field: cols[i],
                formatter: "tickCross",
                headerFilter: "tick",
                headerFilterFunc: function (headerValue, rowValue, rowData, filterParams) {
                    if (headerValue) {
                        return rowValue;
                    } else {
                        return true;
                    }
                }
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
        initialSort: [{column: 'appearances', dir: 'desc'}],
        rowClick: function (e, row) {

            var preName = row.getData()['name'];
            var name = preName.replace(" ", "_");
            window.location.href = "/fm/save/".concat(saveNo).concat("/").concat(name);
        }
    });
    return table;
}

var table = playerTable();


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
            defPlayer.innerHTML = def[i - 1][0];
            crePlayer.innerHTML = cre[i - 1][0];
            attPlayer.innerHTML = att[i - 1][0];
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
    console.log(def, cre, att);
}

bestPlayersTable();
