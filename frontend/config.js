// Определяем базовый URL для API автоматически
(function() {
  const hostname = window.location.hostname;

  if (hostname === "localhost" || hostname === "127.0.0.1") {
    // Если фронт открыт локально
    window.API_BASE_URL = "http://localhost:8000";
  } else {
    // Если фронт открыт по внешнему IP или домену
    window.API_BASE_URL = http://${hostname}:8000;
  }
})();

 
