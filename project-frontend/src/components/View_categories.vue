<template>
  <div class="bg-f">
    <h1 style="font-size: bold; color: blue; text-decoration: underline;">Categories</h1>
    <div class="category-container">
      <div v-for="category in categories" :key="category.id" class="category-item">
        <h2 style="color: azure; font-size: 30px; font-weight: bold;">Category ID: {{ category.id }}</h2>
        <h2 style="color: blue; font-size: 30px; font-weight: bold;">Category Name: {{ category.name }}</h2>
        <img :src="'http://127.0.0.1:5000/static/images/' + category.image" :alt="category.name" height="300" /><br /><br />
        <button @click="deleteCategory(category.id)"
          style="background-color: red; color: white; font-size: 25px;">Delete</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      categories: [],
      accessToken: localStorage.getItem('access_token')
    }
  },
  mounted() {
    // console.log('hello from mounted')
    axios.get('http://127.0.0.1:5000/categories', {
      headers: {
        "Content-Type":"application/json",
        'Authentication-Token': this.accessToken
      }
    })
      .then(response => {
        // console.log(response.data)
        this.categories = response.data.categories;
      })
      .catch(error => {
        console.error('Error fetching categories:', error);
      });
  },
  methods: {
  deleteCategory(category_id) {
    console.log('Deleting category with ID:', category_id);
    axios.delete(`http://127.0.0.1:5000/remove_category/${category_id}`, {
      headers: {
        'Authentication-Token': this.accessToken
      }
    })
      .then(response => {
        // Handle successful deletion
        console.log(response.data.message);
        // Remove the deleted category from the 'categories' array
        this.categories = this.categories.filter(category => category.id !== category_id);
      })
      .catch(error => {
        // Handle deletion error
        if (error.response) {
          // The request was made and the server responded with a status code
          // that falls out of the range of 2xx
          console.error('Server Error:', error.response.data);
          console.error('Status Code:', error.response.status);
        } else if (error.request) {
          // The request was made but no response was received
          console.error('No response received from the server:', error.request);
        } else {
          // Something happened in setting up the request that triggered an Error
          console.error('Error message:', error.message);
        }
      });
  },

  }
}


</script>

<style scoped>

</style>
