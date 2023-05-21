
<template>
  <div>
    <p>Saisissez votre nom : </p>
    <input type="text" v-model="username">
    <button @click="launchNewQuiz">Go !</button>
  </div>
</template>

<script>
import participationStorageService from "@/ParticipationStorageService";

export default {
  name: "NewQuizPage",

  data() {
    return {
      username:''
    }
  },

  methods:{
    launchNewQuiz(){
      participationStorageService.savePlayerName(this.username);
      console.log("Launch new quiz with", this.username);
      this.$router.push('/questions');
    },
  },

  async created() {
    console.log("Composant NewQuizPage page 'created'");
  }
};
</script>