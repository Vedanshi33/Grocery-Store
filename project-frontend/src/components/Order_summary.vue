<template>
    <div class="my-orders-container">
      <h1 class="my-orders-title">My Orders</h1>
      <div v-if="loading">Loading...</div>
      <div v-else>
        <table class="my-orders-table white-bg">
          <thead>
            <tr>
              <th>Date</th>
              <th>Product Name</th>
              <th>Total Bill Paid</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(order, index) in orders" :key="index">
              <td>{{ order.date }}</td>
              <td>{{ order.product_name }}</td>
              <td>{{ order.total_bill_paid }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        orders: [],
        loading: true,
      };
    },
    mounted() {
      this.fetchMyOrders();
    },
    methods: {
      fetchMyOrders() {
        
        const apiUrl = 'http://127.0.0.1:5000/my_orders';
  
       
        const headers = {
          'Content-Type': 'application/json',
          'Authentication-Token': localStorage.getItem('access_token'),
        };
  
        // Make a GET request to the API endpoint with headers
        axios.get(apiUrl, { headers })
          .then((response) => {
            // Update the component data with the received data
            this.orders = response.data;
            this.loading = false;
          })
          .catch((error) => {
            console.error('Error fetching my orders:', error);
            this.loading = false;
          });
      },
    },
  };
  </script>
  


  <style scoped>
  .my-orders-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
  }
  
  .my-orders-title {
    font-size: 24px;
    margin-bottom: 15px;
    color: #007bff; /* Nice font color */
  }
  
  .loading-message {
    font-size: 18px;
    color: #555;
  }
  
  .my-orders-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 15px;
  }
  
  .my-orders-table th,
  .my-orders-table td {
    padding: 12px;
    text-align: left;
    border-bottom: 1px solid #ddd;
  }
  
  .my-orders-table th {
    background-color: #f2f2f2; /* Header background color */
  }
  
  .my-orders-table tbody tr.white-bg:hover {
    background-color: #f5f5f5;
  }
  
  .white-bg {
    background-color: #fff; /* White background color */
  }
  </style>