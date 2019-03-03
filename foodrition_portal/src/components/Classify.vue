<template>
  <div id="classify">
    <b-container>
      <b-collapse id="classify_collapse" v-model="notClassified">
        <b-row class="justify-content-center mt-5">
          <b-col class="col-md-2"><img style="margin:auto; display:block" src="../assets/rice.svg" width="100" height="100"></b-col>
          <b-col class="col-md-2"><img style="margin:auto; display:block" src="../assets/lettuce.svg" width="100" height="100"></b-col>
          <b-col class="col-md-2"><img style="margin:auto; display:block" src="../assets/spaguetti.svg" width="100" height="100"></b-col>    
        </b-row> 
        <b-row class="justify-content-center">
          <div class="mt-5">
            <h1>Wanna know what's in your food?</h1>
          </div>
        </b-row>
      </b-collapse>
      <b-row class="justify-content-center">
        <vue-dropzone id="dropzone"  class="mt-5" ref="myVueDropzone" :destroyDropzone="false" @vdropzone-removed-file="removedFile" @vdropzone-success="fileSuccess" :options="dropzoneOptions">
        </vue-dropzone>
      </b-row>
      <div v-if="!notClassified"> 
        <b-row class="justify-content-center" >
          <h2>{{predFood.food_class}}</h2>
        </b-row>
      </div>
      <b-row class="justify-content-center mt-5" v-if="!notClassified">
        <b-col class="col-md-4">
          <foodcomposition v-bind:predFood="predFood"></foodcomposition>
        </b-col>
        <b-col class="col-md-4">
          <foodtable v-bind:predFood="predFood"></foodtable>
        </b-col>
        <b-col class="col-md-4">
        </b-col>       
      </b-row>
    </b-container>
  </div>
</template>

<script>
import vue2Dropzone from 'vue2-dropzone'
import axios from 'axios'
import 'vue2-dropzone/dist/vue2Dropzone.min.css'
import Foodcomposition from './FoodComposition.vue'
import Foodtable from './FoodTable.vue'
import Food from '../models/food.js'

export default {
  name: 'classify',
  components: {
    vueDropzone: vue2Dropzone,
    'foodcomposition': Foodcomposition,
    'foodtable': Foodtable
  },
  data: function () {
    return {
      dropzoneOptions: {
          url: process.env.VUE_APP_REPO_API + "/classify",
          acceptedFiles: 'image/*',
          thumbnailWidth: 450,
          thumbnailHeight: 250,
          maxFilesize: 0.5,
          dictDefaultMessage: "Drop your Image here!",
          addRemoveLinks: true,
          maxFiles: 1,
          headers: {
            'Authorization': this.$store.getters.token
          }   
      },
      notClassified: true,
      predFood: new Food('None','None',20,20,20,20,20,20,20)
    }
  },
  methods:{
    fileSuccess (file, response){  
      //predFood = this.predFood
      var food_class = response["food_class"]
      var food_descr = response["nutr_class"]; 
      var ndb_no = response["nutr_ndb_no"];

      this.$http.get( process.env.VUE_APP_REPO_API + "/food",{ 
        params:{
          ndb_no: ndb_no
        } 
      }).then((response) => {
        console.log(response['data']['results'])
        var food_resp = response['data']['results'][0]
        this.predFood = this.food_from_response(food_resp, food_class, 
                                                food_descr)
      })
      this.notClassified = false     
    },
    removedFile (file, error, xhr){
      console.log("File removed!", file)
      this.notClassified = true
    },
    class_to_description(class_name){
      return (class_name.charAt(0).toUpperCase() + class_name.slice(1)).replace('_', ' ');
    },
    food_from_response(food_resp, food_class, food_descr){
      var food = new Food('','',0,0,0,0,0,0,0)
      food.descr = food_descr
      food.food_class = this.class_to_description(food_class) 
      food.protein_g= food_resp['protein_g'];
      food.water_g= food_resp['water_g'];
      food.fiber_g= food_resp['fiber_g'];
      food.carbohydrt_g= food_resp['carbohydrt_g'];
      food.energy_kcal= food_resp['energy_kcal'];
      food.sugar_g= food_resp['sugar_g'];
      food.lipid_g= food_resp['lipid_g'];
      return food
    } 
  },
  mounted(){
    console.log("REPO API " + process.env.VUE_APP_REPO_API)
  }
}
</script>

<style>
.vue-dropzone {
  min-width: 500px;
  min-height: 250px !important;
}   
</style>

