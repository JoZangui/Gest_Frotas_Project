function enviarLocalizacao(vehicleId) {
  navigator.geolocation.watchPosition(function(position) {
    fetch("/api/localizacao/", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({
        vehicle_id: vehicleId,
        lat: position.coords.latitude,
        lng: position.coords.longitude
      })
    });
  }, function(error) {
    console.error("Erro ao obter localização:", error);
  }, { enableHighAccuracy: true, maximumAge: 0 });
}

// Exemplo: cada motorista tem um ID único
enviarLocalizacao("carro_01");
