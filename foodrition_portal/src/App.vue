<template>
  <div>
    <Navbar></Navbar>
    <router-view  class="mt-6"></router-view>
  </div>
</template>

<script>
import Classify from './components/Classify.vue'
import Impressum from './components/Impressum.vue'
import Navbar from './components/Navbar.vue'
import Foodcomposition from './components/FoodComposition.vue'

export default {
  name: 'app',
  components: {
    Impressum,
    Classify,
    Navbar,
    Foodcomposition
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
