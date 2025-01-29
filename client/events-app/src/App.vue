<script setup>
import Calendar from './components/Calendar.vue'
import Events from './components/Events.vue'
</script>

<template>
  <div id="app" class="top-level">
    <Calendar />
    <Events/>
  </div>
</template>

<style scoped>
.top-level {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
</style>
