<template>
  <main role="main">
    <div class="jumbotron">
      <h1>Floor plans classifier service</h1>
      <p class="lead">The service allows to upload and classify the image using multiple classifiers and list all the uploaded images.
        This application uses Django and Django REST Framework for backend, Vue.js for the frontend. </p>
      <!--<a class="btn btn-lg btn-primary" href="" role="button">View tutorial</a>-->
    </div>

    <!--<h4 v-if="!authenticated">-->
      <!--You are not logged in! Please <a class="btn btn-primary" @click="auth.login()">Log In</a> to continue.-->
    <!--</h4>-->
  </main>
</template>

<script>
export default {
  name: 'home'
}
</script>

<style>
  a {
    cursor: pointer;
  }
</style>
