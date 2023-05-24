import axios from "axios";

const instance = axios.create({
  baseURL: `${import.meta.env.VITE_API_URL}`,
  json: true,
});
import participationStorageService from "@/services/participationStorageService";

export default {
  async call(method, resource, data = null, token = null) {
    var headers = {
      "Content-Type": "application/json",
    };
    if (token != null) {
      headers.authorization = "Bearer " + token;
    }

    return instance({
      method,
      headers: headers,
      url: resource,
      data,
    })
      .then((response) => {
        return { status: response.status, data: response.data };
      })
      .catch((error) => {
        if (error.response.status == 401) {
          participationStorageService.clear();
          this.$router.push("/login");
        }
        return { error: error };
      });
  },
  getQuizInfo() {
    return this.call("get", "quiz-info");
  },
  getQuestion(position) {
    let result = this.call("get", "questions?position=" + position);
    return result;
  },
  sendParticipation(answers, username) {
    let data = {
      answers: answers,
      playerName: username,
    };
    let result = this.call("post", "participations", data);
    return result;
  },
  generateJWTToken(password) {
    let data = {
      password: password,
    };
    let result = this.call("post", "login", data);
    return result;
  },
  getAllQuestions(token) {
    return this.call("get", "questions-all", null, token);
  },
  deleteQuestion(id, token) {
    return this.call("delete", "questions/" + id, null, token);
  },
  updateQuestion(data, token) {
    return this.call("put", "questions/" + data.id, data, token);
  },
  addQuestion(data, token) {
    return this.call("post", "questions", data, token);
  }
};
