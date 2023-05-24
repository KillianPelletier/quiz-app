
<template>
  <h1 class="white">Connexion</h1>
  <div>
    <h4>Saisissez le mot de passe : </h4>
    <input type="text" v-model="password">
    <button @click="login" class="white">Se connecter</button>
  </div>
</template>

<script>
import quizApiService from "@/services/QuizApiService";
import participationStorageService from "@/services/ParticipationStorageService";

export default {
  name: "LoginPage",

  data() {
    return {
      password:''
    }
  },

  methods:{
    async login(){
      let result = await quizApiService.generateJWTToken(this.password);
      if(result.status != 200){
        window.alert("Mot de passe incorrect");
        return;
      }
      participationStorageService.saveJWTToken(result.data.token);
      this.$router.push('/admin');
    }
  },

  async created() {
    /*let jwtToken = participationStorageService.getJWTToken();
    if(jwtToken != null){
      this.$router.push('/admin');
    }*/

    console.log("Composant Login page 'created'");
  }
};
</script>

<style>
</style>