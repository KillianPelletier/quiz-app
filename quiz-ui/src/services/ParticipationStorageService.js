export default {
  clear() {
    window.localStorage.clear();
  },
  savePlayerName(playerName) {
    window.localStorage.setItem("playerName", playerName);
  },
  getPlayerName() {
    return window.localStorage.getItem("playerName");
  },
  saveParticipation(participation) {
    window.localStorage.setItem("participation", participation);
  },
  getParticipation() {
    return window.localStorage.getItem("participation");
  },
  saveJWTToken(jwtToken) {
    window.localStorage.setItem("jwtToken", jwtToken);
  },
  getJWTToken() {
    return window.localStorage.getItem("jwtToken");
  },
};
