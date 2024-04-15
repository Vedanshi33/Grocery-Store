<template>
    <div class="bg-f">
      <div class="container">
        <h1 class="confirmation-title">Order Confirmation</h1>
        <p class="confirmation-message">Thank you for your purchase!</p>
        <p class="confirmation-message">Your order has been confirmed and will be processed shortly.</p>
        <router-link to="/user_dashboard" class="btn btn-primary">Continue Shopping</router-link>
       
        <button @click="logout" class="btn btn-primary">Logout</button>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';

  export default {
    // Your script logic goes here
    data() {
    return {
      accessToken: localStorage.getItem('access_token'),
     
    };
  },
  mounted() {
    // const categoryId = this.$route.params.category_id;
    axios.get(`http://127.0.0.1:5000/confirmation`, {
      headers: {
        "Content-Type": "application/json",
        'Authentication-Token': this.accessToken
      }
    })
    .then(response => {
      console.log(response.data.categories);
      this.categories=response.data.categories
    })
    .catch(error => {
      // Handle errors here
      console.error('Error:', error);
    });
  },
  
  methods:{
    logout() {
      localStorage.clear(),
      this.$router.push('/')
    },

  },
};
  </script>
  
  <style scoped>
  .bg-f {
    background: #ec008c;
    background: -webkit-linear-gradient(to right, #fc6767, #ec008c);
    background: linear-gradient(to right, #fc6767, #ec008c);
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  
  .container {
    max-width: 800px;
    margin: 0 auto;
    padding: 30px;
    text-align: center;
  }
  
  .confirmation-title {
    color: blueviolet;
    font-family: Arial;
    font-size: 60px;
    margin-bottom: 40px;
  }
  
  .confirmation-message {
    color: white;
    font-size: 40px;
    margin-bottom: 20px;
  }
  
  .btn {
    display: inline-block;
    padding: 10px 20px;
    background-color: blue;
    color: white;
    text-decoration: none;
    border-radius: 5px;
    font-size: 30px;
    margin: 10px;
  }
  </style>
  