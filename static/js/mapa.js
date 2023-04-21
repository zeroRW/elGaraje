let mapOptions = {
    center:[20.58608, -100.38049],
    zoom:10
    }
    
    let map = new L.map('map' , mapOptions);
    
    let layer = new L.TileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png');
    map.addLayer(layer);
    
    let marker = new L.Marker([20.58608, -100.38049]);
    marker.addTo(map);