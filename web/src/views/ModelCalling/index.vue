<template>
  <div class="model-calling">
    <!-- 页面标题 -->
    <header class="bg-gradient-to-r from-primary to-secondary text-white py-8 px-6">
      <div class="max-w-7xl mx-auto">
        <h1 class="text-3xl font-bold mb-2">模型调用</h1>
        <p class="text-white/80">多模型融合的智能销量预测分析平台</p>
      </div>
    </header>

    <main class="max-w-7xl mx-auto px-6 py-8">
      <!-- 模型列表表格 -->
      <section class="section">
        <div class="flex justify-between items-center mb-6">
          <h2>📊 模型列表</h2>
          <router-link to="/model-detail" class="btn btn-primary">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 inline-block mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
            查看模型预测
          </router-link>
        </div>
        <div class="table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th>排名</th>
                <th>模型名称</th>
                <th>发布单位</th>
                <th>WMAPE</th>
                <th>简介</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="model in sortedModels" :key="model.id">
                <td>
                  <span 
                    class="inline-flex items-center justify-center w-8 h-8 rounded-full text-sm font-bold"
                    :class="getRankClass(model.ranking)"
                  >
                    {{ model.ranking }}
                  </span>
                </td>
                <td class="font-semibold">{{ model.name }}</td>
                <td>{{ model.company }}</td>
                <td :class="getMetricClass(model.wmape)">{{ model.wmape ? model.wmape.toFixed(2) + '%' : 'N/A' }}</td>
                <td class="max-w-md truncate" :title="model.description">{{ model.description }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <!-- 回测结果排名 -->
      <section class="section">
        <h2>🏆 滚动窗口回测结果（WMAPE排名前五）</h2>
        <div class="grid grid-cols-1 md:grid-cols-5 gap-4">
          <div 
            v-for="result in backtestResults" 
            :key="result.rank"
            class="rank-card"
            :class="getRankCardClass(result.rank)"
          >
            <div class="rank-badge">第{{ result.rank }}名</div>
            <div class="model-name">{{ result.model_name }}</div>
            <div class="metrics">
              <div class="metric">
                <span class="label">WMAPE</span>
                <span class="value">{{ result.wmape.toFixed(2) }}%</span>
              </div>
            </div>
            <div class="description">{{ result.description }}</div>
          </div>
        </div>

        <!-- 回测结果表格 -->
        <div class="mt-6">
          <h3 class="text-lg font-semibold mb-3">详细回测数据</h3>
          <div class="table-container">
            <table class="data-table">
              <thead>
                <tr>
                  <th>排名</th>
                  <th>模型名称</th>
                  <th>WMAPE</th>
                  <th>评价</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="result in backtestResults" :key="result.rank">
                  <td>
                    <span 
                      class="inline-flex items-center justify-center w-6 h-6 rounded-full text-xs font-bold"
                      :class="getRankClass(result.rank)"
                    >
                      {{ result.rank }}
                    </span>
                  </td>
                  <td class="font-semibold">{{ result.model_name }}</td>
                  <td :class="getMetricClass(result.wmape)">{{ result.wmape ? result.wmape.toFixed(2) + '%' : 'N/A' }}</td>
                  <td>{{ result.description }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </section>
    </main>

    <!-- 页脚 -->
    <footer class="bg-gray-800 text-white py-4 px-6">
      <div class="max-w-7xl mx-auto text-center text-sm">
        <p>实体商家销量预测系统 © 2025</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { models, backtestResults } from '@/data/models'

const sortedModels = computed(() => {
  return [...models].sort((a, b) => a.ranking - b.ranking)
})

const getRankClass = (rank) => {
  switch (rank) {
    case 1:
      return 'bg-yellow-400 text-yellow-900'
    case 2:
      return 'bg-gray-300 text-gray-700'
    case 3:
      return 'bg-orange-400 text-orange-900'
    default:
      return 'bg-gray-100 text-gray-600'
  }
}

const getRankCardClass = (rank) => {
  switch (rank) {
    case 1:
      return 'border-yellow-400 bg-gradient-to-br from-yellow-50 to-yellow-100'
    case 2:
      return 'border-gray-300 bg-gradient-to-br from-gray-50 to-gray-100'
    case 3:
      return 'border-orange-400 bg-gradient-to-br from-orange-50 to-orange-100'
    default:
      return 'border-blue-300 bg-gradient-to-br from-blue-50 to-blue-100'
  }
}

const getMetricClass = (value) => {
  if (!value) return 'text-gray-400'
  if (value < 10) return 'text-green-600 font-semibold'
  if (value < 35) return 'text-yellow-600 font-semibold'
  return 'text-red-600 font-semibold'
}
</script>

<style scoped>
.rank-card {
  @apply p-4 rounded-lg border-2 transition-transform hover:scale-105;
}

.rank-badge {
  @apply text-3xl font-bold mb-2;
}

.model-name {
  @apply text-lg font-semibold mb-2;
}

.metrics {
  @apply mb-2;
}

.metric {
  @apply flex justify-between text-sm;
}

.metric .label {
  @apply text-gray-500;
}

.metric .value {
  @apply font-bold text-primary;
}

.description {
  @apply text-xs text-gray-600;
}
</style>
