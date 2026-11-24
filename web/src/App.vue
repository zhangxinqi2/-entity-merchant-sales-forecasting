<template>
  <div class="min-h-screen bg-gray-100 flex">
    <!-- 侧边栏 -->
    <Sidebar />
    
    <!-- 主内容区 -->
    <main class="flex-1 ml-64">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import Sidebar from '@/components/Sidebar.vue'
</script>
