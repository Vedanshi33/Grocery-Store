
<template>
  <div id="app">
    <nav>
      <router-link to="/" style="color: white;">Home</router-link> |
      <router-link to="/about" style="color: white;">About</router-link>
    </nav>
    <router-view />
  </div>
</template>

<style>
body.bg-nav {
  background: #e96443;
  /* fallback for old browsers */
  background: -webkit-linear-gradient(to right, #904e95, #e96443);
  /* Chrome 10-25, Safari 5.1-6 */
  background: linear-gradient(to right, #904e95, #e96443);
  /* W3C, IE 10+/ Edge, Firefox 16+, Chrome 26+, Opera 12+, Safari 7+ */
}
</style>