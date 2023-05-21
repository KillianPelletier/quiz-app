<template>
  <h3>{{question.title }}</h3>
  <p>{{question.text}}</p>
  <img v-if="question.image" :src="question.image" />

  <div v-for="(pa, index) in question.possibleAnswers" v-bind:key="pa.id">
    <a @click="$emit('click-on-answer', index+1)">{{pa.text}}</a>
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