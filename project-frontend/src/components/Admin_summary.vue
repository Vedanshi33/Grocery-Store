<template>
    <div class="admin-summary-container">
      <h1 class="admin-summary-title">Admin Summary</h1>
      <div v-if="loading" class="loading-message">Loading...</div>
      <div v-else>
        <table class="order-table">
          <thead>
            <tr>
              <th>Order ID</th>
              <th>Product ID</th>
              <th>Quantity</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in orderItems" :key="item.order_id" class="order-item">
              <td>{{ item.order_id }}</td>
              <td>{{ item.product_id }}</td>
              <td>{{ item.quantity }}</td>
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
        accessToken: localStorage.getItem('access_token'),
        orderItems: [],
        loading: true,
      };
    },
    mounted() {
      this.fetchAdminSummary();
    },
    methods: {
      fetchAdminSummary() {
        
        const apiUrl = 'http://127.0.0.1:5000/admin/summary';
  
        
        const headers = {
          'Content-Type': 'application/json',
          'Authentication-Token': this.accessToken,
        };
  
        
        axios.get(apiUrl, { headers })
          .then((response) => {
            
            this.orderItems = response.data.order_items;
            this.loading = false;
          })
          .catch((error) => {
            console.error('Error fetching admin summary:', error);
            this.loading = false;
          });
      },
    },
  };
  </script>
  
  <style scoped>
  .admin-summary-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
  }
  
  .admin-summary-title {
    font-size: 24px;
    margin-bottom: 15px;
    color: #333; /* Nice font color */
  }
  
  .loading-message {
    font-size: 18px;
    color: #555;
  }
  
  .order-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 15px;
  }
  
  .order-table th,
  .order-table td {
    padding: 12px;
    border: 1px solid #ddd;
    text-align: left;
  }
  
  .order-table th {
    background-color: #f2f2f2; /* Header background color */
  }
  
  .order-item {
    margin-bottom: 10px;
    background-color: #f9f9f9;
  }
  </style>
  