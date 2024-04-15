<template>
  <div>
    <div
      class="d-flex flex-column flex-md-row align-items-center p-3 px-md-4 mb-3 bg-white border-bottom shadow-sm u-nav">
      <div class="container">
        <h5 class="my-0 mr-md-auto font-weight-normal">GROCERY STORE</h5>
        <router-link to="/" style="margin-right: 10px;">Home</router-link>
        <router-link to="/Create_category" style="margin-right: 10px;">Add Category</router-link>
        
        <router-link to="/admin_summary" style="margin-right: 10px;">Summary of Orders</router-link>
        <router-link to="/request" style="margin-right: 10px;">Requests</router-link>
        

        
        <button @click="logout" class="btn btn-outline-primary">Logout</button>
      </div>
    </div>

    <ul class="category-list">
      <div class="category-box" v-for="category in categories" :key="category.id">
        <li>
          <div style="color: white; font-size: x-large;">
            {{ category.name }}
          </div><br>
          
          <img :src="'http://127.0.0.1:5000/static/images/' + category.image" :alt="category.name" height="400"
            width="400"><br><br>
          <router-link :to="'/edit_category/' + category.id" class="btn btn-primary">Edit Category</router-link><br><br>
          <div class="inner-box">
           
            
            <form class="remove-form" @submit.prevent="deleteCategory(category.id)">
              <button type="submit" style="background-color: red; color: white; font-size: 20px;">Delete</button>
              <input type="hidden" name="confirm_delete" value="1">
            </form>
          </div>
        </li>
      </div>
    </ul>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      accessToken: localStorage.getItem('access_token'),
      searchQuery: '',
      quantity: 1,
      searchResults: [],
      categories: [],
      role: localStorage.getItem('role')
    };
  },
  mounted() {
    // const categoryId = this.$route.params.category_id;
    axios.get(`http://127.0.0.1:5000/categories`, {
      headers: {
        "Content-Type": "application/json",
        'Authentication-Token': this.accessToken
      }
    })
      .then(response => {
        console.log(response.data.categories);
        this.categories = response.data.categories
      })
      .catch(error => {
        // Handle errors here
        console.error('Error:', error);
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
          if (this.role === 'store manager') {
          alert(response.data.message)
        } else {
          this.categories = this.categories.filter(category => category.id !== category_id);
        }
          // Remove the deleted category from the 'categories' array
          
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
    searchProducts() {
      axios
        .get(`http://127.0.0.1:5000/search_products?query=${this.searchQuery}`, {
          headers: {
            'Authentication-Token': this.accessToken,
          },
        })
        .then((response) => {
          this.searchResults = response.data.product_results;
          this.categories = response.data.category_results;
        })
        .catch((error) => {
          console.error('Error fetching search results:', error);
        });
    },

    logout() {
      localStorage.clear(),
        this.$router.push('/')
    },
    export_products(){
      axios
        .get(`http://127.0.0.1:5000/export`, {
          headers: {
            'Authentication-Token': this.accessToken,
          },
        })
        .then((response) => {
          alert(response.data.message)
        })
        .catch((error) => {
          console.error('Error fetching search results:', error);
        });
    },
  },
};
</script>

<style scoped>
/* Add your component-specific styles here */
.container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 10px;
  /* Adjust the margin value as needed */
}

.container router-link,
.container button {
  margin-left: 10px;
  /* Adjust the margin value as needed */
}
</style>