<template>

  <h1>Admin</h1>
  <div>
    <button id="show-modal" @click="questionAdd()">Ajouter une question</button>
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
        <td><button id="show-modal" @click.stop.prevent="questionUpdate(q)">Modifier</button></td>
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
    <!--Question modification Modal-->
    <div class="modal-mask" v-if="idShowQuestionUpdate != -1 || addQuestion == true">
      <div class="modal-wrapper">
        <div class="modal-container">
          <div class="modal-header">
            <slot name="header">
              <div v-if="idShowQuestionUpdate != -1">
                Mise à jour de question :
                "<b>{{currentQuestion.title}}</b>"
              </div>
              <div v-if="addQuestion == true">
                Création de question
              </div>
            </slot>
          </div>

          <div class="modal-body">
            <slot name="body">
              <form id="updateForm" method="get">
                <div>
                  <p>Position : </p>
                  <input class="verySmallField" type="text" name="position" v-model="currentQuestion.position">
                </div>

                <div>
                  <p>Titre : </p>
                  <input class="smallField" type="text" name="title" v-model="currentQuestion.title">
                </div>

                <div style="margin-bottom:20px">
                  <p>Intitulé : </p>
                  <input class="mediumField" type="text" name="label" v-model="currentQuestion.text">
                </div>

                <div style="margin-bottom:10px" v-for="(answer,index) in currentQuestion.possibleAnswers" v-bind:key="answer.id">
                  <p>Réponse {{ index + 1}} : </p>
                  <textarea class="largeField" v-bind:name="'answer'+(index)" v-model="(answer.text)"></textarea>
                  <div>
                    Réponse correcte : <input type="radio" v-bind:id="isCorrect+(index)" name="correctAnswer" v-bind:checked="(answer.isCorrect)" @click="correctAnswer(index)">
                  </div>
                </div>

              </form>
            </slot>
          </div>

          <div class="modal-footer">
            <slot name="footer">
              <button class="modal-default-button" @click="hideModal()">
                Annuler
              </button>
              <button class="modal-default-button" @click="sendForm()" v-if="idShowQuestionUpdate != -1">
                Confirmer la mise à jour
              </button>
              <button class="modal-default-button" @click="sendForm()" v-if="addQuestion == true">
                Confirmer la création
              </button>
            </slot>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import quizApiService from "@/services/QuizApiService";
import participationStorageService from "@/services/ParticipationStorageService";

export default {
  name: "AdminPage",

  data() {
    return {
      jwtToken:Text,
      questions:[],
      idShowQuestionDetail:-1,
      idShowQuestionUpdate:-1,
      addQuestion: false,
      currentQuestion:{},
      correctAnswerIndex:null,
      addedQuestion:{
        image:"",
        position:"",
        title:"",
        text:"",
        possibleAnswers:[
          {text:"", isCorrect:true},
          {text:"", isCorrect:false},
          {text:"", isCorrect:false},
          {text:"", isCorrect:false}
        ]
      },
    }
  },

  methods:{
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

    async questionUpdate(q){
      if(this.idShowQuestionUpdate != q.id){
        this.idShowQuestionUpdate = q.id;
      }
      else {
        this.idShowQuestionUpdate = -1;
      }

      this.currentQuestion = q;
    },

    async questionAdd(){
      if(this.addQuestion == false){
        this.addQuestion = true;
      }

      this.currentQuestion = this.addedQuestion;
    },

    async hideModal(){
      this.currentQuestion = null;
      this.addQuestion=false;
      this.idShowQuestionUpdate = -1;
    },

    async sendForm(){
      if(this.currentQuestion.position == "" || this.currentQuestion.title == "" || this.currentQuestion.text == "")
        window.alert("Le formulaire doit être rempli correctement")
      else{
        if(isNaN(parseInt(this.currentQuestion.position)))
          window.alert("La position doit être un nombre")
        else{
          this.currentQuestion.position = parseInt(this.currentQuestion.position);

          if(this.correctAnswerIndex != null){
            this.currentQuestion.possibleAnswers.forEach(element => {
              element.isCorrect = false;
            });

            this.currentQuestion.possibleAnswers[this.correctAnswerIndex].isCorrect = true;
          }

          if(this.addQuestion == true && this.currentQuestion.position > this.questions.length + 1)
            window.alert("Position trop élevée " + (this.questions.length + 1) + " max")
          else if(this.addQuestion == false && this.currentQuestion.position > this.questions.length)
            window.alert("Position trop élevée " + (this.questions.length) + " max")
          else{
            if(this.addQuestion == true)
              await quizApiService.addQuestion(this.currentQuestion, this.jwtToken);
            else
              await quizApiService.updateQuestion(this.currentQuestion, this.jwtToken);

            //Update questions
            let result = await quizApiService.getAllQuestions(this.jwtToken);
            this.questions = result.data;

            //Close Modal and Reset forms
            this.hideModal();
            this.correctAnswerIndex=null;
            this.addedQuestion={
              image:"",
              position:"",
              title:"",
              text:"",
              possibleAnswers:[
                {text:"", isCorrect:true},
                {text:"", isCorrect:false},
                {text:"", isCorrect:false},
                {text:"", isCorrect:false}
              ]
            };
          }
        }
      }
    },

    async correctAnswer(index){
      this.correctAnswerIndex=index;
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
.bold {
  font-weight: bold;
}

.correctAnswer {
  background-color: hsla(160, 100%, 37%, 0.5);
}

.modal-mask {
  position: fixed;
  z-index: 9998;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: table;
  transition: opacity 0.3s ease;
}

.modal-wrapper {
  display: table-cell;
  vertical-align: middle;
}

.modal-container {
  width: 60%;
  margin: 0px auto;
  padding: 20px 30px;
  background-color: #fff;
  border-radius: 2px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.33);
  transition: all 0.3s ease;
  font-family: Helvetica, Arial, sans-serif;
}

.modal-header h3 {
  margin-top: 0;
  color: #42b983;
}

.modal-body {
  margin: 20px 0;
}

.modal-default-button {
  float: right;
}

/*
 * The following styles are auto-applied to elements with
 * transition="modal" when their visibility is toggled
 * by Vue.js.
 *
 * You can easily play with the modal transition by editing
 * these styles.
 */

.modal-enter {
  opacity: 0;
}

.modal-leave-active {
  opacity: 0;
}

.modal-enter .modal-container,
.modal-leave-active .modal-container {
  -webkit-transform: scale(1.1);
  transform: scale(1.1);
}

p{
  margin-bottom:0 !important
}

.verySmallField {
  width:5%
}
.smallField {
  width:20%
}

.mediumField {
  width:50%
}

.largeField {
  width:70%
}

</style>