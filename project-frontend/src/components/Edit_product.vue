<template>
  <div class="bg-f">
    <h1 class="title">Edit Product</h1>
    <form @submit.prevent="updateProduct" enctype="multipart/form-data">
      <div>
        <label for="p_id">Product ID:</label>
        <input v-model="productData.productID" type="number" id="p_id" name="p_id"><br><br>
        <label for="p_name">Product Name:</label>
        <input v-model="productData.productName" type="text" id="p_name" name="p_name"><br><br>
        <label for="p_image">Product Image</label>
        <input v-on:change="onFileChange" type="file" name="p_image"><br><br>
        <label for="manufacturing_date">Manufacturing Date:</label>
        <input v-model="productData.manufacturingDate" type="date" id="manufacturing_date" name="manufacturing_date"><br><br>
        <label for="rate_per_unit">Price:</label>
        <input v-model="productData.price" type="number" id="rate_per_unit" name="rate_per_unit"><br><br>
        <label for="details">Details:</label>
        <input v-model="productData.details" type="text" id="details" name="details"><br><br>
        <label for="quantity">Quantity</label>
        <input v-model="productData.quantity" type="text" id="quantity" name="quantity"><br><br>
        <label for="quantity_unit">Quantity Unit:</label>
        <input v-model="productData.quantityUnit" type="text" id="quantity_unit" name="quantity_unit"><br><br>
      </div>
      <div>
        <button type="submit" class="btn-update">Update</button><br><br>
      </div>
    </form>
    <form @submit.prevent="deleteProduct" style="margin-top: 20px;">
      <button type="submit" class="btn-delete">Delete</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      category_Id:this.$route.params.category_id,
      accessToken: localStorage.getItem('access_token'),
      productData: {
        productID: this.$route.params.product_id,
        productName: "",
        productImage:null,
        manufacturingDate: "",
        price: "",
        details: "",
        quantity: "",
        quantityUnit: "",
      },
      
    };
  },
  methods: {
    onFileChange(event) {
      this.productImage = event.target.files[0];
    },
    deleteProduct() {
      console.log('Product ID to delete:', this.productData.productID);
      
      // Check if you have a valid product ID to delete
      if (this.productData.productID) {
        axios.delete(`http://127.0.0.1:5000/delete_product/${this.category_Id}/${this.productData.productID}`, {
          headers: {
            'Authentication-Token': this.accessToken
          },
        })
        .then(response => {
          // Handle success response
          console.log(response.data);
          
        })
        .catch(error => {
          // Handle error response
          console.error('Error deleting product:', error);
        });
      } else {
        // Handle case where product ID is not available
        console.error('Product ID is not valid.');
      }
    },
    updateProduct() {
      console.log('Updating product...');

      let formData = new FormData();
      formData.append('p_id', this.productData.productID);
      formData.append('p_image', this.productImage);
      formData.append('p_name', this.productData.productName);
      formData.append('manufacturing_date', this.productData.manufacturingDate);
      formData.append('rate_per_unit', this.productData.price);
      formData.append('details', this.productData.details);
      formData.append('quantity', this.productData.quantity);
      formData.append('quantity_unit', this.productData.quantityUnit);

      axios.post(`http://127.0.0.1:5000/edit_product/${this.productData.productID}`, formData, {
        headers: {
          'Authentication-Token': this.accessToken
        }
      })
      .then(response => {
        console.log(response.data);
      })
      .catch(error => {
        console.error('Error updating product:', error);
      });
    }
  }
}
</script>

<style scoped>

.bg-f {
  background: #ec008c;
  background: -webkit-linear-gradient(to right, #fc6767, #ec008c);
  background: linear-gradient(to right, #fc6767, #ec008c);
}

.btn-update {
  background-color: green;
  color: white;
  font-size: 20px;
}

.btn-delete {
  background-color: brown;
  color: white;
  font-size: 20px;
}
</style>
