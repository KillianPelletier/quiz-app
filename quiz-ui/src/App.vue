<script setup>
  import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <div class="videoBackground">
    <video class="videoItself" autoplay muted loop id="myVideo">
      <source src="src/assets/bulles2.webm" type="video/webm">
    </video>
  </div>
  <header>
    <div class="headerCustom">
      <nav class="headerGridContainer">
        
        <RouterLink to="/" class="headerGridItem heinekenRed"><img src="src/assets/redStar.png"><h2 style="height:100%; text-align: center;">Alcoolotestoquizz</h2></RouterLink>
        <RouterLink to="/about" class="headerGridItem heinekenRed"><h2 style="height:100%; vertical-align: middle; line-height: 90px;">Nous</h2></RouterLink>
        <RouterLink to="/login" class="headerGridItem heinekenRed"><h2 style="height:100%; vertical-align: middle; line-height: 90px;">Admin</h2></RouterLink>
      </nav>
    </div>
  </header>

  <div class="mainContainer">
    <RouterView />
  </div>

  <div class="footer">
    <h4>L'abus d'alcool est dangereux pour la santé à consommer avec modération</h4>
    <a href="https://sante.gouv.fr/prevention-en-sante/addictions/article/l-addiction-a-l-alcool"><h5>En savoir plus</h5></a>
  </div>
</template>

<style scoped>

img{
  max-width: 50px;
  max-height:50px;
}
.logo {
  display: block;
  margin: 0 auto 2rem;
}

nav {
  width: 100%;
  font-size: 12px;
  text-align: center;
  margin-top: 2rem;
}

nav a.router-link-exact-active {
  color: var(--color-text);
}

nav a.router-link-exact-active:hover {
  background-color: transparent;
}

nav a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
}

nav a:first-of-type {
  border: 0;
}

.headerCustom{
  display: block;
  margin-left: auto;
  margin-right: auto;
  width:80%;
}

.headerGridContainer {
  margin-top: 2%;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-template-rows: repeat(1, 1fr);
  gap: 1rem;
  padding: 5px;
}

.headerGridItem {
  margin: .5rem;
  text-align: center;
}
.headerGridItem :hover{
  color: #008200;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    width:100%;
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }

  nav {
    text-align: left;
    margin-left: -1rem;
    font-size: 1rem;

    padding: 1rem 0;
    margin-top: 1rem;
  }
}
</style>
