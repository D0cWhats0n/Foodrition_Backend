<template>
<b-navbar class="bg-primary navbar-dark navbar-expand-lg" toggleable="lg">
<!-- <router-link class="nav-link" to="/">Foodrition</router-link> -->
    <b-navbar-brand href="/">Foodrition</b-navbar-brand>

    <b-navbar-toggle target="nav_collapse" />

    <b-collapse is-nav id="nav_collapse">
        <b-navbar-nav>
            <router-link class="nav-link" to="/about">About</router-link>
            <span class="nav-link logout-span" v-if="isLoggedIn"><a @click="logout">Logout</a></span>
        </b-navbar-nav>
    </b-collapse>
</b-navbar>
</template>

<script>
export default {
  name: 'navbar',
  computed: {
    isLoggedIn: function() {
      return this.$store.getters.isLoggedIn;
    }
  },
  methods: {
    logout: function() {
      this.$store.dispatch("logout").then(() => {
        this.$router.push("/login");
    });
    }
  }
}
</script>
<style>
.logout-span {
  cursor: pointer
}   
</style>