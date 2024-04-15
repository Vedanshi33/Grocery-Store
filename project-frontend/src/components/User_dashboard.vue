<template>
  <div>
    <div class="d-flex flex-column flex-md-row align-items-center p-3 px-md-4 mb-3 bg-white border-bottom shadow-sm u-nav">
      <h5 class="my-0 mr-md-auto font-weight-normal">Grocery Store</h5>
      <router-link  to="/" style="margin-right: 10px;">Home</router-link>
      <router-link  to="/order_summary" style="margin-right: 10px;">My orders</router-link>
      <router-link  to="/cart" style="margin-right: 10px;">My Cart</router-link>
      
      <router-link  to="/request" style="margin-right: 10px;">Request</router-link>
      <button @click="logout" class="btn btn-outline-primary">Logout</button>
      
      
    </div>

    <div class="container">
      <div class="row">
        <div class="col-md-6 offset-md-3">
          <form @submit.prevent="searchProducts" class="text-center">
            <div class="form-group">
              <input v-model="searchQuery" type="text" class="form-control" placeholder="Search for products/categories/price">
              
            </div>
            <button type="submit" class="btn btn-primary">Search</button><br><br>
          </form>
        </div>
      </div>
    </div>

    <div class="categories-container">
      <div class="row">
        <div v-for="category in categories" :key="category.id" class="col-md-4">
          <div class="category-box" :style="{ backgroundColor: 'rgba(231, 228, 34, 0.862)', color: 'rgb(246, 46, 46)', padding: '10px', marginBottom: '10px', border: '1px solid rgb(13, 0, 128)' }">
            <h2>
              <router-link :to="'/category/' + category.id" style="display: inline-block; padding: 10px 20px; background-color: green; color: white; text-decoration: none;">
                {{ category.name }}
              </router-link>
            </h2>
            <img :src="'http://127.0.0.1:5000/static/images/' + category.image" :alt="category.name" height="250" width="350"><br><br>
            <router-link :to="'/category/' + category.id"><button class="btn text-dark" >View Category</button></router-link>
          </div>
        </div>
      </div>
    </div>

    <div class="container mt-4">
      <div class="row">
        <div v-if="searchResults && searchResults.length > 0">
        <div  v-for="product in searchResults" :key="product.p_id" class="col-md-4">
          <div class="card">
            <div class="card-body">
              <img :src="'http://127.0.0.1:5000/static/images/' + product.p_image" :alt="product.p_name" style="height: 300px; width: 300px;">
              <h5 class="card-title">{{ product.p_name }}</h5>
              <p class="card-text">Rate per Unit: Rs {{ product.rate_per_unit }}</p>
              <p class="card-text">Unit: {{ product.unit }}</p>
              
              
              <form @submit.prevent="addToCart(product.p_id)" class="mt-2">
                <label for="quantity">Quantity: </label>
                <input type="number" id="quantity" v-model="quantity" min="1" :max="product.quantity">
                <button type="submit" class="btn btn-primary">Add to Cart</button>
              </form>
            </div>
          </div>
        </div>
        </div>
      </div>
    </div>
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
      this.categories=response.data.categories
    })
    .catch(error => {
      // Handle errors here
      console.error('Error:', error);
    });
  },
  methods: {
    searchProducts() {
      axios
        .get(`http://127.0.0.1:5000/search_products?query=${this.searchQuery}`, {
          headers: {
            'Authentication-Token': this.accessToken,
          },
        })
        .then((response) => {
          console.log(response.data)
          this.searchResults = response.data.product_results;
          this.categories = response.data.category_results;
        })
        .catch((error) => {
          console.error('Error fetching search results:', error);
        });
    },
    formatManufacturingDate(date) {
      const options = { year: 'numeric', month: 'long', day: 'numeric' };
      const formattedDate = new Date(date).toLocaleDateString(undefined, options);
      return formattedDate;
    },
    addToCart(productId) {
     
         axios.post(
          `http://127.0.0.1:5000/add_to_cart/${productId}`,
          { quantity: this.quantity },
          {
            headers: {
              'Content-Type': 'application/json',
              'Authentication-Token': this.accessToken,
            },
          }
        )
        .then((response) => {
          console.log(response.data.message);
          this.$emit('added-to-cart', response.data.message);
        })
        .catch((error) => {
          console.error('Error adding to cart:', error);
        });
    },
    logout() {
      localStorage.clear(),
      this.$router.push('/')
    },
  },
};
</script>

<style scoped>
/* Add your component-specific styles here */
</style>