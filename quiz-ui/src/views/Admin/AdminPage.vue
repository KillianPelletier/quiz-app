
<template>
  <h1>Admin</h1>
</template>

<script>
import participationStorageService from "@/services/participationStorageService";

export default {
  name: "AdminPage",

  data() {
    return {
      jwtToken:Text,
      questions:[]
    }
  },

  methods:{
  },

  async created() {
    this.jwtToken = participationStorageService.getJWTToken();
    if(this.jwtToken === null){
      window.alert("Vous devez vous connecter avant d'accéder à cette page.");
      this.$router.push('/login');
    }
    //this.questions = 


    console.log("Composant Login page 'created'");
  }
};
</script>