<template>
  <h1>Question {{ currentQuestion.position }} / {{ totalNumberOfQuestion }}</h1>
  <QuestionDisplay :question="currentQuestion" @click-on-answer="answerClickedHandler" />
</template>

<script>
  import QuestionDisplay from "@/views/QuestionDisplay.vue";
  import quizApiService from "@/services/QuizApiService";

  export default {
    components: {
      QuestionDisplay
    },

    data() {
      return {
        currentQuestion: {}
      }
    },

    async created() {
      this.currentQuestion = await quizApiService.getQuestion("1");
      console.log("Question Manager 'created'");
    },
  }
</script>