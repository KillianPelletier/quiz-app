<template>
  <h3>{{question.title }}</h3>
  <p>{{question.text}}</p>
  <div style="min-height:320px">
    <img v-if="question.image" :src="question.image" />
  </div>
  <div class="gridContainer">
    <div v-for="(pa, index) in question.possibleAnswers" v-bind:key="pa.id" class="gridItem" @click="$emit('click-on-answer', index+1)">
      <a class="question">{{pa.text}}</a>
    </div>
  </div>

</template>

<script>
  export default {
    props: {
      question: {
        type: Object
      }
    },
    emits: ["click-on-answer"]
  }
</script>

<style scoped>
  img{
    max-height: 300px;
    max-width: 600px;
    display: block;
    margin-left: auto;
    margin-right: auto;
  }

  .gridContainer {
    margin-top: 2%;
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    grid-template-rows: repeat(2, 1fr);
    gap: 1rem;
    padding: 5px;
  }

  .gridItem {
    border: 1px;
    padding: .5rem;
    color: black;
    text-align: center;
  }

  .question{
    width:100%;
  }

  @media (hover: hover) {
    .gridItem:hover {
      background-color: hsla(160, 100%, 37%, 0.2);
      cursor: pointer;
    }
  }
</style>