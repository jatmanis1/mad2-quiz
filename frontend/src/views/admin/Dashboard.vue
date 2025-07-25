<template>
  <div class="admin-dashboard">
    <div class="header">
      <h1>Admin Dashboard</h1>
    </div>

    <!-- Summary Cards -->
    <div class="stats-grid">
      <div class="stat-card">
        <h3>{{ stats.total_users }}</h3>
        <p>Total Users</p>
      </div>
      <div class="stat-card">
        <h3>{{ stats.total_subjects }}</h3>
        <p>Total Subjects</p>
      </div>
      <div class="stat-card">
        <h3>{{ stats.total_quizzes }}</h3>
        <p>Total Quizzes</p>
      </div>
      <div class="stat-card">
        <h3>{{ stats.total_attempts }}</h3>
        <p>Quiz Attempts</p>
      </div>
    </div>

    <!-- Navigation Cards -->
    <div class="navigation-grid">
      <router-link to="/admin/subjects" class="nav-card">
        <h3>Manage Subjects</h3>
        <p>Create, edit, and delete subjects</p>
      </router-link>
      <router-link to="/admin/chapters" class="nav-card">
        <h3>Manage Chapters</h3>
        <p>Create, edit, and delete chapters</p>
      </router-link>
      <router-link to="/admin/quizzes" class="nav-card">
        <h3>Manage Quizzes</h3>
        <p>Create, edit, and delete quizzes</p>
      </router-link>
    </div>

    <!-- Recent Quiz Attempts -->
    <div class="recent-attempts">
      <h2>Recent Quiz Attempts</h2>
      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th>User</th>
              <th>Quiz</th>
              <th>Score</th>
              <th>Date</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="score in stats.recent_scores" :key="score.id">
              <td>{{ score.user_name }}</td>
              <td>{{ score.quiz_title }}</td>
              <td>{{ score.score }}/{{ score.total_marks }}</td>
              <td>{{ formatDate(score.timestamp_of_attempt) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'AdminDashboard',
  data() {
    return {
      stats: {
        total_users: 0,
        total_subjects: 0,
        total_quizzes: 0,
        total_attempts: 0,
        recent_scores: []
      }
    }
  },
  async mounted() {
    await this.fetchStats()
  },
  methods: {
    async fetchStats() {
      try {
        const response = await axios.get('/admin/dashboard/stats')
        this.stats = response.data
      } catch (error) {
        console.error('Error fetching stats:', error)
      }
    },
    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString()
    }
  }
}
</script>

<style scoped>
.admin-dashboard {
  padding: 20px;
}

.header {
  margin-bottom: 30px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  text-align: center;
}

.stat-card h3 {
  font-size: 2rem;
  color: #007bff;
  margin: 0;
}

.navigation-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.nav-card {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  text-decoration: none;
  color: inherit;
  transition: transform 0.2s;
}

.nav-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.15);
}

.recent-attempts {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.table-container {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 15px;
}

th, td {
  padding: 10px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

th {
  background-color: #f8f9fa;
  font-weight: 600;
}
</style>
