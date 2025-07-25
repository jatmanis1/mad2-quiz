<template>
  <div class="container mt-4">
    <!-- Header -->
    <div class="row mb-4">
      <div class="col-12">
        <div class="d-flex justify-content-between align-items-center">
          <div>
            <h2>Available Quizzes</h2>
            <p class="text-muted">Choose a subject and chapter to start your quiz</p>
          </div>
          <div>
            <router-link to="/dashboard" class="btn btn-outline-primary">
              <i class="fas fa-arrow-left me-2"></i>Back to Dashboard
            </router-link>
          </div>
        </div>
      </div>
    </div>

    <!-- Subject Selection -->
    <div class="row mb-4">
      <div class="col-12">
        <div class="card">
          <div class="card-header">
            <h5>Select Subject</h5>
          </div>
          <div class="card-body">
            <div class="row">
              <div 
                v-for="subject in subjects" 
                :key="subject.id"
                class="col-md-4 mb-3"
              >
                <div 
                  class="card subject-card"
                  :class="{ 'selected': selectedSubject?.id === subject.id }"
                  @click="selectSubject(subject)"
                  style="cursor: pointer;"
                >
                  <div class="card-body text-center">
                    <i class="fas fa-book fa-2x mb-2 text-primary"></i>
                    <h6>{{ subject.name }}</h6>
                    <p class="text-muted small">{{ subject.description }}</p>
                    <span class="badge bg-info">{{ subject.chapters_count }} chapters</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Chapter Selection -->
    <div v-if="selectedSubject" class="row mb-4">
      <div class="col-12">
        <div class="card">
          <div class="card-header">
            <h5>Select Chapter - {{ selectedSubject.name }}</h5>
          </div>
          <div class="card-body">
            <div class="row">
              <div 
                v-for="chapter in chapters" 
                :key="chapter.id"
                class="col-md-6 mb-3"
              >
                <div 
                  class="card chapter-card"
                  :class="{ 'selected': selectedChapter?.id === chapter.id }"
                  @click="selectChapter(chapter)"
                  style="cursor: pointer;"
                >
                  <div class="card-body">
                    <div class="d-flex justify-content-between align-items-center">
                      <div>
                        <h6>{{ chapter.name }}</h6>
                        <p class="text-muted small mb-0">{{ chapter.description }}</p>
                      </div>
                      <span class="badge bg-success">{{ chapter.quizzes_count }} quizzes</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Quiz Selection -->
    <div v-if="selectedChapter" class="row">
      <div class="col-12">
        <div class="card">
          <div class="card-header">
            <h5>Available Quizzes - {{ selectedChapter.name }}</h5>
          </div>
          <div class="card-body">
            <div v-if="quizzes.length === 0" class="text-center text-muted py-4">
              <i class="fas fa-info-circle fa-2x mb-2"></i>
              <p>No quizzes available for this chapter yet.</p>
            </div>
            <div v-else class="row">
              <div 
                v-for="quiz in quizzes" 
                :key="quiz.id"
                class="col-md-6 mb-3"
              >
                <div class="card quiz-card h-100">
                  <div class="card-body">
                    <h6>{{ quiz.title }}</h6>
                    <p class="text-muted small">{{ quiz.description }}</p>
                    
                    <div class="quiz-info mb-3">
                      <div class="row">
                        <div class="col-6">
                          <small class="text-muted">
                            <i class="fas fa-clock me-1"></i>{{ quiz.time_duration }} minutes
                          </small>
                        </div>
                        <div class="col-6">
                          <small class="text-muted">
                            <i class="fas fa-question-circle me-1"></i>{{ quiz.questions_count }} questions
                          </small>
                        </div>
                      </div>
                      <div class="row mt-1">
                        <div class="col-6">
                          <small class="text-muted">
                            <i class="fas fa-star me-1"></i>{{ quiz.total_marks }} marks
                          </small>
                        </div>
                        <div class="col-6">
                          <small class="text-muted">
                            <i class="fas fa-calendar me-1"></i>{{ formatDate(quiz.date_of_quiz) }}
                          </small>
                        </div>
                      </div>
                    </div>
                    
                    <!-- Previous Attempt Info -->
                    <div v-if="getUserAttempt(quiz.id)" class="alert alert-info py-2">
                      <small>
                        <strong>Previous Attempt:</strong> 
                        {{ getUserAttempt(quiz.id).total_scored }}/{{ getUserAttempt(quiz.id).total_marks }}
                        ({{ getUserAttempt(quiz.id).percentage }}%)
                      </small>
                    </div>
                    
                    <div class="d-flex justify-content-between align-items-center">
                      <div>
                        <span 
                          class="badge"
                          :class="getQuizStatusBadge(quiz)"
                        >
                          {{ getQuizStatus(quiz) }}
                        </span>
                      </div>
                      <div>
                        <button 
                          @click="startQuiz(quiz)"
                          class="btn btn-primary btn-sm"
                          :disabled="!canStartQuiz(quiz)"
                        >
                          {{ getUserAttempt(quiz.id) ? 'Retake Quiz' : 'Start Quiz' }}
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'QuizList',
  data() {
    return {
      subjects: [],
      chapters: [],
      quizzes: [],
      userScores: [],
      selectedSubject: null,
      selectedChapter: null,
      loading: false
    }
  },
  async mounted() {
    await this.fetchSubjects()
    await this.fetchUserScores()
  },
  methods: {
    async fetchSubjects() {
      try {
        const response = await axios.get('/user/subjects')
        this.subjects = response.data
      } catch (error) {
        console.error('Failed to fetch subjects:', error)
      }
    },
    
    async fetchUserScores() {
      try {
        const response = await axios.get('/user/scores')
        this.userScores = response.data
      } catch (error) {
        console.error('Failed to fetch user scores:', error)
      }
    },
    
    async selectSubject(subject) {
      this.selectedSubject = subject
      this.selectedChapter = null
      this.quizzes = []
      
      try {
        const response = await axios.get(`/user/chapters`)
        this.chapters = response.data
      } catch (error) {
        console.error('Failed to fetch chapters:', error)
      }
    },
    
    async selectChapter(chapter) {
      this.selectedChapter = chapter
      
      try {
        const response = await axios.get(`/user/quizzes`)
        this.quizzes = response.data
      } catch (error) {
        console.error('Failed to fetch quizzes:', error)
      }
    },
    
    startQuiz(quiz) {
      if (this.canStartQuiz(quiz)) {
        this.$router.push(`/quiz/${quiz.id}/take`)
      }
    },
    
    canStartQuiz(quiz) {
      const now = new Date()
      const quizDate = new Date(quiz.date_of_quiz)
      return quizDate <= now && quiz.questions_count > 0
    },
    
    getQuizStatus(quiz) {
      const now = new Date()
      const quizDate = new Date(quiz.date_of_quiz)
      
      if (quizDate > now) return 'Upcoming'
      if (quiz.questions_count === 0) return 'No Questions'
      if (this.getUserAttempt(quiz.id)) return 'Completed'
      return 'Available'
    },
    
    getQuizStatusBadge(quiz) {
      const status = this.getQuizStatus(quiz)
      switch (status) {
        case 'Available': return 'bg-success'
        case 'Completed': return 'bg-info'
        case 'Upcoming': return 'bg-warning'
        case 'No Questions': return 'bg-secondary'
        default: return 'bg-secondary'
      }
    },
    
    getUserAttempt(quizId) {
      return this.userScores.find(score => score.quiz_id === quizId)
    },
    
    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString()
    }
  }
}
</script>

<style scoped>
.subject-card, .chapter-card, .quiz-card {
  transition: transform 0.2s, box-shadow 0.2s;
  border: 2px solid transparent;
}

.subject-card:hover, .chapter-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.subject-card.selected, .chapter-card.selected {
  border-color: #0d6efd;
  background-color: #f8f9ff;
}

.quiz-info {
  font-size: 0.875rem;
}

.quiz-card {
  border-left: 4px solid #0d6efd;
}
</style>
