<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card">
          <div class="card-header">
            <h3 class="text-center">Register for Quiz Master</h3>
          </div>
          <div class="card-body">
            <form @submit.prevent="handleRegister">
              <div class="mb-3">
                <label for="username" class="form-label">Email Address</label>
                <input 
                  type="email" 
                  class="form-control" 
                  id="username"
                  v-model="formData.username"
                  required
                >
              </div>
              <div class="mb-3">
                <label for="fullName" class="form-label">Full Name</label>
                <input 
                  type="text" 
                  class="form-control" 
                  id="fullName"
                  v-model="formData.full_name"
                  required
                >
              </div>
              <div class="mb-3">
                <label for="qualification" class="form-label">Qualification</label>
                <input 
                  type="text" 
                  class="form-control" 
                  id="qualification"
                  v-model="formData.qualification"
                  placeholder="e.g., B.Tech, M.Sc, etc."
                >
              </div>
              <div class="mb-3">
                <label for="dob" class="form-label">Date of Birth</label>
                <input 
                  type="date" 
                  class="form-control" 
                  id="dob"
                  v-model="formData.dob"
                >
              </div>
              <div class="mb-3">
                <label for="password" class="form-label">Password</label>
                <input 
                  type="password" 
                  class="form-control" 
                  id="password"
                  v-model="formData.password"
                  required
                  minlength="6"
                >
              </div>
              <div class="mb-3">
                <label for="confirmPassword" class="form-label">Confirm Password</label>
                <input 
                  type="password" 
                  class="form-control" 
                  id="confirmPassword"
                  v-model="confirmPassword"
                  required
                >
              </div>
              <div class="d-grid">
                <button type="submit" class="btn btn-primary" :disabled="loading">
                  {{ loading ? 'Registering...' : 'Register' }}
                </button>
              </div>
            </form>
            <div class="text-center mt-3">
              <router-link to="/login">Already have an account? Login</router-link>
            </div>
            <div v-if="error" class="alert alert-danger mt-3">
              {{ error }}
            </div>
            <div v-if="success" class="alert alert-success mt-3">
              {{ success }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Register',
  data() {
    return {
      formData: {
        username: '',
        full_name: '',
        qualification: '',
        dob: '',
        password: ''
      },
      confirmPassword: '',
      loading: false,
      error: null,
      success: null
    }
  },
  methods: {
    async handleRegister() {
      this.error = null
      this.success = null
      
      // Validate passwords match
      if (this.formData.password !== this.confirmPassword) {
        this.error = 'Passwords do not match'
        return
      }
      
      this.loading = true
      
      const result = await this.$store.dispatch('register', this.formData)
      
      if (result.success) {
        this.success = 'Registration successful! You can now login.'
        setTimeout(() => {
          this.$router.push('/login')
        }, 2000)
      } else {
        this.error = result.message
      }
      
      this.loading = false
    }
  }
}
</script>
