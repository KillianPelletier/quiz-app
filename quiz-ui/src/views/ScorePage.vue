
<template>
  <h1>Votre score : {{participation.score }}</h1>

  <h4>Votre position {{ playerIndex + 1 }} sur {{ registeredScores.length }}</h4>
  <div v-for="(answer, index) in participation.answersSummaries" v-bind:key="index">
    {{ index + ". "+answer.correctAnswerPosition + " " + answer.wasCorrect?"&#9989;":"&#10060;" }}
  </div>

  <div v-for="(scoreEntry, index) in registeredScores" v-bind:key="scoreEntry.date" v-bind:class = "(index == playerIndex)?'playerScore':''">
    {{ scoreEntry.playerName }} - {{ scoreEntry.score }}
  </div>

  <RouterLink to="/">Retour à la page principale</RouterLink>
</template>
 
<script>
import quizApiService from "@/services/QuizApiService";
import participationStorageService from "@/services/participationStorageService";

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