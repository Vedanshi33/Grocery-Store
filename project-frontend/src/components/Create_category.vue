<template>
  <div>
    <h2>Create Category</h2>
    <form @submit.prevent="createCategory">
      <div class="form-group">
        <label for="category_id">Category ID:</label>
        <input type="text" class="form-control" v-model="categoryId" required>
      </div>
      <div class="form-group">
        <label for="category_name">Category Name:</label>
        <input type="text" class="form-control" v-model="categoryName" required>
      </div>
      <div class="form-group">
        <label for="image">Category Image:</label>
        <input type="file" class="form-control" @change="handleFileUpload" required>
      </div>
      <button type="submit" class="btn btn-primary">Create Category</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      categoryId: '',
      categoryName: '',
      image: null,
      accessToken: localStorage.getItem('access_token'),
      role: localStorage.getItem('role')
    };
  },
  methods: {
    handleFileUpload(event) {
      this.image = event.target.files[0];
    },
    createCategory() {
      const formData = new FormData();
      formData.append('category_id', this.categoryId);
      formData.append('category_name', this.categoryName);
      formData.append('file', this.image);

      axios.post('http://127.0.0.1:5000/create_category', formData, {
        headers: {
          'Authentication-Token': this.accessToken
        }
      })
      .then(response => {
        if (this.role === 'store manager'){
          alert('request has been sent to admin')
         }
        console.log(response.data.message);
        this.$router.push('/view_categories')
      
      })
      .catch(error => {
        console.error('Error creating category:', error);
       
        if (error.response) {
         
          console.error('Response data:', error.response.data);
          console.error('Response status:', error.response.status);
          console.error('Response headers:', error.response.headers);
        } else if (error.request) {
         
          console.error('Request data:', error.request);
        } else {
       
          console.error('Error message:', error.message);
        }
       
      });
    }
  }
}
</script>
