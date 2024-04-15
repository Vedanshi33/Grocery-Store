<template>
<div class="d-flex justify-content-center align-items-center vh-100">
  <div class="card square-card">
    <div class="card-body">
      <h2 class="card-title text-center">Register</h2>
      <form @submit.prevent="registerUser">
        <div class="form-group">
          <label>First Name:</label>
          <input v-model="formData.first_name" type="text" class="form-control" required>
        </div>

        <div class="form-group">
          <label>Last Name:</label>
          <input v-model="formData.last_name" type="text" class="form-control" required>
        </div>

        <div class="form-group">
          <label>Email:</label>
          <input v-model="formData.email" type="email" class="form-control" required>
        </div>

        <div class="form-group">
          <label>Password:</label>
          <input v-model="formData.password" type="password" class="form-control" required>
        </div>

        <div class="form-group text-center">
          <button type="submit" class="btn btn-primary btn-lg btn-block">Register</button>
        </div>
      </form>
      
      <p class="text-center">Already have an account? <router-link to="/User_login">Login Here</router-link></p>
    </div>
  </div>
</div>
</template>

<script>
export default {
data() {
  return {
    formData: {
      first_name: '',
      last_name: '',
      email: '',
      password: ''
    }
  };
},
methods: {
  async registerUser() {
    try {
     
      const response = await fetch('http://127.0.0.1:5000/user_register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(this.formData)
      });

      if (response.ok) {
      
        console.log('User registered successfully');
        this.$router.push({ name: 'User_login' });
       
      } else {
       
        console.error('Registration failed');
      }
    } catch (error) {
      console.error('Error registering user:', error);
    }
  }
}
};
</script>