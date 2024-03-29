$(document).ready( function () {
    $('#billboard_songs').DataTable({
        ajax: '/api/billboard_songs',
        serverSide: true,
        columns: [
            {data: 'date', visible: false},
            {data: 'title'},
            {data: 'artist'},
            {data: 'spotify_link'},
            {data: 'spotify_id'},
            {data: 'genre', visible: false},
            {data: 'analysis_url', visible: false},
            {data: 'energy', visible: false},
            {data: 'liveness', visible: false},
            {data: 'tempo', visible: false},
            {data: 'speechiness', visible: false},
            {data: 'acousticness', visible: false},
            {data: 'instrumentalness', visible: false},
            {data: 'time_signature', visible: false},
            {data: 'danceability', visible: false},
            {data: 'key', visible: false},
            {data: 'duration_ms', visible: false},
            {data: 'loudness', visible: false},
            {data: 'valence', visible: false},
            {data: 'mode', visible: false},
            {data: 'lyrics', visible: false},
            {data: 'clean_lyrics', visible: false},
        ],
        dom: 'Bfrtip',
        buttons: ['colvis'],
        createdRow: function(row, data, dataIndex){
            $(row).attr('onclick', 'selectRow(this)');
        }
        
    });
   
});

var selected_songs = [];

function selectRow(row){
    // Grab the table representing the users playlist, note it will be empty in the beginning
    var playlist = document.getElementById("selected-songs");
    var cells = row.getElementsByTagName("td");
    var song_title = cells[0].textContent;
    var song_artist = cells[1].textContent;
    var song_spotify_link = cells[2].textContent;
    var song_spotify_id = cells[3].textContent;

    // Check if the song has already been chosen by the user
    if (selected_songs.includes(song_title)){
        swal("The song "+ song_title + "by " + song_artist + " has already been selected.");
        return;
        }

    if (selected_songs.length >= 10){
        swal("Playlist capacity reached. No more than 10 songs allowed.");
        return;
    }

    // Add song to the selected songs array
    selected_songs.push(song_title);

    // Create a new row in the playlist table
    var newRow = document.createElement("tr");
    var track_title = document.createElement("td");
    var track_artist = document.createElement("td");
    var track_spotify_link = document.createElement("td");
    var track_spotify_id = document.createElement("td");

    track_title.textContent = song_title;
    track_artist.textContent = song_artist;
    track_spotify_link.textContent = song_spotify_link;
    track_spotify_id.textContent = song_spotify_id;

    newRow.appendChild(track_title);
    newRow.appendChild(track_artist);
    newRow.appendChild(track_spotify_link);
    newRow.appendChild(track_spotify_id);

    // Create a delete button for the new row
    var deleteButton = document.createElement("button");
    deleteButton.textContent = "Delete";
    deleteButton.onclick = function () {
        // Remove the song from the selected playlist
        var index = selected_songs.indexOf(song_title);
        if (index > -1){
            selected_songs.splice(index, 1);
        }
        playlist.deleteRow(newRow.rowIndex);
    }
    newRow.appendChild(deleteButton);

    // This adds the selected song to the playlist table
    playlist.appendChild(newRow);
}

function save_playlist(){     
    // Get the table element
    var table = document.getElementById("selected-songs");

    // Get the table data
    var data = []
    var headers = []
    for (var i = 0; i < table.rows[0].cells.length; i++){
        headers[i] = table.rows[0].cells[i].innerHTML.toLowerCase().replace(/ /gi, '');
    }
    for (var i = 1; i < table.rows.length; i++) {
        var tableRow = table.rows[i];
        var rowData = {};
        for (var j = 0; j < tableRow.cells.length; j++) {
          rowData[headers[j]] = tableRow.cells[j].innerHTML;
        }
        data.push(rowData);
        console.log(rowData);
       }
    console.log(data);

    // Assign the data to a variable
    var playlistData = data;
    
    // Do something with the playlistData variable
    for (var i = 0; i < playlistData.length; i++){
        var input = document.createElement("input");
        input.setAttribute('type', 'hidden');
        input.name = 'song' + i;
        input.value = playlistData[i].spotifyid;
        document.getElementById('selected-songs').appendChild(input);
        console.log(input);
    }
}