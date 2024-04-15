<template>
    <div class="bg-f">
        <h1 style="font-size: bold; color: blue; text-decoration: underline;">
            Add Product to {{ category_name }}
        </h1>

        <form @submit.prevent="submitForm" enctype="multipart/form-data">
            <label for="p_id" style="color: azure; font-size: 30px; font-weight: bold;">
                Product ID:
            </label>
            <input v-model="productID" type="number" id="p_id" required /><br /><br />
            <label for="p_name" style="color: azure; font-size: 30px; font-weight: bold;">
                Product Name:
            </label>
            <input v-model="productName" type="text" id="p_name" required /><br /><br />

            <label for="p_image" style="color: azure; font-size: 30px; font-weight: bold;">
                Product Image
            </label>
            <input type="file" id="p_image" ref="fileInput" @change="handleFileChange" required /><br /><br />

            <label for="manufacturing_date" style="color: azure; font-size: 30px; font-weight: bold;">
                Manufacturing Date:
            </label>
            <input v-model="manufacturingDate" type="date" id="manufacturing_date" required /><br /><br />

            <label for="rate_per_unit" style="color: azure; font-size: 30px; font-weight: bold;">
                Price:
            </label>
            <input v-model="price" type="number" id="rate_per_unit" required /><br /><br />

            <label for="details" style="color: azure; font-size: 30px; font-weight: bold;">Details:</label>
            <input v-model="details" type="text" id="details" required /><br /><br />

            <label for="quantity" style="color: azure; font-size: 30px; font-weight: bold;">Quantity</label>
            <input v-model="quantity" type="text" id="quantity" required /><br /><br />

            <label for="name" style="color: azure; font-size: 30px; font-weight: bold;">
                Quantity Unit:
            </label>
            <input v-model="quantityUnit" type="text" id="quantity_unit" required /><br /><br />

            <button type="submit" style="background-color: green; color: white; font-size: 20px;">
                Add Product
            </button>
        </form>
    </div>
</template>
  
  
<script>
import axios from "axios";

export default {
    data() {
        return {
            category_name: null,
            productID:'',
            productName: "",
            productImage: null,
            manufacturingDate: "",

            price: "",
            details: "",
            quantity: "",
            quantityUnit: "",
            accessToken: localStorage.getItem('access_token')
        };
    },
    mounted() {

        const categoryId = this.$route.params.category_id;

        axios.get(`http://127.0.0.1:5000/add_product/${categoryId}`, {
            headers: {
                'Authentication-Token': this.accessToken
            }
        })
            .then(response => {
                // console.log(response.data)
                this.category_name = response.data.category.name;
                //   console.log(this.category)
            })
            .catch(error => {
                console.error("Error fetching category data:", error);
            });
    },

    methods: {
        handleFileChange(event) {
            this.imageFile = event.target.files[0];
            // console.log(this.imageFile)
        },
        submitForm() {
        const categoryId = this.$route.params.category_id;

        const formData = new FormData();
        // console.log(this.productImage)
        formData.append('p_id', this.productID);
        formData.append('p_image', this.imageFile,this.imageFile.name); 
        formData.append('p_name', this.productName);
        formData.append('manufacturing_date', this.manufacturingDate);
        formData.append('rate_per_unit', this.price);
        formData.append('details', this.details);
        formData.append('quantity', this.quantity);
        formData.append('quantity_unit', this.quantityUnit);

        axios.post(`http://127.0.0.1:5000/add_product/${categoryId}`, formData, {
            headers: {
                'Content-Type': 'multipart/form-data', 
                'Authentication-Token': this.accessToken
            }
        })
            .then(response => {
                console.log(response.data.message);
                this.$router.push(`/category/${categoryId}`);

               

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
  
<style scoped>
.bg-f {
    background: #ec008c;
    background: -webkit-linear-gradient(to right, #fc6767, #ec008c);
    background: linear-gradient(to right, #fc6767, #ec008c);
}
</style>
  