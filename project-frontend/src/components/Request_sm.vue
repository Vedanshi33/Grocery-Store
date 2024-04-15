<template>
    <div v-if="role === 'admin'">
        <h3>
            Store Manager requests
        </h3>
        <table v-if="sm_requests.length !== 0">
            <tr>
                <th>Firstname</th>
                <th>Lastname</th>
                <th>Email</th>
                <th>Action</th>
            </tr>
            <tr class="" v-for="user in sm_requests" :key="user.id">
                <td>
                    {{ user.first_name }}
                </td>
                <td>
                    {{ user.last_name }}
                </td>
                <td>
                    {{ user.email }}
                </td>
                <td>
                    <button @click="accept_request(user.id)">
                        Accept
                    </button>
                    <button @click="reject_request(user.id)">
                        Reject
                    </button>
                </td>
            </tr>
        </table>
        <div v-else>
            There is no pending store manager request
        </div>
        <br>
        <br>
        <h3>
            Category requests
        </h3>
        <table v-if="requests.length !== 0" border="1px" width="100%">
            <tr>
                <th>SM Firstname</th>
                <th>SM Lastname</th>
                <th>SM Email</th>
                <th>Type</th>
                <th>Details</th>
                <th>Action</th>
            </tr>
            <tr class="" v-for="req in requests" :key="req.id">
                <td>
                    {{ req.first_name }}
                </td>
                <td>
                    {{ req.last_name }}
                </td>
                <td>
                    {{ req.email }}
                </td>
                <td>
                    {{ req.request_type }}
                </td>
                <td>
                    <div v-if="req.request_type === 'create'">
                        Category Name: {{ req.name }}
                        <br>
                        Category Image:<br>
                        <img :src="'http://127.0.0.1:5000/static/images/' + req.image" :alt="req.name" height="100"
                            width="100">
                    </div>
                    <div v-else-if="req.request_type === 'edit'">
                        New Category Name: {{ req.name }}
                        <br>
                        New Category Image:<br>
                        <img :src="'http://127.0.0.1:5000/static/images/' + req.image" :alt="req.name" height="100"
                            width="100">
                        <br>
                        <br>
                        Old Category Name: {{ req.category_name }}
                        <br>
                        Old Category Image:<br>
                        <img :src="'http://127.0.0.1:5000/static/images/' + req.category_image" :alt="req.category_name"
                            height="100" width="100">
                    </div>
                    <div v-else>
                        Category Name: {{ req.category_name }}
                        <br>
                        Category Image:<br>
                        <img :src="'http://127.0.0.1:5000/static/images/' + req.category_image" :alt="req.category_name"
                            height="100" width="100">
                    </div>
                </td>
                <td>
                    <button @click="accept_category_request(req.id)">
                        Accept
                    </button>
                    <button @click="reject_category_request(req.id)">
                        Reject
                    </button>
                </td>
            </tr>
        </table>
        <div v-else>
            There is no pending Category request
        </div>
    </div>
    <div v-else-if="role === 'store manager'">
        <h3>
            Category requests
        </h3>
        <table v-if="requests.length !== 0" border="1px" width="100%">
            <tr>
                <th>Status</th>
                <th>Type</th>
                <th>Details</th>
                <th>Action</th>
            </tr>
            <tr class="" v-for="req in requests" :key="req.id">
                <td>
                    {{ req.status }}
                </td>
                <td>
                    {{ req.request_type }}
                </td>
                <td>
                    <div v-if="req.request_type === 'create' && req.status !== 'accepted'">
                        Category Name: {{ req.name }}
                        <br>
                        Category Image:<br>
                        <img :src="'http://127.0.0.1:5000/static/images/' + req.image" :alt="req.name" height="100"
                            width="100">
                    </div>
                    <div v-else-if="req.request_type === 'edit' && req.status !== 'accepted'">
                        New Category Name: {{ req.name }}
                        <br>
                        New Category Image:<br>
                        <img :src="'http://127.0.0.1:5000/static/images/' + req.image" :alt="req.name" height="100"
                            width="100">
                        <br>
                        <br>
                        Current Category Name: {{ req.category_name }}
                        <br>
                        Current Category Image:<br>
                        <img :src="'http://127.0.0.1:5000/static/images/' + req.category_image" :alt="req.category_name"
                            height="100" width="100">
                    </div>
                    <div v-else-if="req.request_type === 'delete'">
                        Category Name: {{ req.name }}
                        <br>
                        Category Image:<br>
                        <img :src="'http://127.0.0.1:5000/static/images/' + req.image" :alt="req.name"
                            height="100" width="100">
                    </div>
                    <div v-else>
                        Category Name: {{ req.name }}
                        <br>
                        Category Image:<br>
                        <img :src="'http://127.0.0.1:5000/static/images/' + req.image" :alt="req.name"
                            height="100" width="100">
                    </div>
                </td>
                <td>
                    <div v-if="req.status === 'pending'">
                        <button @click="reject_category_request(req.id)">
                            Cancel
                        </button>
                    </div>
                    <div v-else>
                        N/A
                    </div>
                </td>
            </tr>
        </table>
        <div v-else>
            There is no pending Category request
        </div>
    </div>
    <div v-else>
        <div v-if="status === 'rejected'">
            <p>
                Click On Button to make request to become store manager : <button @click="send_StoreManagerRequest()">Click
                    me</button>
                <br>
                Note: if you have already sent request and not it is showing you option to make request again this means
                admin has rejected your request
            </p>
        </div>
        <div v-else-if="status === 'pending'">
            <P>
                Your Request is pending please check again after sometime
                <br>
                if you want to cancel your request click this button : <button @click="cancel_StoreManagerRequest()">Click
                    me</button>
            </P>
        </div>
        <div v-else>
            Congratulations Your a Storemanager now please logout first then login to see new Storemanager Dashboard
        </div>
    </div>
</template>
  
  
<script>
import axios from 'axios';

export default {
    data() {
        return {
            accessToken: localStorage.getItem('access_token'),
            role: localStorage.getItem('role'),
            requests: {},
            status: null,
            sm_requests: {}
        };
    },
    mounted() {
        this.fetchRequest()
    },
    methods: {

        fetchRequest() {
            if (this.role === 'admin') {
                axios.get(`http://127.0.0.1:5000/admin/get_storemanager_request`, {
                    headers: {
                        "Content-Type": "application/json",
                        'Authentication-Token': this.accessToken
                    }
                })
                    .then(response => {
                        console.log(response.data.sm_request);
                        this.sm_requests = response.data.sm_request
                    })
                    .catch(error => {
                        // Handle errors here
                        console.error('Error:', error);
                    });
                axios.get(`http://127.0.0.1:5000/category_requests`, {
                    headers: {
                        "Content-Type": "application/json",
                        'Authentication-Token': this.accessToken
                    }
                })
                    .then(response => {
                        console.log(response.data.sm_request);
                        this.requests = response.data
                    })
                    .catch(error => {
                        // Handle errors here
                        console.error('Error:', error);
                    });
            } else if (this.role === 'user') {
                axios.get(`http://127.0.0.1:5000/user_request_status`, {
                    headers: {
                        "Content-Type": "application/json",
                        'Authentication-Token': this.accessToken
                    }
                })
                    .then(response => {
                        console.log(response.data.status);
                        this.status = response.data.status
                    })
                    .catch(error => {
                        // Handle errors here
                        console.error('Error:', error);
                    });
            } else if (this.role === 'store manager') {
                axios.get(`http://127.0.0.1:5000/category_requests`, {
                    headers: {
                        "Content-Type": "application/json",
                        'Authentication-Token': this.accessToken
                    }
                })
                    .then(response => {
                        console.log(response.data.sm_request);
                        this.requests = response.data
                    })
                    .catch(error => {
                        // Handle errors here
                        console.error('Error:', error);
                    });
            }
        }
        ,

        reject_request(user_id) {
            axios.delete(`http://127.0.0.1:5000/admin/storemanager_request/${user_id}`, {
                headers: {
                    "Content-Type": "application/json",
                    'Authentication-Token': this.accessToken
                }
            })
                .then(response => {
                    console.log(response.data)
                    this.fetchRequest()

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
        accept_request(user_id) {
            axios.post(`http://127.0.0.1:5000/admin/storemanager_request/${user_id}`, null, {
                headers: {
                    "Content-Type": "application/json",
                    'Authentication-Token': this.accessToken
                }
            })
                .then(response => {
                    console.log(response.data)
                    this.fetchRequest()
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
        send_StoreManagerRequest() {
            axios.post(`http://127.0.0.1:5000/storemanager_request`, null, {
                headers: {
                    "Content-Type": "application/json",
                    'Authentication-Token': this.accessToken
                }
            })
                .then(response => {
                    console.log(response.data)
                    this.fetchRequest()
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
        cancel_StoreManagerRequest() {
            axios.delete(`http://127.0.0.1:5000/storemanager_request`, {
                headers: {
                    "Content-Type": "application/json",
                    'Authentication-Token': this.accessToken
                }
            })
                .then(response => {
                    console.log(response.data)
                    this.fetchRequest()
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
        accept_category_request(req_id) {
            console.log(req_id)
            axios.post(`http://127.0.0.1:5000/category_requests`, { id: req_id }, {
                headers: {
                    "Content-Type": "application/json",
                    'Authentication-Token': this.accessToken
                }
            })
                .then(response => {
                    alert(response.data.message)
                    this.fetchRequest()
                })
                .catch(error => {
                    // Handle errors here
                    console.error('Error:', error);
                });

        },
        reject_category_request(req_id) {
            console.log(req_id)
            axios.delete(`http://127.0.0.1:5000/category_requests`, {
                headers: {
                    "Content-Type": "application/json",
                    'Authentication-Token': this.accessToken
                },
                data: { id: req_id },
            })
                .then(response => {
                    alert(response.data.message)
                    this.fetchRequest()
                })
                .catch(error => {
                    // Handle errors here
                    console.error('Error:', error);
                });
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
    color: black;
    font-weight: bold;
    font-size: 16px;
}
</style>
  