
<template>
  
  <h1 class="white">L'Alcoolotestoquizz</h1>

  <RouterLink to="/start-new-quiz-page" class="routeButton heinekenRed">Démarrer le quiz !</RouterLink>


  <h3 class="white">Meilleurs Scores</h3>
  <div class="scoreGridContainer">
    <div v-for="scoreEntry in registeredScores" v-bind:key="scoreEntry.date" class="scoreGridItem">
      {{ scoreEntry.playerName }} - <b>{{ Math.round(((this.size - scoreEntry.score) * 0.46) * 100) / 100 }}g/L</b>
    </div>
  </div>

</template>

<script>
import quizApiService from "@/services/QuizApiService";

export default {
  name: "HomePage",

  data() {
    return {
      registeredScores: [],
      size:0
    }
  },

  async created() {
    let quizInfoApiResult = await quizApiService.getQuizInfo();
    let data = quizInfoApiResult.data;
    this.registeredScores = data.scores;
    this.size = data.size;
    console.log("Composant Home page 'created'");
  }
};
</script>

<style>
</style>