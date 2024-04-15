<template>
  <div>
    <h1>Cart</h1>
    <div>
      <h2>Cart Details</h2>
      <table>
        <thead>
          <tr>
            <th>Product Name</th>
            <th>Quantity</th>
            <th>Price</th>
            <th>Total Price</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="cartItem in cartItems" :key="cartItem.product_id">
            <td>{{ cartItem.product_name }}</td>
            <td>{{ cartItem.quantity }}</td>
            <td>
              Rs {{ (cartItem.price).toFixed(2) }}
            </td>
            <td>
              Rs {{ (cartItem.total_price).toFixed(2) }}
            </td>
            <td>
              <button @click="removeFromCart(cartItem.product_id)" class="btn btn-danger">Remove</button>
            </td>
          </tr>
        </tbody>
      </table>
      <p class="total-amount">Total Amount: Rs {{ totalAmount.toFixed(2) }}</p><br><br>
    </div>

    <div class="cart-actions">
      <button @click="$router.push('/user_dashboard')">Continue Shopping</button>
      <button @click="$router.push('/billing')">Proceed to Billing</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      accessToken: localStorage.getItem('access_token'),
      cartItems: [],
      totalAmount: 0,
    };
  },
  mounted() {
    

    this.fetchCartData();
  },
  methods: {
    fetchCartData() {
      axios.get(`http://127.0.0.1:5000/cart`, {
        headers: {
          "Content-Type": "application/json",
          'Authentication-Token': this.accessToken
        }
      })
      .then(response => {
        this.cartItems = response.data.cart_items;
        this.totalAmount = response.data.total_amount;
        
      })
      .catch(error => {
        console.error('Error fetching cart data:', error);
      });
    },
    removeFromCart(productId) {
      console.log('Removing product with ID:', productId);
      axios.delete(`http://127.0.0.1:5000/remove_from_cart/${productId}`, {
       headers: {
        "Content-Type": "application/json",
         'Authentication-Token': this.accessToken
    },
  })
  .then((response) => {
    console.log('Product removed successfully:', response.data.message);
  // Update cart data after removal
    this.fetchCartData();
})
  .catch((error) => {
  console.error("Error removing product from cart:", error);
});
}

  }
};
</script>

<style scoped>

</style>
  