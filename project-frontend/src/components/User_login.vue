<template>
  <div class="d-flex justify-content-center align-items-center vh-100">
    <div class="card" style="max-width: 500px; margin: 0 auto;">

      <div class="card-body">
        <h2 class="card-title text-center">Login</h2>
        <form @submit.prevent="loginUser">
          <div class="form-group">
            <label>Email:</label>
            <input v-model="formData.email" type="email" class="form-control" required>
          </div>

          <div class="form-group">
            <label>Password:</label>
            <input v-model="formData.password" type="password" class="form-control" required>
          </div>

          <div class="form-group text-center">
            <button type="submit" class="btn btn-primary btn-lg btn-block" :disabled="isLoading">Login</button>
          </div>

          <div class="error-message" v-if="error">{{ error }}</div>

        </form>

        <p class="text-center">Don't have an account? <router-link to="/User_register">Create Account</router-link></p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      formData: {
        email: '',
        password: ''
      },
      isLoading: false,
      error: null
    };
  },
  methods: {
    async loginUser() {
      this.isLoading = true;
      this.error = null; // Clear previous error messages
      console.log(JSON.stringify(this.formData))

      try {
        const response = await fetch('http://127.0.0.1:5000/user_login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(this.formData)
        });
        if (response.ok) {
          const data = await response.json();
          console.log(data)
          if (data.message === "Login successful") {
            const access_token = data.access_token;
            const role = data.role;
            localStorage.setItem("access_token", access_token);
            localStorage.setItem("role", role);
            alert("Successfully Logged in !!");
            if(role === 'admin'){
              this.$router.push("/admin_dashboard");
            }else if(role === 'store manager'){
              this.$router.push("/sm_dashboard");
            }else{this.$router.push("/user_dashboard");}
            
          } else {
            alert("Invalid credentials !!");
          }
        } else {
          alert("An error occurred while logging in !!");
        }
      } catch (error) {
        console.error(error);
        alert("An error occurred while logging in !!");
      } finally {
        this.isLoading = false;
      }
    }
  }
};
</script>

<style scoped>

.error-message {
  color: red;
  margin-top: 10px;
}
</style>
