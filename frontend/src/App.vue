<!-- src/App.vue -->
<template>
  <div id="app">
    <router-view /> <!-- 👈 This renders Login.vue (or other routed components) -->
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>
