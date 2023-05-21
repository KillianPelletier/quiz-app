<template>
  <h1>Question {{ currentQuestion.position }} / {{ totalNumberOfQuestion }}</h1>
  <QuestionDisplay :question="currentQuestion" @click-on-answer="answerClickedHandler" />
</template>

<script>
  import QuestionDisplay from "@/views/QuestionDisplay.vue";
  import quizApiService from "@/services/QuizApiService";
  import participationStorageService from "@/services/ParticipationStorageService";

  export default {
    components: {
      QuestionDisplay
    },

    data() {
      return {
        currentQuestion: {
          position:1
        },
        answers:[],
        totalNumberOfQuestion:0
      }
    },

    methods:{
      async loadQuestionByPosition(){
        let result = await quizApiService.getQuestion(""+this.currentQuestion.position);
        this.currentQuestion = result.data
      },

      async answerClickedHandler(selectedAnswerIndex){
        this.answers.push(selectedAnswerIndex);
        if(this.currentQuestion.position == this.totalNumberOfQuestion){
          this.endQuiz();
          return;
        }
        this.currentQuestion.position+=1
        this.loadQuestionByPosition()
      },

      async endQuiz(){
        console.log("Quiz finished");
        let playerName = participationStorageService.getPlayerName();
        let result = await quizApiService.sendParticipation(this.answers, playerName);
        console.log(result);
      }
    },

    async created() {
      let quizInfo = await quizApiService.getQuizInfo();
      this.totalNumberOfQuestion = quizInfo.data.size;
      await this.loadQuestionByPosition();
      console.log("Question Manager 'created'");
    }
  }
</script>