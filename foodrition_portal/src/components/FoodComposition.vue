<template>
  <div class="justify-content-center" id="foodcomposition">
    <h2 class="text-center">Food Composition</h2>
    <div id='donut_chart'></div>
  </div>  
</template>

<script>
import c3 from 'c3'
import Food from '../models/food.js'

export default {
  name: 'foodcomposition',
  props: {
    predFood: Food
  },
  watch:{
    predFood: function(newVal, oldVal){
      console.log("predFood changed!")
      console.log(newVal)
      this.donut_chart.load({
        columns: this.get_chart_columns(newVal)
      }) 
    }
  },
  data: function () {
    return {
      donut_chart: null
    }
  },
  methods:{
    get_chart_columns(food){
      var columns = []
      if (food.water_g !== null){
        columns.push(['water', food.water_g])
      }
      if (food.fiber_g !== null){
        columns.push(['fiber', food.fiber_g])
      }
      if (food.protein_g !== null){
        columns.push(['protein', food.protein_g])
      }
      if (food.carbohydrt_g !== null){
        columns.push(['carbohydrate', food.carbohydrt_g])
      }
      if (food.lipid_g !== null){
        columns.push(['lipid', food.lipid_g])
      }
      return columns
    }
  },
  mounted(){
    console.log("Mounting foodcomposition with ", this.predFood)
    this.donut_chart= c3.generate({
          bindto: '#donut_chart',
          size:{
            width: 350,
            height: 350
          },
          data: {
            columns: this.get_chart_columns(this.predFood),
            type : 'donut',
            colors: {
              "water": '#ecf0f1', 
              "protein": '#3498DB',
              "carbohydrate": "#F39C12",
              "fiber": '#20c997',
              "lipid": '#E74C3C'
            }
          }
        })
    }
}

</script>