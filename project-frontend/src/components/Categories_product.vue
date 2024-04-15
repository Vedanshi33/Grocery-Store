<template>
  <div class="categories-container">
    <h1 class="category-title">{{ category.category_name }} Products</h1>
    <div class="product" v-for="product in category.products" :key="product.product_id">
      <h3 class="product-name">{{ product.product_name }}</h3>
      <img :src="'http://127.0.0.1:5000/static/images/' + product.p_image" :alt="product.product_name"
        class="product-image" />

      
      <div v-if="product.demand_factor > 1.0">
        <div class="price-hike">
          Hike Now the product is at Rs {{ (product.rate_per_unit * product.demand_factor).toFixed(2) }}
        <p class="original-price">Rate per unit: Rs {{ product.rate_per_unit.toFixed(2) }}</p>
        <p class="manufacturing-date">Manufacturing Date: {{ formatDate(product.manufacturing_date) }}</p>
        <p class="product-details">Details: {{ product.product_details }}</p>
        </div>
      </div>
      <div v-else-if="product.demand_factor < 1.0">
        <div class="price-discount">
          Discount Now the product is at Rs {{ (product.rate_per_unit * product.demand_factor).toFixed(2) }}
        </div>
        <p class="manufacturing-date">Manufacturing Date: {{ formatDate(product.manufacturing_date) }}</p>
        <p class="product-details">Details: {{ product.product_details }}</p>
      </div>
      <div v-else>
        <p class="original-price">Rate per Unit: Rs {{ product.rate_per_unit.toFixed(2) }}</p>
        <p class="manufacturing-date">Manufacturing Date: {{ formatDate(product.manufacturing_date) }}</p>
        <p class="product-details">Details: {{ product.product_details }}</p>
      </div>




      <form @submit.prevent="addToCart(product.product_id, quantity)">
        <label for="quantity">Quantity: </label>
        <input v-model="quantity" type="number" id="quantity" min="1" />
        <button type="submit" class="add-to-cart-button">Add to Cart</button>
      </form>
    </div>
  </div>
</template>


<script>
import axios from 'axios';

export default {
  
  data() {
    return {
      accessToken: localStorage.getItem('access_token'),
      category: {},
      quantity: 1
    };
  },
  mounted() {
    const categoryId = this.$route.params.category_id;
    axios.get(`http://127.0.0.1:5000/category/${categoryId}`, {
      headers: {
        "Content-Type": "application/json",
        'Authentication-Token': this.accessToken
      }
    })
      .then(response => {
        console.log(response.data.products);
        this.category = response.data
      })
      .catch(error => {
        // Handle errors here
        console.error('Error:', error);
      });
  },
  methods: {

    addToCart(productId, quantity) {
      axios.post(`http://127.0.0.1:5000/add_to_cart/${productId}`, { 'quantity': quantity }, {
        headers: {
          "Content-Type": "application/json",
          'Authentication-Token': this.accessToken
        }
      })
        .then(response => {
          console.log(response.data.message);
          this.$router.push(`/cart`);
          this.$emit('added-to-cart', response.data.message);
        })
        .catch(error => {
          console.error('Error adding to cart:', error);
          if (error.response && error.response.status === 400) {
            alert("This product is currently OUT OF STOCK");
          } else {
            alert("An error occurred while adding the product to the cart.");
          }
        });
    },
    formatDate(date) {
      const options = { year: 'numeric', month: 'long', day: 'numeric' };
      const formattedDate = new Date(date).toLocaleDateString(undefined, options);
      return formattedDate;

    }
  }
};
</script>

<style scoped>
.categories-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-start;
  align-items: flex-start;
}

.product {
  display: inline-block;
  width: 45%;
  margin: 10px;
  text-align: center;
}

.product img {
  width: 100%;
  height: 400px;
  object-fit: cover;
}

.price-hike {
  color: red;
  font-weight: bold;
}

.price-discount {
  color: green;
  font-weight: bold;
}

.original-price {
  font-weight: bold;
  font-size: 16px;
}

.manufacturing-date {
  font-weight: bold;
  font-size: 16px;
}

.product-details {
  color:black;
  font-weight: bold;
  font-size: 16px;
}
</style>
