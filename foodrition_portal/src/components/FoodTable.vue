<template>
    <div class="justify-content-center" id="foodtable">
        <h2 class="text-center">Per <input type="number" id="weight" v-model.number="foodWeight" min="1" max="10000"></input>g:</h2>
        <h4 class="mt-5">Water: {{(predFood.water_g*foodWeight/100).toFixed(2)}}g</h4>
        <h4 class="my-3">Fiber: {{(predFood.fiber_g*foodWeight/100).toFixed(2)}}g</h4>
        <h4 class="my-3">Protein: {{(predFood.protein_g*foodWeight/100).toFixed(2)}}g</h4>
        <h4 class="my-3">Carbohydrates: {{(predFood.carbohydrt_g*foodWeight/100).toFixed(2)}}g</h4>
        <h4 class="my-3">Lipid: {{(predFood.lipid_g*foodWeight/100).toFixed(2)}}g</h4>
    </div>
</template>

<script>
import Food from '../models/food.js'

export default {
  name: 'foodtable',
  props: {
      predFood: Food
  },
  data: function(){
      return {
          foodWeight: 100
      }
  }
}



</script>