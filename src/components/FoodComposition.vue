<template>
  <div id="foodcomposition">
    <h2 class="text-center">Food Composition</h2>
    <div id='donut_chart'></div>
  </div>  
</template>

<script>
import c3 from 'c3'
import Food from '../models/food.js'

export default {
  name: 'foodcomposition',
  data: function () {
    return {
      donut_chart: null
    }
  },
  methods:{
  },
  mounted(){
    console.log("Mounting foodcomposition")
    this.donut_chart= c3.generate({
      bindto: '#donut_chart',
      size:{
        width: 350,
        height: 350
      },
      data: {
        columns: [
          ['data1', 30],
          ['data2', 120]
        ],
        type : 'donut',
        colors: {
          "data1": '#343a40', 
          "data2": '#6c757d'
        }
      }
    })
  }
}
</script>