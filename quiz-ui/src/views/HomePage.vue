
<template>
  <h1>Home page</h1>

  <RouterLink to="/start-new-quiz-page">Démarrer le quiz !</RouterLink>

  <div v-for="scoreEntry in registeredScores" v-bind:key="scoreEntry.date">
    {{ scoreEntry.playerName }} - {{ scoreEntry.score }}
  </div>
</template>

<script>
import quizApiService from "@/services/QuizApiService";

export default {
  name: "HomePage",

  data() {
    return {
      registeredScores: []
    }
  },

  async created() {
    let quizInfoApiResult = await quizApiService.getQuizInfo();
    let data = quizInfoApiResult.data;
    this.registeredScores = data.scores;
    console.log("Composant Home page 'created'");
  }
};
</script>