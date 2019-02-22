<template>
<b-navbar class="bg-primary navbar-dark" toggleable="lg">
    <b-navbar-brand href="/">Foodrition</b-navbar-brand>

    <b-navbar-toggle target="nav_collapse" />

    <b-collapse is-nav id="nav_collapse">
        <b-navbar-nav>
            <router-link class="nav-link" to="/about">About</router-link>
        </b-navbar-nav>
    </b-collapse>
</b-navbar>
</template>

<script>
export default {
  name: 'navbar'
}
</script>