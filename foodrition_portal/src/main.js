import Vue from 'vue'
import App from './App.vue'
import Router from 'vue-router'
import BootstrapVue from "bootstrap-vue"
import Impressum from './components/Impressum.vue'
import Classify from './components/Classify.vue'
import Login from './components/Login.vue'
import store from './store.js'
import "bootstrap/dist/css/bootstrap_flatly.min.css"
import "bootstrap-vue/dist/bootstrap-vue.css"
import Axios from 'axios'

Vue.use(BootstrapVue)
Vue.use(Router)

const routes = [
    { 
      path: '/', 
      name: 'classify', 
      component: Classify,  
      meta: { 
        requiresAuth: true
      }
    },
    { 
      path: '/about',
      name: 'about', 
      component: Impressum,
      meta: { 
        requiresAuth: true
      } 
    },
    {
      path: '/login',
      name: 'login',
      component: Login
    },  
];

var router = new Router({
  routes 
})

// Check before changing page if logged in
router.beforeEach((to, from, next) => {
  if(to.matched.some(record => record.meta.requiresAuth)) {
    if (store.getters.isLoggedIn) {
      next()
      return
    }
    next('/login') 
  } else {
    next() 
  }
})

Vue.config.productionTip = false

// register axios for the whole app and add token if it exists from localStorage
Vue.prototype.$http = Axios;
const token = localStorage.getItem('token');
if (token) {
  console.log("Setting auth header: " + token)
  Vue.prototype.$http.defaults.headers.common['Authorization'] = token
}


new Vue({
  render: h => h(App),
  store,
  router
}).$mount('#app')
