
<template>
  
  <div>
    <h1>Admin</h1>
    <button @click="deconnection">Déconnexion</button>
    <table>
      <tr>
        <th>Position</th>
        <th>Image</th>
        <th>Titre</th>
        <th>Intitulé</th>
        <th></th>
        <th></th>
      </tr>
      <template v-for="q in questions" v-bind:key="q.id">
        <tr  @click="questionDetails(q.id)" style="cursor:pointer">
        <td>{{ q.position }}</td>
        <td><img v-if="q.image" :src="q.image" style="max-height: 50px;" /></td>
        <td>{{ q.title }}</td>
        <td>{{ q.text }}</td>
        <td><button @click.stop.prevent="updateQuestion(q.id)">Modifier</button></td>
        <td><button @click.stop.prevent="deleteQuestion(q.id)">Supprimer</button></td>
      </tr>
      
      <tr v-show="idShowQuestionDetail == q.id">
        <td colspan="6">
          <div v-for="answer in q.possibleAnswers" v-bind:key="answer.id" v-bind:class="(answer.isCorrect)?'correctAnswer':''">
            {{answer.text}}
          </div>
        </td>
      </tr>
      </template>
    </table>
  </div>
</template>

<script>
import quizApiService from "@/services/QuizApiService";
import participationStorageService from "@/services/participationStorageService";

export default {
  name: "AdminPage",

  data() {
    return {
      jwtToken:Text,
      questions:[],
      idShowQuestionDetail:-1
    }
  },

  methods:{
    async updateQuestion(id){
      console.log("Update question id : " + id);
    },

    async deleteQuestion(id){
      console.log("Delete question id : " + id);
      await quizApiService.deleteQuestion(id, this.jwtToken);

      let result = await quizApiService.getAllQuestions(this.jwtToken);
      this.questions = result.data;
      window.alert("Question supprimée avec succès !");
    },

    async questionDetails(id){
      if(this.idShowQuestionDetail != id){
        this.idShowQuestionDetail = id;
      }
      else {
        this.idShowQuestionDetail = -1;
      }
    },

    async deconnection(){
      participationStorageService.clearJWTToken();
      this.$router.push('/');
    }
    
  },

  async created() {
    this.jwtToken = participationStorageService.getJWTToken();
    if(this.jwtToken === null){
      window.alert("Vous devez vous connecter avant d'accéder à cette page.");
      this.$router.push('/login');
    }
    let result = await quizApiService.getAllQuestions(this.jwtToken);
    this.questions = result.data;


    console.log("Composant Login page 'created'");
  }

  
};
</script>

<style>

.correctAnswer {
  background-color: hsla(160, 100%, 37%, 0.5);
}

</style>