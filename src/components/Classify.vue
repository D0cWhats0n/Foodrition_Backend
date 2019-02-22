<template>
  <div id="classify">
    <b-container>
      <b-collapse id="classify_collapse" v-model="not_classified">
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
      <div v-if="!not_classified"> 
        <b-row class="justify-content-center" >
          <h2>{{food_class}}</h2>
        </b-row>
      </div>
      <b-row class="justify-content-center mt-5">
        <b-col class="col-md-4">
         <foodcomposition/>
        </b-col>
        <b-col class="col-md-4">
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
import c3 from 'c3'
import 'vue2-dropzone/dist/vue2Dropzone.min.css'
import Foodcomposition from './FoodComposition.vue'
import Food from '../models/food.js'

export default {
  name: 'classify',
  components: {
    vueDropzone: vue2Dropzone,
    'foodcomposition': Foodcomposition
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
          maxFiles: 1
      },
      not_classified: true,
      food_class: '',
      nutr_descr: '',
      nutrition_data: {
        water_g: 0,
        energy_kcal: 0,
        protein_g: 0,
        carbohydtr_g: 0,
        fiber_g: 0,
        sugar_g: 0,
        lipid_g: 0
      },
    }
  },
  methods:{
    fileSuccess (file, response){  
      var self = this;
      console.log(response)
      this.food_class = this.class_to_description(response["food_class"]);
      this.nutr_descr = response["nutr_class"]; 
      this.ndb_no = response["nutr_ndb_no"];

      axios.get( process.env.VUE_APP_REPO_API + "/food",{ 
        params:{
          ndb_no: this.ndb_no
        } 
      }).then((response) => {
        console.log(response['data']['results'])
        self.nutrition_data.protein_g= response['data']['results'][0]['protein_g'];
        console.log("protein data :" + response['data']['results'][0]['protein_g'])
      })
      this.not_classified = false     
    },
    removedFile (file, error, xhr){
      console.log("File removed!")
      this.not_classified = true
    },
    class_to_description(class_name){
      return (class_name.charAt(0).toUpperCase() + class_name.slice(1)).replace('_', ' ');
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

