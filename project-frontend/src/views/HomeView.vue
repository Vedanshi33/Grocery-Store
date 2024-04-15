<template>
  <div class="container d-flex justify-content-center align-items-center vh-100">
    <div class="text-center">
      <div class="home">
        <h1 class="text-light display-4" style="font-size: 70px">WELCOME TO THE GROCERY STORE</h1><br><br>
        <HelloWorld msg="ENJOY SHOPPING" class="my-4 custom-text" /> <!-- Added custom class -->

        <router-link to="/User_login" class="btn btn-primary btn-lg">Login as User</router-link>
        <router-link to="/Admin_login" class="btn btn-primary btn-lg ml-2 mr-2">Login as Admin</router-link>
      </div>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import HelloWorld from '@/components/HelloWorld.vue'

export default {
  name: 'HomeView',
  components: {
    HelloWorld
  }
}
</script>



<style >
/* Global styles for body background */
body {
  background: #e96443;
  /* fallback for old browsers */
  background: -webkit-linear-gradient(to right, #904e95, #e96443);
  /* Chrome 10-25, Safari 5.1-6 */
  background: linear-gradient(to right, #904e95, #e96443);
  /* W3C, IE 10+/ Edge, Firefox 16+, Chrome 26+, Opera 12+, Safari 7+ */
}</style>
