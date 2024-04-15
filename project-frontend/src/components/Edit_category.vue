
  <template>
    <div class="bg-f">
      <h1 style="font-size: bold; color: blue; text-decoration: underline;">Edit Category</h1>
      <form @submit.prevent="updateCategory" >
        <div class="form-group">
          <label for="category_id">Category ID:</label>
          <input type="text" class="form-control" v-model="categoryId">
        </div>
        <div>
          <label for="category_name" style="color: azure; font-size: 30px; font-weight: bold;">Category Name:</label>
          <input v-model="categoryName" type="text" name="category_name" style="font-size: 20px;">
        </div>
        <div style="margin-top: 20px;">
          <label for="image" style="color: azure; font-size: 30px; font-weight: bold;">Image:</label>
          <input v-on:change="onFileChange" type="file" name="image" style="font-size: 20px;">
        </div>
        <div style="margin-top: 20px;">
          <button @click="updateCategory()" style="background-color: green; color: white; font-size: 20px;">Update</button>
        </div>
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
      imageFile: null,
      accessToken: localStorage.getItem('access_token'),
      role: localStorage.getItem('role')
    };
  },
  methods: {
    onFileChange(event) {
      this.imageFile = event.target.files[0]; 
    },
    updateCategory() {
      console.log('Updating category...');

      let formData = new FormData();
      formData.append('category_id', this.categoryId);
      formData.append('category_name', this.categoryName);
      formData.append('image', this.imageFile);

      axios.post(`http://127.0.0.1:5000/edit_category/${this.categoryId}`, formData, {
         headers: {
           'Authentication-Token': this.accessToken
         }
        
       })
       .then(response => {
        
         console.log(response.data);
         if (this.role === 'store manager'){
          alert('request has been sent to admin')
         }
       })
       .catch(error => {
         console.error('Error updating category:', error);
        
       });
    }
  }
};
</script>

<style scoped>

.bg-f {
  background: #ec008c;
  background: -webkit-linear-gradient(to right, #fc6767, #ec008c);
  background: linear-gradient(to right, #fc6767, #ec008c);
}
</style>

  