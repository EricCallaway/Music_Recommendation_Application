// This file contains the javascript code for the songs page

// This function diplays the songs table
$(document).ready( function () {
    $('#song_data').DataTable({
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
    });
   
    // This function is called when the user clicks on a song in the table
    $('#song_data tbody').on('click', 'tr', function(){
        var data = $('#song_data').DataTable().row( this ).data();
        swal("Great Choice!", "You chose the song " + data.title + " by " + data.artist);
    });
});