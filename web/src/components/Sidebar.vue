<template>
  <aside class="sidebar bg-gray-800 text-white w-64 min-h-screen flex flex-col">
    <!-- Logo -->
    <div class="p-4 border-b border-gray-700">
      <h1 class="text-lg font-bold text-primary">销量预测系统</h1>
    </div>

    <!-- 导航菜单 -->
    <nav class="flex-1 p-4">
      <ul class="space-y-2">
        <li>
          <button
            @click="toggleSection('data-analysis')"
            class="w-full flex items-center gap-3 px-3 py-2 rounded-lg transition-colors"
            :class="expandedSection === 'data-analysis' ? 'bg-gray-700 text-white' : 'hover:bg-gray-700 text-gray-300'"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
            <span>数据解构</span>
            <svg v-if="expandedSection !== 'data-analysis'" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 ml-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
            <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 ml-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
            </svg>
          </button>
          <!-- 子菜单 -->
          <ul v-if="expandedSection === 'data-analysis'" class="mt-2 ml-4 space-y-1">
            <li>
              <router-link
                to="/"
                class="flex items-center gap-2 px-3 py-1.5 rounded text-sm hover:bg-gray-700 transition-colors"
                :class="$route.path === '/' ? 'bg-gray-700 text-primary' : 'text-gray-300'"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
                </svg>
                <span>基础数据</span>
              </router-link>
            </li>
            <li>
              <router-link
                to="/data-management"
                class="flex items-center gap-2 px-3 py-1.5 rounded text-sm hover:bg-gray-700 transition-colors"
                :class="$route.path === '/data-management' ? 'bg-gray-700 text-primary' : 'text-gray-300'"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
                </svg>
                <span>数据管理</span>
              </router-link>
            </li>
          </ul>
        </li>

        <li>
          <button
            @click="toggleSection('model-calling')"
            class="w-full flex items-center gap-3 px-3 py-2 rounded-lg transition-colors"
            :class="expandedSection === 'model-calling' ? 'bg-gray-700 text-white' : 'hover:bg-gray-700 text-gray-300'"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
            </svg>
            <span>模型调用</span>
            <svg v-if="expandedSection !== 'model-calling'" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 ml-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
            <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 ml-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
            </svg>
          </button>
          <!-- 子菜单 -->
          <ul v-if="expandedSection === 'model-calling'" class="mt-2 ml-4 space-y-1">
            <li>
              <router-link
                to="/model-calling"
                class="flex items-center gap-2 px-3 py-1.5 rounded text-sm hover:bg-gray-700 transition-colors"
                :class="$route.path === '/model-calling' ? 'bg-gray-700 text-primary' : 'text-gray-300'"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
                </svg>
                <span>模型列表</span>
              </router-link>
            </li>
            <li>
              <router-link
                to="/model-detail"
                class="flex items-center gap-2 px-3 py-1.5 rounded text-sm hover:bg-gray-700 transition-colors"
                :class="$route.path === '/model-detail' ? 'bg-gray-700 text-primary' : 'text-gray-300'"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
                <span>模型预测</span>
              </router-link>
            </li>
          </ul>
        </li>

        <li>
          <button
            @click="toggleSection('inventory')"
            class="w-full flex items-center gap-3 px-3 py-2 rounded-lg transition-colors"
            :class="expandedSection === 'inventory' ? 'bg-gray-700 text-white' : 'hover:bg-gray-700 text-gray-300'"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
            </svg>
            <span>入库管理</span>
            <svg v-if="expandedSection !== 'inventory'" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 ml-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
            <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 ml-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
            </svg>
          </button>
          <!-- 子菜单 -->
          <ul v-if="expandedSection === 'inventory'" class="mt-2 ml-4 space-y-1">
            <li>
              <router-link
                to="/inventory"
                class="flex items-center gap-2 px-3 py-1.5 rounded text-sm hover:bg-gray-700 transition-colors"
                :class="$route.path === '/inventory' ? 'bg-gray-700 text-primary' : 'text-gray-300'"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
                </svg>
                <span>入库报告</span>
              </router-link>
            </li>
          </ul>
        </li>

        <li>
          <button
            @click="toggleSection('guide')"
            class="w-full flex items-center gap-3 px-3 py-2 rounded-lg transition-colors"
            :class="expandedSection === 'guide' ? 'bg-gray-700 text-white' : 'hover:bg-gray-700 text-gray-300'"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
            </svg>
            <span>新手指南</span>
            <svg v-if="expandedSection !== 'guide'" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 ml-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
            <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 ml-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
            </svg>
          </button>
          <!-- 子菜单 -->
          <ul v-if="expandedSection === 'guide'" class="mt-2 ml-4 space-y-1">
            <li>
              <router-link
                to="/guide"
                class="flex items-center gap-2 px-3 py-1.5 rounded text-sm hover:bg-gray-700 transition-colors"
                :class="$route.path === '/guide' ? 'bg-gray-700 text-primary' : 'text-gray-300'"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                </svg>
                <span>快速入门</span>
              </router-link>
            </li>
          </ul>
        </li>
      </ul>
    </nav>

    <!-- 底部信息 -->
    <div class="p-4 border-t border-gray-700">
      <p class="text-xs text-gray-400 text-center">© 2025 实体商家</p>
    </div>
  </aside>
</template>

<script setup>
import { ref } from 'vue'

const expandedSection = ref('data-analysis')

const toggleSection = (section) => {
  expandedSection.value = expandedSection.value === section ? '' : section
}
</script>

<style scoped>
.sidebar {
  position: fixed;
  left: 0;
  top: 0;
  z-index: 100;
}
</style>
