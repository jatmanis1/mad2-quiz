<template>
  <div class="container mt-4">
    <div class="row">
      <div class="col-12">
        <h2>Welcome, {{ user?.full_name }}!</h2>
        <p class="text-muted">Your Quiz Dashboard</p>
      </div>
    </div>
    
    <!-- Statistics Cards -->
    <div class="row mb-4">
      <div class="col-md-3">
        <div class="card bg-primary text-white">
          <div class="card-body">
            <h5>Total Attempts</h5>
            <h2>{{ dashboardData.total_attempts }}</h2>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card bg-success text-white">
          <div class="card-body">
            <h5>Average Score</h5>
            <h2>{{ dashboardData.average_score }}%</h2>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card bg-info text-white">
          <div class="card-body">
            <h5>Available Quizzes</h5>
            <h2>{{ dashboardData.available_quizzes }}</h2>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card bg-warning text-white">
          <div class="card-body">
            <h5>This Month</h5>
            <h2>{{ monthlyAttempts }}</h2>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Recent Attempts -->
    <div class="row">
      <div class="col-md-8">
        <div class="card">
          <div class="card-header">
            <h5>Recent Quiz Attempts</h5>
          </div>
          <div class="card-body">
            <div v-if="dashboardData.recent_attempts.length === 0" class="text-center text-muted">
              No quiz attempts yet. <router-link to="/quizzes">Start your first quiz!</router-link>
            </div>
            <div v-else>
              <table class="table">
                <thead>
                  <tr>
                    <th>Quiz</th>
                    <th>Score</th>
                    <th>Date</th>
                    <th>Action</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="attempt in dashboardData.recent_attempts" :key="attempt.id">
                    <td>{{ attempt.quiz_title }}</td>
                    <td>
                      <span class="badge" :class="getScoreBadgeClass(attempt.percentage)">
                        {{ attempt.total_scored }}/{{ attempt.total_marks }} ({{ attempt.percentage }}%)
                      </span>
                    </td>
                    <td>{{ formatDate(attempt.timestamp_of_attempt) }}</td>
                    <td>
                      <router-link 
                        :to="`/quiz/results/${attempt.id}`"
                        class="btn btn-sm btn-outline-primary"
                      >
                        View Results
                      </router-link>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Quick Actions -->
      <div class="col-md-4">
        <div class="card">
          <div class="card-header">
            <h5>Quick Actions</h5>
          </div>
          <div class="card-body">
            <div class="d-grid gap-2">
              <router-link to="/quizzes" class="btn btn-primary">
                Browse Quizzes
              </router-link>
              <button @click="exportData" class="btn btn-outline-secondary">
                Export My Data
              </button>
              <button @click="showProfile = !showProfile" class="btn btn-outline-info">
                {{ showProfile ? 'Hide' : 'Show' }} Profile
              </button>
            </div>
          </div>
        </div>
        
        <!-- Profile Card -->
        <div v-if="showProfile" class="card mt-3">
          <div class="card-header">
            <h5>Profile Information</h5>
          </div>
          <div class="card-body">
            <p><strong>Email:</strong> {{ user.username }}</p>
            <p><strong>Full Name:</strong> {{ user.full_name }}</p>
            <p><strong>Qualification:</strong> {{ user.qualification || 'Not specified' }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'UserDashboard',
  data() {
    return {
      dashboardData: {
        total_attempts: 0,
        average_score: 0,
        recent_attempts: [],
        available_quizzes: 0
      },
      showProfile: false
    }
  },
  computed: {
    user() {
      return this.$store.state.user
    },
    monthlyAttempts() {
      const currentMonth = new Date().getMonth()
      return this.dashboardData.recent_attempts.filter(attempt => {
        const attemptDate = new Date(attempt.timestamp_of_attempt)
        return attemptDate.getMonth() === currentMonth
      }).length
    }
  },
  async mounted() {
    await this.fetchDashboardData()
  },
  methods: {
    async fetchDashboardData() {
      try {
        const response = await axios.get('/user/dashboard')
        this.dashboardData = response.data
      } catch (error) {
        console.error('Failed to fetch dashboard data:', error)
      }
    },
    getScoreBadgeClass(percentage) {
      if (percentage >= 80) return 'bg-success'
      if (percentage >= 60) return 'bg-warning'
      return 'bg-danger'
    },
    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString()
    },
    async exportData() {
      try {
        // Trigger CSV export job
        await axios.post('/user/export-data')
        alert('Export job started! You will receive an email when ready.')
      } catch (error) {
        console.error('Export failed:', error)
        alert('Export failed. Please try again.')
      }
    }
  }
}
</script>
