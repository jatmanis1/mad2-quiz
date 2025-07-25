import { createStore } from 'vuex'
import axios from 'axios'

const API_BASE_URL = 'http://localhost:5000/api/'

// Configure axios defaults
axios.defaults.baseURL = API_BASE_URL

export default createStore({
    state: {
        user: null,
        token: localStorage.getItem('token') || null,
        subjects: [],
        quizzes: [],
        currentQuiz: null,
        scores: []
    },

    mutations: {
        SET_USER(state, user) {
            state.user = user
        },
        SET_TOKEN(state, token) {
            state.token = token
            if (token) {
                localStorage.setItem('token', token)
                axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
            } else {
                localStorage.removeItem('token')
                delete axios.defaults.headers.common['Authorization']
            }
        },
        SET_SUBJECTS(state, subjects) {
            state.subjects = subjects
        },
        SET_QUIZZES(state, quizzes) {
            state.quizzes = quizzes
        },
        SET_CURRENT_QUIZ(state, quiz) {
            state.currentQuiz = quiz
        },
        SET_SCORES(state, scores) {
            state.scores = scores
        },
        LOGOUT(state) {
            state.user = null
            state.token = null
            localStorage.removeItem('token')
            delete axios.defaults.headers.common['Authorization']
        }
    },

    actions: {
        async login({ commit }, credentials) {
            try {
                const response = await axios.post('/auth/login', credentials)
                const { access_token, user } = response.data

                commit('SET_TOKEN', access_token)
                commit('SET_USER', user)

                return { success: true, user }
            } catch (error) {
                return {
                    success: false,
                    message: error.response?.data?.message || 'Login failed'
                }
            }
        },

        async register({ commit }, userData) {
            try {
                await axios.post('/auth/register', userData)
                return { success: true, message: 'Registration successful' }
            } catch (error) {
                return {
                    success: false,
                    message: error.response?.data?.message || 'Registration failed'
                }
            }
        },

        async fetchSubjects({ commit }) {
            try {
                const response = await axios.get('/admin/subjects')
                commit('SET_SUBJECTS', response.data)
                return { success: true }
            } catch (error) {
                return { success: false, message: 'Failed to fetch subjects' }
            }
        },

        async createSubject({ dispatch }, subjectData) {
            try {
                await axios.post('/admin/subjects', subjectData)
                dispatch('fetchSubjects')
                return { success: true, message: 'Subject created successfully' }
            } catch (error) {
                return {
                    success: false,
                    message: error.response?.data?.message || 'Failed to create subject'
                }
            }
        },

        async fetchQuizzes({ commit }, chapterId) {
            try {
                const response = await axios.get(`/user/chapters/${chapterId}/quizzes`)
                commit('SET_QUIZZES', response.data)
                return { success: true }
            } catch (error) {
                return { success: false, message: 'Failed to fetch quizzes' }
            }
        },

        async startQuiz({ commit }, quizId) {
            try {
                const response = await axios.get(`/quiz/${quizId}/start`)
                commit('SET_CURRENT_QUIZ', response.data)
                return { success: true, quiz: response.data }
            } catch (error) {
                return { success: false, message: 'Failed to start quiz' }
            }
        },

        async submitQuiz({ dispatch }, { quizId, answers, timeTaken }) {
            try {
                const response = await axios.post(`/quiz/${quizId}/submit`, {
                    answers,
                    time_taken: timeTaken
                })
                return { success: true, result: response.data }
            } catch (error) {
                return { success: false, message: 'Failed to submit quiz' }
            }
        },

        logout({ commit }) {
            commit('LOGOUT')
        }
    },

    getters: {
        isAuthenticated: state => !!state.token,
        userRole: state => state.user?.role,
        isAdmin: state => state.user?.role === 'admin',
        isUser: state => state.user?.role === 'user'
    }
})
