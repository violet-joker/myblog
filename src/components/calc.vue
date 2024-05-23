<template>
  <div id="calc">
    <p>a = {{ a }}; b = {{ b }} </p>
    a + b = <input v-model="input" @keydown.enter="check('+')" type="number"/><br>
    a - b = <input v-model="input" @keydown.enter="check('-')" type="number"/><br>
    a * b = <input v-model="input" @keydown.enter="check('*')" type="number"/><br>
  </div>
</template>

<script setup>
import { ref } from "vue";
const a = ref(0), b = ref(0), input = ref(0)


function rand(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min
}

function check(op) {
  let res = 0
  if (op === '+')  res = a.value + b.value
  else if (op === '-') res = a.value - b.value
  else res = a.value * b.value
  if (input.value === res) {
    console.log('ok, next')
    a.value = rand(1, 100)
    b.value = rand(1, 100)
    if (a.value < b.value) {
      [a.value, b.value] = [b.value, a.value]
    }
    input.value = null
  } else {
    console.log('wrong', res, input.value)
  }
}
</script>

<style>
#calc {
  font-size: 30px;
}
#calc input {
  width: 100px;
}
#calc input:focus {
  background-color: #4b5f4b;
}
</style>