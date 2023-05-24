
<template>
    <h1 class="white">Votre score : {{participation.score }}</h1>

  <h4>Votre position {{ playerIndex + 1 }} sur {{ registeredScores.length }}</h4>
  <h4>{{ registeredScores[playerIndex].playerName }} tu bois {{ participation.answersSummaries.length - participation.score }} shot(s)</h4>

  <h3 class="white">Corrections</h3>
  <div v-for="(answer, index) in participation.answersSummaries" v-bind:key="index">
    <h6 class="white">Question {{ index + 1}} : Réponse {{ answer.correctAnswerPosition }} {{ (answer.wasCorrect)?"&#9989;":"&#10060;" }}</h6>
  </div>

  <h3 class="white">Meilleurs Scores</h3>
  <div class="scoreGridContainer">
    <div v-for="scoreEntry in registeredScores" v-bind:key="scoreEntry.date" class="scoreGridItem">
      {{ scoreEntry.playerName }} - <b>{{ Math.round((( participation.answersSummaries.length - scoreEntry.score) * 0.46) * 100) / 100 }}g/L</b>
    </div>
  </div>

  <RouterLink to="/">Retour à la page principale</RouterLink>
</template>
 
<script>
import quizApiService from "@/services/QuizApiService";
import participationStorageService from "@/services/ParticipationStorageService";

export default {
  name: "ScorePage",

  data() {
    return {
      registeredScores:[],
      participation:Object,
      playerIndex:Number
    }
  },

  props: {
      score: {
        type: Object
      }
    },

  async created() {
    let quizInfoApiResult = await quizApiService.getQuizInfo();
    let data = quizInfoApiResult.data;
    this.registeredScores = data.scores;
    this.participation = JSON.parse(participationStorageService.getParticipation());
    this.playerIndex = this.registeredScores.findIndex(p => p.playerName == this.participation.playerName && p.score == this.participation.score)
    console.log("Composant Score page 'created'");
  }
};
</script>

<style>
.playerScore {
  background-color: hsla(160, 100%, 37%, 0.5);
}
</style>