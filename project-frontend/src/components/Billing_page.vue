<template>
    <div class="billing-container">
      <h1 class="billing-title">Billing</h1>
      <form @submit.prevent="confirmOrder">
        <label for="payment_method">Select Payment Method:</label>
        <select v-model="selectedPaymentMethod" id="payment_method" name="payment_method">
          <option value="upi">UPI</option>
          <option value="card">Card</option>
          <option value="cash_on_delivery">Cash on Delivery</option>
        </select>
        <br><br>
        <button type="submit" class="confirm-order-button">Confirm Order</button>
      </form>
    </div>
  </template>
  
  <script>
import axios from 'axios';
  export default {
    data() {
      return {
        accessToken: localStorage.getItem('access_token'),

        selectedPaymentMethod: 'upi'
      };
    },
   
    methods: {
      confirmOrder() {
        const dataToSend = {
        payment_method: this.selectedPaymentMethod
     
      };

      
      axios.post('http://127.0.0.1:5000/confirmation', dataToSend,{
      headers: {
        "Content-Type": "application/json",
        'Authentication-Token': this.accessToken
      }
    })
        .then(response => {
          console.log('Order confirmation successful:', response.data.message);
          this.$router.push(`/confirmation`);
         
        })
        .catch(error => {
            if (error.response) {
          // The request was made and the server responded with a status code
          // that falls out of the range of 2xx
          console.error('Error response data:', error.response.data);
          console.error('Error response status:', error.response.status);
          console.error('Error response headers:', error.response.headers);
        } else if (error.request) {
          // The request was made but no response was received
          console.error('Error request data:', error.request);
        } else {
          // Something happened in setting up the request that triggered an Error
          console.error('Error message:', error.message);
        }
        console.error('Error confirming order:', error.config);
      });
       
        
      }
    }
  };
  </script>
  
  <style scoped>
  .billing-container {
    max-width: 350px;
    margin: 0 auto;
    padding: 30px;
    background-color: #fff;
    border-radius: 5px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  }
  
  .billing-title {
    color: #007bff;
    text-align: center;
    margin-top: 20px;
  }
  
  label {
    display: block;
    margin-bottom: 15px;
    font-weight: bold;
  }
  
  select {
    width: 100%;
    padding: 12px;
    font-size: 16px;
    border: 1px solid #ccc;
    border-radius: 5px;
  }
  
  .confirm-order-button {
    display: block;
    width: 100%;
    padding: 12px;
    font-size: 16px;
    background-color: #007bff;
    color: #fff;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    margin-top: 15px;
  }
  
  .confirm-order-button:hover {
    background-color: #0056b3;
  }
  </style>
  