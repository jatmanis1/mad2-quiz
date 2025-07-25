<template>
  <div class="container mt-4">
    <!-- Loading Spinner -->
    <div v-if="loading" class="text-center">
      <div class="spinner-border" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p>Loading quiz...</p>
    </div>

    <!-- Quiz Interface -->
    <div v-else-if="quiz" class="row">
      <div class="col-md-8">
        <div class="card">
          <div class="card-header d-flex justify-content-between align-items-center">
            <h4>{{ quiz.quiz.title }}</h4>
            <div class="timer">
              <span class="badge bg-warning fs-6">
                Time Remaining: {{ formatTime(timeRemaining) }}
              </span>
            </div>
          </div>
          <div class="card-body">
            <div class="progress mb-3">
              <div 
                class="progress-bar" 
                :style="{ width: progressPercentage + '%' }"
                role="progressbar"
              >
                Question {{ currentQuestionIndex + 1 }} of {{ quiz.questions.length }}
              </div>
            </div>

            <div v-if="currentQuestion" class="question-container">
              <h5 class="mb-3">{{ currentQuestion.question_statement }}</h5>
              <div class="options">
                <div 
                  v-for="(option, index) in getOptions(currentQuestion)" 
                  :key="index"
                  class="form-check mb-2"
                >
                  <input 
                    class="form-check-input" 
                    type="radio" 
                    :name="`question_${currentQuestion.id}`"
                    :id="`option_${currentQuestion.id}_${index + 1}`"
                    :value="index + 1"
                    v-model="answers[currentQuestion.id]"
                  >
                  <label 
                    class="form-check-label" 
                    :for="`option_${currentQuestion.id}_${index + 1}`"
                  >
                    {{ option }}
                  </label>
                </div>
              </div>
            </div>

            <div class="navigation-buttons mt-4">
              <button 
                @click="previousQuestion" 
                class="btn btn-outline-secondary me-2"
                :disabled="currentQuestionIndex === 0"
              >
                Previous
              </button>
              <button 
                @click="nextQuestion" 
                class="btn btn-primary me-2"
                v-if="currentQuestionIndex < quiz.questions.length - 1"
              >
                Next
              </button>
              <button 
                @click="submitQuiz" 
                class="btn btn-success"
                v-if="currentQuestionIndex === quiz.questions.length - 1"
              >
                Submit Quiz
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Question Navigator -->
      <div class="col-md-4">
        <div class="card">
          <div class="card-header">
            <h5>Question Navigator</h5>
          </div>
          <div class="card-body">
            <div class="question-grid">
              <button
                v-for="(question, index) in quiz.questions"
                :key="question.id"
                @click="goToQuestion(index)"
                class="btn btn-sm me-1 mb-1"
                :class="getQuestionButtonClass(index, question.id)"
              >
                {{ index + 1 }}
              </button>
            </div>
            <div class="legend mt-3">
              <small>
                <span class="badge bg-success me-1">●</span> Answered<br>
                <span class="badge bg-primary me-1">●</span> Current<br>
                <span class="badge bg-light text-dark me-1">●</span> Not Answered
              </small>
            </div>
            <button @click="submitQuiz" class="btn btn-warning w-100 mt-3">
              Submit Quiz
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Custom Confirmation Modal -->
    <div v-if="showConfirmDialog" class="custom-modal-overlay">
      <div class="custom-modal">
        <div class="modal-header">
          <h5 class="modal-title">Submit Quiz</h5>
        </div>
        <div class="modal-body">
          <p>Are you sure you want to submit your quiz?</p>
          <p><strong>Answered:</strong> {{ answeredCount }}/{{ quiz?.questions.length }}</p>
          <p><strong>Time Remaining:</strong> {{ formatTime(timeRemaining) }}</p>
          <p class="text-warning"><small>You cannot change your answers after submission.</small></p>
          <div v-if="submitError" class="alert alert-danger mt-2">
            {{ submitError }}
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn btn-secondary" @click="showConfirmDialog = false" :disabled="submitting">
            Cancel
          </button>
          <button class="btn btn-success" @click="confirmSubmit" :disabled="submitting">
            {{ submitting ? 'Submitting...' : 'Submit Quiz' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'TakeQuiz',
  data() {
    return {
      quiz: null,
      loading: true,
      currentQuestionIndex: 0,
      answers: {},
      startTime: null,
      timeRemaining: 0,
      timer: null,
      submitting: false,
      submitError: null,
      showConfirmDialog: false
    }
  },
  computed: {
    currentQuestion() {
      return this.quiz?.questions[this.currentQuestionIndex]
    },
    progressPercentage() {
      if (!this.quiz) return 0
      return ((this.currentQuestionIndex + 1) / this.quiz.questions.length) * 100
    },
    answeredCount() {
      return Object.keys(this.answers).length
    }
  },
  async mounted() {
    await this.loadQuiz()
  },
  beforeUnmount() {
    if (this.timer) {
      clearInterval(this.timer)
    }
  },
  methods: {
    async loadQuiz() {
      const quizId = this.$route.params.quizId
      try {
        const response = await axios.get(`/quiz/${quizId}/start`)
        this.quiz = response.data
        this.startTime = new Date(response.data.start_time)
        this.timeRemaining = this.quiz.quiz.time_duration * 60
        this.startTimer()
        this.loading = false
      } catch (error) {
        console.error('Failed to load quiz:', error)
        this.$router.push('/quizzes')
      }
    },
    startTimer() {
      this.timer = setInterval(() => {
        this.timeRemaining--
        if (this.timeRemaining <= 0) {
          this.timeUp()
        }
      }, 1000)
    },
    timeUp() {
      alert('Time is up! Your quiz will be auto-submitted.')
      this.submitError = null
      this.confirmSubmit()
    },
    formatTime(seconds) {
      const minutes = Math.floor(seconds / 60)
      const secs = seconds % 60
      return `${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
    },
    getOptions(question) {
      return [question.option1, question.option2, question.option3, question.option4]
    },
    getQuestionButtonClass(index, questionId) {
      if (index === this.currentQuestionIndex) return 'btn-primary'
      else if (this.answers[questionId]) return 'btn-success'
      else return 'btn-light'
    },
    previousQuestion() {
      if (this.currentQuestionIndex > 0) this.currentQuestionIndex--
    },
    nextQuestion() {
      if (this.currentQuestionIndex < this.quiz.questions.length - 1) this.currentQuestionIndex++
    },
    goToQuestion(index) {
      this.currentQuestionIndex = index
    },
    submitQuiz() {
      this.submitError = null
      this.showConfirmDialog = true
    },
    async confirmSubmit() {
      this.submitting = true
      this.submitError = null
      this.showConfirmDialog = false

      if (!this.quiz || !this.quiz.quiz) {
        this.submitError = 'Quiz data is not available.'
        this.submitting = false
        return
      }

      const timeTaken = this.quiz.quiz.time_duration - Math.floor(this.timeRemaining / 60)

      try {
        const response = await axios.post(`/quiz/${this.quiz.quiz.id}/submit`, {
          answers: this.answers,
          timeTaken: timeTaken        
        })
        console.log('Quiz submitted successfully:', response.data)
        this.submitting = false
        this.$router.push(`/quiz/results/${response.data.score.id}`)

        if (response.data && response.data.success) {
          clearInterval(this.timer)
          this.$router.push(`/quiz/results/${response.data.result.score.id}`)
        } else {
          this.submitError = response.data.message || 'Unknown error, please try again.'
        }
      } catch (error) {
        this.submitError = error?.response?.data?.message || error.message || 'Failed to submit quiz.'
      } finally {
        this.submitting = false
      }
    }
  }
}
</script>

<style scoped>
.question-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 5px;
}

.timer {
  font-size: 1.1em;
  font-weight: bold;
}

.options .form-check {
  padding: 10px;
  border: 1px solid #dee2e6;
  border-radius: 5px;
  transition: background-color 0.2s;
}

.options .form-check:hover {
  background-color: #f8f9fa;
}

.options .form-check-input:checked + .form-check-label {
  font-weight: bold;
  color: #0d6efd;
}

.custom-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1050;
}

.custom-modal {
  background-color: #fff;
  border-radius: 8px;
  width: 90%;
  max-width: 500px;
  box-shadow: 0 5px 15px rgba(0,0,0,0.3);
  padding: 20px;
}
</style>
