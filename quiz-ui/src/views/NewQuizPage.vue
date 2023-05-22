
<template>
  <div>
    <p>Saisissez votre nom : </p>
    <input type="text" v-model="playerName">
    <button @click="launchNewQuiz">Go !</button>
  </div>
</template>

<script>
import participationStorageService from "@/services/ParticipationStorageService";

export default {
  name: "NewQuizPage",

  data() {
    return {
      playerName:''
    }
  },

  methods:{
    launchNewQuiz(){
      participationStorageService.clear();
      participationStorageService.savePlayerName(this.playerName);
      console.log("Launch new quiz with", this.playerName);
      this.$router.push('/questions');
    },
  },

  async created() {
    console.log("Composant NewQuizPage page 'created'");
  }
};
</script>