<template>
  <div class="product-detail">
    <!-- 返回按钮 -->
    <header class="bg-white shadow-sm">
      <div class="max-w-7xl mx-auto px-6 py-4">
        <button @click="goBack" class="flex items-center gap-2 text-gray-600 hover:text-primary transition-colors">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
          返回首页
        </button>
      </div>
    </header>

    <main class="max-w-7xl mx-auto px-6 py-8">
      <!-- 加载状态 -->
      <div v-if="loading" class="flex justify-center items-center h-64">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
      </div>

      <!-- 错误状态 -->
      <div v-else-if="error" class="flex flex-col items-center justify-center h-64">
        <div class="text-6xl mb-4">❌</div>
        <p class="text-gray-600">{{ error }}</p>
        <button @click="loadData" class="mt-4 btn btn-primary">重新加载</button>
      </div>

      <!-- 内容 -->
      <template v-else>
        <!-- 页面标题 -->
        <div class="mb-6">
          <h1 class="text-2xl font-bold text-gray-800">{{ productData.product_name }}</h1>
          <p class="text-gray-600 mt-1">{{ productData.product_id }} · {{ productData.industry }}</p>
        </div>

      <!-- 基本信息卡片 -->
      <section class="section">
        <h2>📋 基本信息</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <div class="info-card">
            <span class="label">时间窗口</span>
            <span class="value">{{ productData.time_window }}</span>
          </div>
          <div class="info-card">
            <span class="label">商品名称</span>
            <span class="value">{{ productData.product_name }}</span>
          </div>
          <div class="info-card">
            <span class="label">商品编码</span>
            <span class="value font-mono">{{ productData.product_id }}</span>
          </div>
          <div class="info-card">
            <span class="label">门店地址</span>
            <span class="value">{{ productData.address }}</span>
          </div>
        </div>
      </section>

      <!-- 统计指标卡片 -->
      <section class="section">
        <h2>📈 统计指标</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <div class="stat-card">
            <div class="stat-icon">💰</div>
            <div class="stat-info">
              <span class="stat-label">售价均值</span>
              <span class="stat-value">¥{{ productData.statistics.price_mean.toFixed(2) }}</span>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">📊</div>
            <div class="stat-info">
              <span class="stat-label">售价众数</span>
              <span class="stat-value">¥{{ productData.statistics.price_mode.toFixed(2) }}</span>
            </div>
          </div>
          <div class="stat-card highlight">
            <div class="stat-icon">📈</div>
            <div class="stat-info">
              <span class="stat-label">销量最大值</span>
              <span class="stat-value">{{ productData.statistics.sales_max }} 件</span>
              <span class="stat-date">{{ productData.statistics.sales_max_date }}</span>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">📉</div>
            <div class="stat-info">
              <span class="stat-label">销量最小值</span>
              <span class="stat-value">{{ productData.statistics.sales_min }} 件</span>
              <span class="stat-date">{{ productData.statistics.sales_min_date }}</span>
            </div>
          </div>
        </div>
      </section>

      <!-- 销量时序图 -->
      <section class="section">
        <h2>📊 销量时序图</h2>
        <div class="chart-container">
          <v-chart :option="chartOption" autoresize />
        </div>
      </section>

      <!-- 销量与气温双轴图 -->
      <section class="section">
        <h2>🌡️ 销量与气温趋势对比</h2>
        <div class="chart-container">
          <v-chart :option="dualAxisChartOption" autoresize />
        </div>
      </section>

      <!-- 原始数据表格 -->
      <section class="section">
        <h2>📁 原始数据</h2>
        <div class="table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th>日期</th>
                <th>销量</th>
                <th>日平均气温(°C)</th>
                <th>平均售价(¥)</th>
                <th>节假日</th>
                <th>打折</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(row, index) in displayedData" :key="index">
                <td>{{ row.date }}</td>
                <td>{{ row.sales }}</td>
                <td>{{ row.temperature }}</td>
                <td>{{ (8 + Math.random() * 6).toFixed(2) }}</td>
                <td>{{ isHoliday(row.date) ? '是' : '否' }}</td>
                <td>{{ Math.random() > 0.7 ? '是' : '否' }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        <div v-if="productData.time_series && productData.time_series.length > 10" class="mt-4 flex justify-center">
          <button 
            @click="loadMore" 
            class="btn btn-primary"
            v-if="currentPage < totalPages"
          >
            加载更多数据
          </button>
          <p v-else class="text-gray-500">已加载全部数据</p>
        </div>
      </section>
      </template>
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
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { LineChart } from 'echarts/charts'
import { TitleComponent, TooltipComponent, LegendComponent, GridComponent } from 'echarts/components'
import { products } from '@/data/products'

use([CanvasRenderer, LineChart, TitleComponent, TooltipComponent, LegendComponent, GridComponent])

const route = useRoute()
const router = useRouter()
const productData = ref({})
const currentPage = ref(1)
const pageSize = 10
const loading = ref(true)
const error = ref(null)

const totalPages = computed(() => {
  if (!productData.value.time_series) return 1
  return Math.ceil(productData.value.time_series.length / pageSize)
})

const displayedData = computed(() => {
  if (!productData.value.time_series) return []
  return productData.value.time_series.slice(0, currentPage.value * pageSize)
})

const loadData = async () => {
  loading.value = true
  error.value = null
  try {
    const productId = route.params.productId
    
    // 从示例数据加载历史记录
    const response = await fetch(`${import.meta.env.BASE_URL}data/products_history_data.json`)
    const historyData = await response.json()
    
    const productInfo = products.find(p => p.product_id === productId)
    const productHistory = historyData[productId]
    
    if (productHistory && productHistory.data) {
      // 转换数据格式
      const timeSeries = productHistory.data.map(record => ({
        date: record.date,
        sales: record.sales,
        temperature: record.temperature
      }))
      
      const salesValues = timeSeries.map(t => t.sales)

      // Compute the mode of the observed prices (the previous demo hard-coded 0).
      const priceCounts = new Map()
      productHistory.data.forEach((record) => {
        const price = Number(record.avg_price)
        if (!Number.isNaN(price)) {
          priceCounts.set(price, (priceCounts.get(price) || 0) + 1)
        }
      })
      let priceMode = 0
      let priceModeCount = 0
      priceCounts.forEach((count, price) => {
        if (count > priceModeCount) {
          priceMode = price
          priceModeCount = count
        }
      })

      productData.value = {
        product_id: productId,
        product_name: productHistory.product_name || productInfo?.product_name || '未知商品',
        industry: productHistory.industry || productInfo?.industry || '',
        address: productHistory.address || productInfo?.address || '',
        time_window: timeSeries.length > 0 
          ? `${timeSeries[0].date} 至 ${timeSeries[timeSeries.length - 1].date}` 
          : '',
        statistics: {
          price_mean: productHistory.data.length > 0
            ? Math.round(productHistory.data.reduce((sum, r) => sum + (r.avg_price || 0), 0) / productHistory.data.length * 100) / 100
            : 0,
          price_mode: Math.round(priceMode * 100) / 100,
          sales_max: salesValues.length > 0 ? Math.max(...salesValues) : 0,
          sales_max_date: salesValues.length > 0 
            ? timeSeries[salesValues.indexOf(Math.max(...salesValues))].date 
            : '',
          sales_min: salesValues.length > 0 ? Math.min(...salesValues) : 0,
          sales_min_date: salesValues.length > 0 
            ? timeSeries[salesValues.indexOf(Math.min(...salesValues))].date 
            : ''
        },
        time_series: timeSeries
      }
    } else {
      // 如果没有示例数据，使用模拟数据作为备用
      const product = products.find(p => p.product_id === productId) || products[0]
      const startDate = new Date('2025-01-01')
      const timeSeries = []
      
      for (let i = 0; i < 126; i++) {
        const date = new Date(startDate)
        date.setDate(date.getDate() + i)
        const baseSales = 100 + Math.random() * 100
        const temperature = 15 + Math.sin(i / 30) * 10 + Math.random() * 5
        const sales = Math.round(baseSales)
        
        timeSeries.push({
          date: date.toISOString().split('T')[0],
          sales,
          temperature: Math.round(temperature * 10) / 10
        })
      }
      
      const salesValues = timeSeries.map(t => t.sales)
      
      productData.value = {
        product_id: productId,
        product_name: product.product_name,
        industry: product.industry,
        address: product.address,
        time_window: '2025-01-01 至 2025-05-06',
        statistics: {
          price_mean: Math.round((8 + Math.random() * 6) * 100) / 100,
          price_mode: Math.round((8 + Math.random() * 4) * 100) / 100,
          sales_max: Math.max(...salesValues),
          sales_max_date: timeSeries[salesValues.indexOf(Math.max(...salesValues))].date,
          sales_min: Math.min(...salesValues),
          sales_min_date: timeSeries[salesValues.indexOf(Math.min(...salesValues))].date
        },
        time_series: timeSeries
      }
    }
    
    loading.value = false
  } catch (e) {
    console.error('加载数据失败:', e)
    error.value = '加载数据失败，请重试'
    loading.value = false
  }
}

onMounted(() => {
  loadData()
})

const goBack = () => {
  router.push('/')
}

const loadMore = () => {
  currentPage.value++
}

const isHoliday = (dateStr) => {
  const date = new Date(dateStr)
  const month = date.getMonth() + 1
  const day = date.getDate()
  const holidays = [
    { month: 1, day: 1 },
    { month: 1, day: 2 },
    { month: 1, day: 3 },
    { month: 2, day: 14 },
    { month: 4, day: 4 },
    { month: 5, day: 1 },
    { month: 5, day: 4 },
    { month: 6, day: 2 },
  ]
  return holidays.some(h => h.month === month && h.day === day)
}

const chartOption = computed(() => {
  const dates = productData.value.time_series ? productData.value.time_series.map(t => t.date) : []
  const sales = productData.value.time_series ? productData.value.time_series.map(t => t.sales) : []
  
  return {
    title: {
      text: `${productData.value.product_name} 销量趋势`,
      left: 'center'
    },
    tooltip: {
      trigger: 'axis'
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: dates,
      axisLabel: {
        rotate: 45,
        fontSize: 10
      }
    },
    yAxis: {
      type: 'value',
      name: '销量(件)'
    },
    series: [
      {
        name: '销量',
        type: 'line',
        smooth: true,
        data: sales,
        lineStyle: {
          color: '#4CAF50',
          width: 2
        },
        areaStyle: {
          color: {
            type: 'linear',
            x: 0,
            y: 0,
            x2: 0,
            y2: 1,
            colorStops: [
              { offset: 0, color: 'rgba(76, 175, 80, 0.3)' },
              { offset: 1, color: 'rgba(76, 175, 80, 0.05)' }
            ]
          }
        }
      }
    ]
  }
})

const dualAxisChartOption = computed(() => {
  const dates = productData.value.time_series ? productData.value.time_series.map(t => t.date) : []
  const sales = productData.value.time_series ? productData.value.time_series.map(t => t.sales) : []
  const temps = productData.value.time_series ? productData.value.time_series.map(t => t.temperature) : []
  
  return {
    title: {
      text: '销量与气温趋势对比',
      left: 'center'
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'cross',
        crossStyle: {
          color: '#999'
        }
      }
    },
    legend: {
      data: ['销量', '气温'],
      top: 30
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: [
      {
        type: 'category',
        data: dates,
        axisPointer: {
          type: 'shadow'
        },
        axisLabel: {
          rotate: 45,
          fontSize: 10
        }
      }
    ],
    yAxis: [
      {
        type: 'value',
        name: '销量(件)',
        min: 0,
        axisLabel: {
          formatter: '{value}'
        }
      },
      {
        type: 'value',
        name: '气温(°C)',
        min: 0,
        axisLabel: {
          formatter: '{value}°'
        }
      }
    ],
    series: [
      {
        name: '销量',
        type: 'line',
        smooth: true,
        data: sales,
        lineStyle: {
          color: '#4CAF50',
          width: 2
        }
      },
      {
        name: '气温',
        type: 'line',
        yAxisIndex: 1,
        smooth: true,
        data: temps,
        lineStyle: {
          color: '#FF9800',
          width: 2
        }
      }
    ]
  }
})
</script>

<style scoped>
.info-card {
  @apply bg-gray-50 rounded-lg p-4 border border-gray-200;
}

.info-card .label {
  @apply text-sm text-gray-500 block mb-1;
}

.info-card .value {
  @apply text-lg font-semibold text-gray-800;
}

.stat-card {
  @apply bg-white rounded-lg shadow-md p-4 flex items-center gap-4;
}

.stat-card.highlight {
  @apply bg-gradient-to-r from-green-50 to-green-100 border border-green-200;
}

.stat-icon {
  @apply text-3xl;
}

.stat-info {
  @apply flex flex-col;
}

.stat-label {
  @apply text-sm text-gray-500;
}

.stat-value {
  @apply text-xl font-bold text-gray-800;
}

.stat-date {
  @apply text-xs text-gray-400;
}

.chart-container {
  @apply w-full h-96;
}
</style>
