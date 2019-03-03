<template>
 <div>
<template>
  <div>
    <b-form @submit="login" >
        <b-row class="mt-5" align-h="center">
            <b-form-group class="col-sm-2 col-form-label"  
                id="UserInputGroup"
                label="User name:"
                label-for="userInput">
                <b-form-input
                id="userInput"
                type="text"
                v-model="user"
                required
                placeholder="Enter user name" />
            </b-form-group>
        </b-row>
        <b-row align-h="center"> 
            <b-form-group id="passwordInputGroup" label="Password:" label-for="passwordInput" class="col-sm-2 col-form-label">
                <b-form-input
                id="passwordInput"
                type="password"
                v-model="password"
                required
                placeholder="Enter password" />
            </b-form-group>
        </b-row>
        <b-row align-h="center"> 
            <b-button  @click="login" type="button"  variant="primary">Login</b-button>
        </b-row>
        <b-row align-h="center mt-3" v-if="loginErr">
          <span class="text-danger">HODOR!</span>
        </b-row>
    </b-form>
  </div>
</template>
 </div>
</template>
<script>
  export default {
    data(){
      return {
        user : "",
        password : ""
      }
    },
    methods: {
      login: function () {
        var user = this.user 
        var password = this.password
        this.$store.dispatch('login', { username: user, password: password })
            .then(() => this.$router.push('/'))
            .catch(err => {
                console.log(err)})
      }
    },
    computed: {
      loginErr(){
        return (this.$store.state.status == 'error')
      }
    }
  }
</script>