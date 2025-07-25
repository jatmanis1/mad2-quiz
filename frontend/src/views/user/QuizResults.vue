<template>
  <div class="container mt-4">
    <div v-if="loading" class="text-center">
      <div class="spinner-border" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p>Loading results...</p>
    </div>
    
    <div v-else-if="results" class="row">
      <!-- Results Header -->
      <div class="col-12 mb-4">
        <div class="card">
          <div class="card-header bg-primary text-white">
            <h3 class="mb-0">Quiz Results</h3>
          </div>
          <div class="card-body">
            <div class="row">
              <div class="col-md-8">
                <h4>{{ results.quiz.title }}</h4>
                <p class="text-muted">{{ results.quiz.description }}</p>
                <p class="mb-0">
                  <strong>Subject:</strong> {{ results.quiz.subject_name }} | 
                  <strong>Chapter:</strong> {{ results.quiz.chapter_name }}
                </p>
              </div>
              <div class="col-md-4 text-end">
                <div class="score-display">
                  <div class="score-circle" :class="getScoreClass(results.score.percentage)">
                    <div class="score-text">
                      <div class="score-number">{{ results.score.percentage }}%</div>
                      <div class="score-fraction">{{ results.score.total_scored }}/{{ results.score.total_marks }}</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Performance Summary -->
      <div class="col-md-4 mb-4">
        <div class="card h-100">
          <div class="card-header">
            <h5>Performance Summary</h5>
          </div>
          <div class="card-body">
            <div class="mb-3">
              <div class="d-flex justify-content-between">
                <span>Total Questions:</span>
                <strong>{{ results.detailed_results.length }}</strong>
              </div>
            </div>
            <div class="mb-3">
              <div class="d-flex justify-content-between">
                <span>Correct Answers:</span>
                <strong class="text-success">{{ correctAnswers }}</strong>
              </div>
            </div>
            <div class="mb-3">
              <div class="d-flex justify-content-between">
                <span>Wrong Answers:</span>
                <strong class="text-danger">{{ wrongAnswers }}</strong>
              </div>
            </div>
            <div class="mb-3">
              <div class="d-flex justify-content-between">
                <span>Unanswered:</span>
                <strong class="text-warning">{{ unanswered }}</strong>
              </div>
            </div>
            <div class="mb-3">
              <div class="d-flex justify-content-between">
                <span>Time Taken:</span>
                <strong>{{ results.score.time_taken || 'N/A' }} min</strong>
              </div>
            </div>
            <div class="mb-3">
              <div class="d-flex justify-content-between">
                <span>Attempt Date:</span>
                <strong>{{ formatDate(results.score.timestamp_of_attempt) }}</strong>
              </div>
            </div>
            
            <div class="mt-4">
              <div class="progress" style="height: 20px;">
                <div 
                  class="progress-bar" 
                  :class="getProgressBarClass(results.score.percentage)"
                  :style="{ width: results.score.percentage + '%' }"
                >
                  {{ results.score.percentage }}%
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Actions -->
      <div class="col-md-8 mb-4">
        <div class="card h-100">
          <div class="card-header">
            <h5>Actions</h5>
          </div>
          <div class="card-body d-flex flex-column">
            <div class="mb-3">
              <button @click="retakeQuiz" class="btn btn-primary me-2">
                <i class="fas fa-redo me-2"></i>Retake Quiz
              </button>
              <router-link to="/quizzes" class="btn btn-outline-primary me-2">
                <i class="fas fa-list me-2"></i>Browse More Quizzes
              </router-link>
              <router-link to="/dashboard" class="btn btn-outline-secondary">
                <i class="fas fa-home me-2"></i>Back to Dashboard
              </router-link>
            </div>
            
            <div class="mt-auto">
              <div class="alert alert-info">
                <h6>Performance Analysis</h6>
                <p class="mb-0">{{ getPerformanceMessage(results.score.percentage) }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Detailed Results -->
      <div class="col-12">
        <div class="card">
          <div class="card-header d-flex justify-content-between align-items-center">
            <h5>Detailed Results</h5>
            <button 
              @click="showAnswers = !showAnswers" 
              class="btn btn-outline-primary btn-sm"
            >
              {{ showAnswers ? 'Hide' : 'Show' }} Answers
            </button>
          </div>
          <div class="card-body" v-if="showAnswers">
            <div class="accordion" id="questionsAccordion">
              <div 
                v-for="(result, index) in results.detailed_results" 
                :key="result.question.id"
                class="accordion-item"
              >
                <h2 class="accordion-header">
                  <button 
                    class="accordion-button collapsed"
                    type="button" 
                    data-bs-toggle="collapse" 
                    :data-bs-target="`#question${index}`"
                  >
                    <div class="d-flex justify-content-between w-100 me-3">
                      <span>Question {{ index + 1 }}</span>
                      <span>
                        <i 
                          class="fas"
                          :class="result.is_correct ? 'fa-check text-success' : 'fa-times text-danger'"
                        ></i>
                        {{ result.question.marks }} mark{{ result.question.marks > 1 ? 's' : '' }}
                      </span>
                    </div>
                  </button>
                </h2>
                <div 
                  :id="`question${index}`"
                  class="accordion-collapse collapse"
                  data-bs-parent="#questionsAccordion"
                >
                  <div class="accordion-body">
                    <div class="question-content">
                      <h6>{{ result.question.question_statement }}</h6>
                      
                      <div class="options mt-3">
                        <div 
                          v-for="(option, optionIndex) in getOptions(result.question)"
                          :key="optionIndex"
                          class="option-item"
                          :class="getOptionClass(optionIndex + 1, result)"
                        >
                          <div class="d-flex justify-content-between align-items-center">
                            <span>{{ String.fromCharCode(65 + optionIndex) }}. {{ option }}</span>
                            <div>
                              <span v-if="result.user_answer == optionIndex + 1" class="badge bg-primary me-1">
                                Your Answer
                              </span>
                              <span v-if="result.question.correct_option == optionIndex + 1" class="badge bg-success">
                                Correct
                              </span>
                            </div>
                          </div>
                        </div>
                      </div>
                      
                      <div class="result-info mt-3">
                        <div class="row">
                          <div class="col-md-6">
                            <small class="text-muted">
                              <strong>Your Answer:</strong> 
                              {{ result.user_answer ? String.fromCharCode(64 + parseInt(result.user_answer)) : 'Not answered' }}
                            </small>
                          </div>
                          <div class="col-md-6">
                            <small class="text-muted">
                              <strong>Correct Answer:</strong> 
                              {{ String.fromCharCode(64 + result.question.correct_option) }}
                            </small>
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
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'QuizResults',
  data() {
    return {
      results: null,
      loading: true,
      showAnswers: false
    }
  },
  computed: {
    correctAnswers() {
      return this.results?.detailed_results.filter(r => r.is_correct).length || 0
    },
    wrongAnswers() {
      return this.results?.detailed_results.filter(r => !r.is_correct && r.user_answer).length || 0
    },
    unanswered() {
      return this.results?.detailed_results.filter(r => !r.user_answer).length || 0
    }
  },
  async mounted() {
    await this.fetchResults()
  },
  methods: {
    async fetchResults() {
      const quizId = this.$route.params.quizId
      const scoreId = this.$route.params.scoreId
      
      try {
        const response = await axios.get(`/quiz/results/${scoreId}`)
        this.results = response.data
      } catch (error) {
        console.error('Failed to fetch results:', error)
        this.$router.push('/dashboard')
      }
      
      this.loading = false
    },
    
    getScoreClass(percentage) {
      if (percentage >= 80) return 'score-excellent'
      if (percentage >= 60) return 'score-good'
      if (percentage >= 40) return 'score-average'
      return 'score-poor'
    },
    
    getProgressBarClass(percentage) {
      if (percentage >= 80) return 'bg-success'
      if (percentage >= 60) return 'bg-info'
      if (percentage >= 40) return 'bg-warning'
      return 'bg-danger'
    },
    
    getOptions(question) {
      return [question.option1, question.option2, question.option3, question.option4]
    },
    
    getOptionClass(optionNumber, result) {
      const classes = ['p-2', 'mb-1', 'rounded']
      
      if (result.user_answer == optionNumber && result.question.correct_option == optionNumber) {
        classes.push('bg-success', 'text-white') // Correct answer chosen
      } else if (result.user_answer == optionNumber) {
        classes.push('bg-danger', 'text-white') // Wrong answer chosen
      } else if (result.question.correct_option == optionNumber) {
        classes.push('bg-light', 'border', 'border-success') // Correct answer not chosen
      } else {
        classes.push('bg-light') // Other options
      }
      
      return classes.join(' ')
    },
    
    getPerformanceMessage(percentage) {
      if (percentage >= 90) return "Excellent! You have a strong understanding of the topic."
      if (percentage >= 80) return "Great job! You performed very well on this quiz."
      if (percentage >= 70) return "Good work! You have a solid grasp of the material."
      if (percentage >= 60) return "Fair performance. Consider reviewing the topics you missed."
      if (percentage >= 40) return "You may want to study this topic more thoroughly before retaking."
      return "Consider reviewing the study materials and retaking this quiz to improve your understanding."
    },
    
    formatDate(dateString) {
      return new Date(dateString).toLocaleString()
    },
    
    retakeQuiz() {
      this.$router.push(`/quiz/${this.results.quiz.id}/take`)
    }
  }
}
</script>

<style scoped>
.score-circle {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
  border: 4px solid;
}

.score-excellent {
  background-color: #d4edda;
  border-color: #28a745;
  color: #155724;
}

.score-good {
  background-color: #d1ecf1;
  border-color: #17a2b8;
  color: #0c5460;
}

.score-average {
  background-color: #fff3cd;
  border-color: #ffc107;
  color: #856404;
}

.score-poor {
  background-color: #f8d7da;
  border-color: #dc3545;
  color: #721c24;
}

.score-text {
  text-align: center;
}

.score-number {
  font-size: 24px;
  font-weight: bold;
}

.score-fraction {
  font-size: 14px;
}

.option-item {
  border: 1px solid #dee2e6;
}

.question-content h6 {
  color: #333;
  font-weight: 600;
}
</style>
