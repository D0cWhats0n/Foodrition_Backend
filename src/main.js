import Vue from 'vue'
import App from './App.vue'
import Router from 'vue-router'
import BootstrapVue from "bootstrap-vue"
import Impressum from './components/Impressum.vue'
import Classify from './components/Classify.vue'
import "bootstrap/dist/css/bootstrap_flatly.min.css"
import "bootstrap-vue/dist/bootstrap-vue.css"

Vue.use(BootstrapVue)
Vue.use(Router)

const routes = [
    { path: '/', name: 'classify', component: Classify },
    { path: '/about', name: 'about', component: Impressum }  
];

const router = new Router({
  routes // short for `routes: routes`
})

Vue.config.productionTip = false

new Vue({
  render: h => h(App),
  router
}).$mount('#app')
