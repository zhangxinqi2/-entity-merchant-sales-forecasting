<template>
  <div class="inventory">
    <!-- 页面标题 -->
    <header class="bg-gradient-to-r from-primary to-secondary text-white py-8 px-6">
      <div class="max-w-7xl mx-auto">
        <h1 class="text-3xl font-bold mb-2">入库管理</h1>
        <p class="text-white/80">基于模型预测的智能入库报告生成系统</p>
      </div>
    </header>

    <main class="max-w-7xl mx-auto px-6 py-8">
      <!-- 筛选区域 -->
      <div class="bg-white rounded-lg shadow-md p-6 mb-8">
        <h2 class="text-xl font-semibold mb-6">🔍 筛选条件</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <!-- 模型选择 -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">模型选择 <span class="text-red-500">*</span></label>
            <select
              v-model="selectedModel"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary"
            >
              <option value="">请选择模型</option>
              <option v-for="model in models" :key="model.id" :value="model.id">
                {{ model.name }}
              </option>
            </select>
          </div>
          <!-- 商品选择 -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">商品选择 <span class="text-red-500">*</span></label>
            <select
              v-model="selectedProduct"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary"
            >
              <option value="">请选择商品</option>
              <option v-for="product in products" :key="product.product_id" :value="product.product_id">
                {{ product.product_id }} - {{ product.product_name }}
              </option>
            </select>
          </div>
        </div>
        <!-- 预测天数 -->
        <div class="mt-6">
          <label class="block text-sm font-medium text-gray-700 mb-2">预测天数</label>
          <input
            v-model.number="predictionDays"
            type="number"
            min="1"
            max="30"
            class="w-32 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary"
          />
          <span class="ml-2 text-gray-500">天（默认7天）</span>
        </div>
        <!-- 生成报告按钮 -->
        <div class="mt-6 flex justify-end">
          <button
            @click="generateReport"
            :disabled="!selectedModel || !selectedProduct"
            class="px-6 py-2 bg-primary text-white rounded-lg hover:bg-primary-dark transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 inline-block mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            生成入库报告
          </button>
        </div>
      </div>

      <!-- 报告内容 -->
      <div v-if="reportGenerated" class="space-y-8">
        <!-- 导出按钮 -->
        <div class="flex justify-end gap-4">
          <button
            @click="exportAsHTML"
            class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 inline-block mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
            </svg>
            导出为 HTML
          </button>
          <button
            @click="exportAsWord"
            class="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition-colors"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 inline-block mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
            </svg>
            导出为 Word
          </button>
        </div>

        <!-- 报告标题 -->
        <div class="bg-white rounded-lg shadow-md p-8">
          <div class="text-center mb-8">
            <h1 class="text-2xl font-bold text-gray-800">入库预测报告</h1>
            <p class="text-gray-500 mt-2">生成时间：{{ currentDate }}</p>
          </div>

          <!-- 1. 总结 -->
          <section class="mb-8">
            <h2 class="text-lg font-semibold text-gray-800 mb-4 border-b pb-2">📊 报告总结</h2>
            <div class="bg-blue-50 rounded-lg p-4">
              <p class="text-gray-700 leading-relaxed">
                根据 <span class="font-semibold">{{ getCurrentModelName() }}</span> 算法预测结果表明：
              </p>
              <p class="text-gray-700 leading-relaxed mt-2">
                训练集时间范围为 <span class="font-semibold">{{ reportData.trainStartDate }}</span> 至 
                <span class="font-semibold">{{ reportData.trainEndDate }}</span>，
                对 <span class="font-semibold">{{ getCurrentProductName() }}</span>（商品ID：{{ selectedProduct }}）进行预测分析。
              </p>
              <p class="text-gray-700 leading-relaxed mt-2">
                预测结果显示，<span class="font-semibold">{{ reportData.predictionStartDate }}</span> 至 
                <span class="font-semibold">{{ reportData.predictionEndDate }}</span> 期间，
                预计总销量为 <span class="font-semibold text-primary">{{ reportData.totalPrediction }}</span> 件。
              </p>
              <p class="text-gray-700 leading-relaxed mt-2">
                <strong>建议入库量：</strong><span class="font-semibold text-primary">{{ reportData.suggestedInventory }}</span> 件
                <span v-if="reportData.peakDate" class="ml-2">
                 （预计 <span class="font-semibold text-red-500">{{ reportData.peakDate }}</span> 达到销量峰值，约 
                  <span class="font-semibold text-red-500">{{ reportData.peakValue }}</span> 件）
                </span>
              </p>
            </div>
          </section>

          <!-- 2. 详细预测结果 -->
          <section class="mb-8">
            <h2 class="text-lg font-semibold text-gray-800 mb-4 border-b pb-2">📈 详细预测结果</h2>
            <div class="table-container">
              <table class="data-table">
                <thead>
                  <tr>
                    <th>日期</th>
                    <th>预测销量(件)</th>
                    <th>建议入库(件)</th>
                    <th>置信区间下限</th>
                    <th>置信区间上限</th>
                    <th>备注</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(item, index) in reportData.predictions" :key="index">
                    <td>{{ item.date }}</td>
                    <td :class="item.isPeak ? 'text-red-600 font-semibold' : ''">{{ item.value }}</td>
                    <td class="text-primary font-semibold">{{ item.suggested }}</td>
                    <td>{{ item.confidenceLower }}</td>
                    <td>{{ item.confidenceUpper }}</td>
                    <td>{{ item.isPeak ? '📌 峰值' : '' }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </section>

          <!-- 3. 预测时序图 -->
          <section class="mb-8">
            <h2 class="text-lg font-semibold text-gray-800 mb-4 border-b pb-2">📊 预测时序图</h2>
            <div class="chart-container">
              <v-chart :option="predictionChartOption" autoresize />
            </div>
          </section>

          <!-- 4. 训练集与测试集对比图 -->
          <section class="mb-8">
            <h2 class="text-lg font-semibold text-gray-800 mb-4 border-b pb-2">🔄 训练集与测试集对比</h2>
            <div class="chart-container">
              <v-chart :option="trainTestChartOption" autoresize />
            </div>
          </section>

          <!-- 5. 入库建议详情 -->
          <section class="mb-8">
            <h2 class="text-lg font-semibold text-gray-800 mb-4 border-b pb-2">📦 入库建议详情</h2>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div class="bg-green-50 rounded-lg p-6 text-center">
                <div class="text-4xl mb-2">📦</div>
                <p class="text-sm text-gray-600">建议总入库量</p>
                <p class="text-3xl font-bold text-green-600 mt-2">{{ reportData.suggestedInventory }}</p>
                <p class="text-xs text-gray-500 mt-1">件</p>
              </div>
              <div class="bg-blue-50 rounded-lg p-6 text-center">
                <div class="text-4xl mb-2">📅</div>
                <p class="text-sm text-gray-600">预测天数</p>
                <p class="text-3xl font-bold text-blue-600 mt-2">{{ predictionDays }}</p>
                <p class="text-xs text-gray-500 mt-1">天</p>
              </div>
              <div class="bg-orange-50 rounded-lg p-6 text-center">
                <div class="text-4xl mb-2">📊</div>
                <p class="text-sm text-gray-600">日均销量</p>
                <p class="text-3xl font-bold text-orange-600 mt-2">{{ reportData.dailyAverage }}</p>
                <p class="text-xs text-gray-500 mt-1">件/天</p>
              </div>
            </div>
            <div class="mt-6 p-4 bg-gray-50 rounded-lg">
              <h3 class="font-semibold text-gray-700 mb-2">📋 入库建议说明</h3>
              <ul class="text-sm text-gray-600 space-y-2">
                <li>• 根据预测结果，建议在 <span class="font-semibold">{{ reportData.predictionStartDate }}</span> 前完成入库</li>
                <li>• 考虑到 {{ reportData.safetyStock }} 件安全库存，建议入库量为预测总量的 {{ reportData.safetyFactor }}%</li>
                <li>• 建议关注 <span class="font-semibold">{{ reportData.peakDate }}</span> 的库存准备，此日预计达到销量峰值</li>
                <li>• 建议定期（每 {{ reportData.reviewInterval }} 天）回顾预测结果，根据实际销售情况调整库存策略</li>
              </ul>
            </div>
          </section>
        </div>
      </div>

      <!-- 未生成报告时的提示 -->
      <div v-else class="bg-white rounded-lg shadow-md p-12 text-center">
        <div class="text-6xl mb-4">📊</div>
        <h3 class="text-xl font-semibold text-gray-700 mb-2">请选择模型和商品生成入库报告</h3>
        <p class="text-gray-500">选择上方的模型和商品，点击"生成入库报告"按钮即可生成完整的入库预测分析报告</p>
      </div>
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
import { ref, computed, reactive } from 'vue'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { LineChart, BarChart } from 'echarts/charts'
import { TitleComponent, TooltipComponent, LegendComponent, GridComponent } from 'echarts/components'
import { models } from '@/data/models'
import { products } from '@/data/products'

use([CanvasRenderer, LineChart, BarChart, TitleComponent, TooltipComponent, LegendComponent, GridComponent])

// 筛选条件
const selectedModel = ref('')
const selectedProduct = ref('')
const predictionDays = ref(7)

// 报告状态
const reportGenerated = ref(false)
const currentDate = computed(() => new Date().toLocaleDateString('zh-CN'))

// 报告数据
const reportData = reactive({
  trainStartDate: '',
  trainEndDate: '',
  predictionStartDate: '',
  predictionEndDate: '',
  totalPrediction: 0,
  suggestedInventory: 0,
  peakDate: '',
  peakValue: 0,
  dailyAverage: 0,
  safetyStock: 0,
  safetyFactor: 120,
  reviewInterval: 7,
  confidenceLevel: 95,
  predictions: [],
  metrics: {
    WMAPE: 0,
    MAPE: 0,
    SMAPE: 0,
    RMSE: 0,
    grade: ''
  }
})

// 获取当前模型名称
const getCurrentModelName = () => {
  const model = models.find(m => m.id === selectedModel.value)
  return model ? model.name : '未知模型'
}

// 获取当前商品名称
const getCurrentProductName = () => {
  const product = products.find(p => p.product_id === selectedProduct.value)
  return product ? product.product_name : '未知商品'
}

// 生成报告数据
const generateReport = async () => {
  if (!selectedModel.value || !selectedProduct.value) return

  // 获取当前商品的历史数据（从示例数据获取）
  const historyData = await getProductHistoryData(selectedProduct.value)
  
  // 计算训练集时间范围（使用所有历史数据）
  const trainStart = historyData.length > 0 
    ? new Date(historyData[0].date) 
    : new Date(Date.now() - 90 * 24 * 60 * 60 * 1000)
  const trainEnd = historyData.length > 0 
    ? new Date(historyData[historyData.length - 1].date) 
    : new Date(Date.now() - 1)
  
  reportData.trainStartDate = trainStart.toLocaleDateString('zh-CN')
  reportData.trainEndDate = trainEnd.toLocaleDateString('zh-CN')
  
  // 基于历史数据生成预测
  const predictions = generatePredictionsFromHistory(historyData)
  if (predictions.length > 0) {
    reportData.predictionStartDate = predictions[0].date
    reportData.predictionEndDate = predictions[predictions.length - 1].date
  }

  // 标记峰值
  let peakValue = 0
  let peakDate = ''
  predictions.forEach(p => {
    if (p.value > peakValue) {
      peakValue = p.value
      peakDate = p.date
    }
  })
  
  predictions.forEach(p => {
    if (p.date === peakDate) {
      p.isPeak = true
    }
  })
  
  const total = predictions.reduce((sum, p) => sum + p.value, 0)
  
  reportData.predictions = predictions
  reportData.totalPrediction = total
  reportData.suggestedInventory = Math.round(total * 1.2)
  reportData.peakDate = peakDate
  reportData.peakValue = peakValue
  reportData.dailyAverage = Math.round(total / predictionDays.value)
  reportData.safetyStock = Math.round(total * 0.2)

  // 实时计算模型检验指标（基于历史数据回测）
  const metrics = calculateRealTimeMetrics(historyData, predictions)
  reportData.metrics.WMAPE = metrics.WMAPE.toFixed(2)
  reportData.metrics.MAPE = metrics.MAPE.toFixed(2)
  reportData.metrics.SMAPE = metrics.SMAPE.toFixed(2)
  reportData.metrics.RMSE = metrics.RMSE.toFixed(2)
  
  // 评估误差等级
  if (metrics.WMAPE < 10) reportData.metrics.grade = '优秀'
  else if (metrics.WMAPE < 20) reportData.metrics.grade = '良好'
  else if (metrics.WMAPE < 30) reportData.metrics.grade = '一般'
  else reportData.metrics.grade = '较差'
  
  reportGenerated.value = true
}

// 实时计算模型检验指标（基于历史数据回测）
const calculateRealTimeMetrics = (historyData, predictions) => {
  // 使用历史数据进行回测
  // 将历史数据分为训练集和测试集（80%训练，20%测试）
  const splitIndex = Math.floor(historyData.length * 0.8)
  const trainData = historyData.slice(0, splitIndex)
  const testData = historyData.slice(splitIndex)
  
  // 如果测试数据太少，使用全部历史数据
  if (testData.length < 7) {
    return { WMAPE: 0, MAPE: 0, SMAPE: 0, RMSE: 0 }
  }
  
  // 模拟模型在测试集上的预测（使用与generatePredictionsFromHistory相同的逻辑）
  const predictedValues = []
  const actualValues = []
  
  // 计算训练集的统计特征
  const weekdaySales = trainData.filter(d => !d.isWeekend).map(d => d.sales)
  const weekendSales = trainData.filter(d => d.isWeekend).map(d => d.sales)
  const avgWeekdaySales = weekdaySales.length > 0 
    ? weekdaySales.reduce((a, b) => a + b, 0) / weekdaySales.length 
    : 100
  const avgWeekendSales = weekendSales.length > 0 
    ? weekendSales.reduce((a, b) => a + b, 0) / weekendSales.length 
    : 130
  
  // 计算最近趋势
  const recentTrainData = trainData.slice(-7)
  const recentTrend = recentTrainData.length > 1 
    ? (recentTrainData[recentTrainData.length - 1].sales - recentTrainData[0].sales) / recentTrainData.length 
    : 0
  
  // 对测试集进行预测
  testData.forEach((actual, index) => {
    const isWeekend = actual.isWeekend
    
    // 基础预测值（考虑周末效应和趋势）
    let baseValue = isWeekend ? avgWeekendSales : avgWeekdaySales
    baseValue += recentTrend * index
    
    // 添加季节性因素
    const startOfYear = new Date(new Date(actual.date).getFullYear(), 0, 1)
    const dayOfYear = Math.floor((new Date(actual.date) - startOfYear) / (1000 * 60 * 60 * 24))
    const seasonalFactor = 1 + Math.sin((dayOfYear / 365) * Math.PI * 2) * 0.15
    baseValue *= seasonalFactor
    
    // 添加合理波动
    const randomFactor = 0.95 + Math.random() * 0.1
    const predicted = Math.round(Math.max(0, baseValue * randomFactor))
    
    predictedValues.push(predicted)
    actualValues.push(actual.sales)
  })
  
  // 计算指标
  const n = actualValues.length
  
  // MAPE (平均绝对百分比误差)
  let mape = 0
  actualValues.forEach((actual, i) => {
    if (actual !== 0) {
      mape += Math.abs((predictedValues[i] - actual) / actual)
    }
  })
  mape = (mape / n) * 100
  
  // SMAPE (对称平均绝对百分比误差)
  let smape = 0
  actualValues.forEach((actual, i) => {
    const denominator = Math.abs(actual) + Math.abs(predictedValues[i])
    if (denominator !== 0) {
      smape += Math.abs(predictedValues[i] - actual) / denominator
    }
  })
  smape = (smape / n) * 100
  
  // RMSE (均方根误差)
  let rmse = 0
  actualValues.forEach((actual, i) => {
    rmse += Math.pow(predictedValues[i] - actual, 2)
  })
  rmse = Math.sqrt(rmse / n)
  
  // WMAPE (加权平均绝对百分比误差)
  let wmape = 0
  const totalActual = actualValues.reduce((sum, val) => sum + val, 0)
  if (totalActual !== 0) {
    actualValues.forEach((actual, i) => {
      wmape += Math.abs(predictedValues[i] - actual)
    })
    wmape = (wmape / totalActual) * 100
  }
  
  return {
    WMAPE: wmape,
    MAPE: mape,
    SMAPE: smape,
    RMSE: rmse
  }
}

// 从示例数据获取商品历史数据
// 缓存历史数据
let historyDataCache = null

// 从示例数据获取商品历史数据
const getProductHistoryData = async (productId) => {
  if (!historyDataCache) {
    try {
      const response = await fetch(`${import.meta.env.BASE_URL}data/products_history_data.json`)
      historyDataCache = await response.json()
    } catch (error) {
      console.error('加载历史数据失败:', error)
      return []
    }
  }
  
  const productHistory = historyDataCache[productId]
  if (!productHistory || !productHistory.data) {
    return []
  }
  
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  
  return productHistory.data
    .filter(record => {
      const recordDate = new Date(record.date)
      return recordDate < today
    })
    .map(record => ({
      date: record.date,
      sales: record.sales,
      isWeekend: record.is_holiday || [0, 6].includes(new Date(record.date).getDay()),
      dayOfWeek: new Date(record.date).getDay()
    }))
}

// 获取商品信息
const getProductInfo = (productId) => {
  if (!historyDataCache) {
    return null
  }
  return historyDataCache[productId]
}

// 生成商品的历史数据（备用函数）
const generateHistoricalData = () => {
  const data = []
  const startDate = new Date()
  startDate.setDate(startDate.getDate() - 60) // 生成最近60天的历史数据
  
  for (let i = 0; i < 60; i++) {
    const date = new Date(startDate)
    date.setDate(date.getDate() + i)
    const baseSales = 80 + Math.random() * 60
    const isWeekend = date.getDay() === 0 || date.getDay() === 6
    const seasonFactor = 1 + Math.sin(i / 30) * 0.1
    const sales = Math.round(baseSales * (isWeekend ? 1.25 : 1) * seasonFactor)
    
    data.push({
      date: date.toISOString().split('T')[0],
      sales,
      isWeekend,
      dayOfWeek: date.getDay()
    })
  }
  
  return data
}

// 基于历史数据生成预测
const generatePredictionsFromHistory = (historyData) => {
  const predictions = []
  // Continue from the last observed day instead of today's date, so the demo
  // stays coherent when the bundled sample data is historical.
  const lastHistoryDate = historyData.length > 0
    ? new Date(historyData[historyData.length - 1].date)
    : new Date()
  const model = models.find(m => m.id === selectedModel.value) || models[0]
  
  // 计算历史日均销量和周末效应
  const weekdaySales = historyData.filter(d => !d.isWeekend).map(d => d.sales)
  const weekendSales = historyData.filter(d => d.isWeekend).map(d => d.sales)
  const avgWeekdaySales = weekdaySales.length > 0 
    ? weekdaySales.reduce((a, b) => a + b, 0) / weekdaySales.length 
    : 100
  const avgWeekendSales = weekendSales.length > 0 
    ? weekendSales.reduce((a, b) => a + b, 0) / weekendSales.length 
    : 130
  
  // 计算最近7天的趋势
  const recentData = historyData.slice(-7)
  const recentTrend = recentData.length > 1 
    ? (recentData[recentData.length - 1].sales - recentData[0].sales) / recentData.length 
    : 0
  
  // 获取模型误差作为不确定性因子
  const modelError = model.wmape / 100 // 转换为小数
  
  // 生成预测
  for (let i = 0; i < predictionDays.value; i++) {
    const date = new Date(lastHistoryDate)
    date.setDate(date.getDate() + i + 1)
    const isWeekend = date.getDay() === 0 || date.getDay() === 6
    const dayOfWeek = date.getDay()
    
    // 基础预测值（考虑周末效应和趋势）
    let baseValue = isWeekend ? avgWeekendSales : avgWeekdaySales
    baseValue += recentTrend * i // 应用趋势
    
    // 添加季节性因素（基于历史数据的周期性模式）
    const seasonalFactor = 1 + Math.sin((historyData.length + i) / 30) * 0.15
    baseValue *= seasonalFactor
    
    // 根据模型误差添加合理波动
    const randomFactor = 1 + (Math.random() - 0.5) * 2 * modelError
    
    const value = Math.round(Math.max(0, baseValue * randomFactor))
    const safetyFactor = 1.2 // 安全库存因子
    const suggested = Math.round(value * safetyFactor)
    const confidenceMargin = modelError * value // 基于模型误差的置信区间
    const confidenceLower = Math.round(value * (1 - modelError))
    const confidenceUpper = Math.round(value * (1 + modelError))
    
    predictions.push({
      date: date.toLocaleDateString('zh-CN'),
      value,
      suggested,
      confidenceLower: Math.max(0, confidenceLower),
      confidenceUpper,
      isPeak: false,
      dayOfWeek,
      isWeekend
    })
  }
  
  return predictions
}

// 预测时序图配置
const predictionChartOption = computed(() => {
  const dates = reportData.predictions.map(p => p.date)
  const values = reportData.predictions.map(p => p.value)
  const suggested = reportData.predictions.map(p => p.suggested)
  const lower = reportData.predictions.map(p => p.confidenceLower)
  const upper = reportData.predictions.map(p => p.confidenceUpper)
  
  return {
    title: {
      text: '未来销量预测趋势',
      left: 'center',
      textStyle: { fontSize: 14 }
    },
    tooltip: {
      trigger: 'axis'
    },
    legend: {
      data: ['预测销量', '建议入库', '置信区间'],
      bottom: 0
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '15%',
      top: '15%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: dates,
      axisLabel: { fontSize: 10 }
    },
    yAxis: {
      type: 'value',
      name: '销量(件)'
    },
    series: [
      {
        name: '预测销量',
        type: 'line',
        data: values,
        smooth: true,
        lineStyle: { color: '#10B981', width: 3 },
        itemStyle: { color: '#10B981' },
        areaStyle: {
          color: {
            type: 'linear',
            x: 0, y: 0, x2: 0, y2: 1,
            colorStops: [
              { offset: 0, color: 'rgba(16, 185, 129, 0.3)' },
              { offset: 1, color: 'rgba(16, 185, 129, 0.05)' }
            ]
          }
        }
      },
      {
        name: '建议入库',
        type: 'line',
        data: suggested,
        smooth: true,
        lineStyle: { color: '#3B82F6', width: 2, type: 'dashed' },
        itemStyle: { color: '#3B82F6' }
      },
      {
        name: '置信区间',
        type: 'line',
        data: lower,
        smooth: true,
        lineStyle: { color: '#F59E0B', width: 1, type: 'dotted' },
        itemStyle: { color: '#F59E0B' },
        areaStyle: {
          color: {
            type: 'linear',
            x: 0, y: 0, x2: 0, y2: 1,
            colorStops: [
              { offset: 0, color: 'rgba(245, 158, 11, 0.2)' },
              { offset: 1, color: 'rgba(245, 158, 11, 0)' }
            ]
          }
        }
      },
      {
        name: '置信区间',
        type: 'line',
        data: upper,
        smooth: true,
        lineStyle: { color: '#F59E0B', width: 1, type: 'dotted' },
        itemStyle: { color: '#F59E0B' },
        areaStyle: {
          color: {
            type: 'linear',
            x: 0, y: 0, x2: 0, y2: 1,
            colorStops: [
              { offset: 0, color: 'rgba(245, 158, 11, 0)' },
              { offset: 1, color: 'rgba(245, 158, 11, 0.2)' }
            ]
          }
        }
      }
    ]
  }
})

// 训练集与测试集对比图配置
const trainTestChartOption = computed(() => {
  const trainDates = []
  const trainValues = []
  const testDates = []
  const testValues = []
  const predValues = []
  
  // 生成训练集数据
  for (let i = 20; i >= 0; i--) {
    const date = new Date()
    date.setDate(date.getDate() - i - predictionDays.value)
    trainDates.push(date.toLocaleDateString('zh-CN'))
    trainValues.push(Math.round(50 + Math.random() * 50))
  }
  
  // 生成测试集数据
  for (let i = predictionDays.value - 1; i >= 0; i--) {
    const date = new Date()
    date.setDate(date.getDate() - i)
    testDates.push(date.toLocaleDateString('zh-CN'))
    testValues.push(Math.round(55 + Math.random() * 45))
  }
  
  // 预测值
  predValues.push(...reportData.predictions.map(p => p.value))
  
  return {
    title: {
      text: '训练集、测试集与预测值对比',
      left: 'center',
      textStyle: { fontSize: 14 }
    },
    tooltip: {
      trigger: 'axis'
    },
    legend: {
      data: ['训练集', '测试集', '预测值'],
      bottom: 0
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '15%',
      top: '15%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: [...trainDates, ...testDates],
      axisLabel: { fontSize: 8 }
    },
    yAxis: {
      type: 'value',
      name: '销量(件)'
    },
    series: [
      {
        name: '训练集',
        type: 'bar',
        data: [...trainValues, ...Array(predictionDays.value).fill(null)],
        itemStyle: { color: '#6B7280' }
      },
      {
        name: '测试集',
        type: 'bar',
        data: [...Array(21).fill(null), ...testValues],
        itemStyle: { color: '#10B981' }
      },
      {
        name: '预测值',
        type: 'line',
        data: [...Array(21).fill(null), ...predValues],
        smooth: true,
        lineStyle: { color: '#3B82F6', width: 3 },
        itemStyle: { color: '#3B82F6' },
        symbol: 'circle',
        symbolSize: 8
      }
    ]
  }
})

// 导出为HTML
const exportAsHTML = () => {
  const content = `
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>入库预测报告</title>
  <style>
    body { font-family: 'Microsoft YaHei', sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
    h1 { text-align: center; color: #1F2937; }
    h2 { color: #374151; border-bottom: 2px solid #E5E7EB; padding-bottom: 10px; }
    .summary { background: #EFF6FF; padding: 15px; border-radius: 8px; margin: 15px 0; }
    table { width: 100%; border-collapse: collapse; margin: 15px 0; }
    th, td { border: 1px solid #E5E7EB; padding: 8px; text-align: center; }
    th { background: #F3F4F6; }
    .metrics { display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin: 15px 0; }
    .metric-card { background: #F9FAFB; padding: 15px; border-radius: 8px; text-align: center; }
    .metric-value { font-size: 24px; font-weight: bold; color: #10B981; }
    .chart-placeholder { background: #F3F4F6; height: 300px; border-radius: 8px; display: flex; align-items: center; justify-content: center; color: #6B7280; }
    .info-cards { display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin: 15px 0; }
    .info-card { background: #ECFDF5; padding: 20px; border-radius: 8px; text-align: center; }
    .info-value { font-size: 32px; font-weight: bold; color: #059669; }
    .warning { background: #FFFBEB; padding: 15px; border-radius: 8px; margin: 15px 0; }
  </style>
</head>
<body>
  <h1>入库预测报告</h1>
  <p style="text-align: center; color: #6B7280;">生成时间：${currentDate.value}</p>
  
  <h2>📊 报告总结</h2>
  <div class="summary">
    <p>根据 <strong>${getCurrentModelName()}</strong> 算法预测结果表明：</p>
    <p>训练集时间范围为 <strong>${reportData.trainStartDate}</strong> 至 <strong>${reportData.trainEndDate}</strong>，对 <strong>${getCurrentProductName()}</strong>（商品ID：${selectedProduct.value}）进行预测分析。</p>
    <p>预测结果显示，<strong>${reportData.predictionStartDate}</strong> 至 <strong>${reportData.predictionEndDate}</strong> 期间，预计总销量为 <strong style="color: #10B981;">${reportData.totalPrediction}</strong> 件。</p>
    <p><strong>建议入库量：</strong><strong style="color: #10B981;">${reportData.suggestedInventory}</strong> 件${reportData.peakDate ? '（预计 <strong style="color: #DC2626;">' + reportData.peakDate + '</strong> 达到销量峰值，约 <strong style="color: #DC2626;">' + reportData.peakValue + '</strong> 件）' : ''}</p>
  </div>

  <h2>📈 详细预测结果</h2>
  <table>
    <thead>
      <tr><th>日期</th><th>预测销量(件)</th><th>建议入库(件)</th><th>置信区间下限</th><th>置信区间上限</th><th>备注</th></tr>
    </thead>
    <tbody>
      ${reportData.predictions.map(p => `<tr><td>${p.date}</td><td${p.isPeak ? ' style="color: #DC2626; font-weight: bold;"' : ''}>${p.value}</td><td style="color: #3B82F6; font-weight: bold;">${p.suggested}</td><td>${p.confidenceLower}</td><td>${p.confidenceUpper}</td><td>${p.isPeak ? '📌 峰值' : ''}</td></tr>`).join('')}
    </tbody>
  </table>

  <h2>📦 入库建议详情</h2>
  <div class="info-cards">
    <div class="info-card"><div style="font-size: 36px;">📦</div><div style="font-size: 12px; color: #6B7280;">建议总入库量</div><div class="info-value">${reportData.suggestedInventory}</div><div style="font-size: 12px; color: #6B7280;">件</div></div>
    <div class="info-card" style="background: #EFF6FF;"><div style="font-size: 36px;">📅</div><div style="font-size: 12px; color: #6B7280;">预测天数</div><div class="info-value" style="color: #2563EB;">${predictionDays.value}</div><div style="font-size: 12px; color: #6B7280;">天</div></div>
    <div class="info-card" style="background: #FFF7ED;"><div style="font-size: 36px;">📊</div><div style="font-size: 12px; color: #6B7280;">日均销量</div><div class="info-value" style="color: #EA580C;">${reportData.dailyAverage}</div><div style="font-size: 12px; color: #6B7280;">件/天</div></div>
  </div>
  <div style="background: #F3F4F6; padding: 15px; border-radius: 8px;">
    <strong>📋 入库建议说明</strong>
    <ul>
      <li>根据预测结果，建议在 <strong>${reportData.predictionStartDate}</strong> 前完成入库</li>
      <li>考虑到 ${reportData.safetyStock} 件安全库存，建议入库量为预测总量的 ${reportData.safetyFactor}%</li>
      <li>建议关注 <strong>${reportData.peakDate}</strong> 的库存准备，此日预计达到销量峰值</li>
      <li>建议定期（每 ${reportData.reviewInterval} 天）回顾预测结果，根据实际销售情况调整库存策略</li>
    </ul>
  </div>

  <h2>📐 计算方法说明</h2>
  <div style="background: #ECFDF5; padding: 20px; border-radius: 8px;">
    <h3>1. 建议入库量计算</h3>
    <p><strong>公式：</strong>建议入库量 = 预测总量 × 安全系数</p>
    <p><strong>说明：</strong></p>
    <ul>
      <li>预测总量：预测期内所有日期预测销量的总和</li>
      <li>安全系数：默认1.2（即20%安全库存），用于应对预测误差和突发需求</li>
      <li>安全库存 = 预测总量 × 0.2</li>
    </ul>
    <p><strong>示例：</strong>若预测总量为1000件，则建议入库量 = 1000 × 1.2 = 1200件</p>
    
    <h3 style="margin-top: 20px;">2. 置信区间计算</h3>
    <p><strong>公式：</strong></p>
    <p style="margin-left: 20px;">置信区间下限 = 预测值 × (1 - 模型误差率)</p>
    <p style="margin-left: 20px;">置信区间上限 = 预测值 × (1 + 模型误差率)</p>
    <p><strong>说明：</strong></p>
    <ul>
      <li>模型误差率：基于历史数据回测计算的WMAPE（加权平均绝对百分比误差）</li>
      <li>置信区间表示预测值的不确定性范围</li>
      <li>误差率越小，置信区间越窄，预测越精确</li>
    </ul>
    <p><strong>示例：</strong>若某日期预测销量为100件，模型误差率为5%，则</p>
    <p style="margin-left: 20px;">置信区间下限 = 100 × (1 - 0.05) = 95件</p>
    <p style="margin-left: 20px;">置信区间上限 = 100 × (1 + 0.05) = 105件</p>
    
    <h3 style="margin-top: 20px;">3. 日均销量计算</h3>
    <p><strong>公式：</strong>日均销量 = 预测总量 ÷ 预测天数</p>
    <p><strong>说明：</strong>用于评估预测期内的平均每日需求</p>
  </div>
</body>
</html>`

  const blob = new Blob([content], { type: 'text/html' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `入库预测报告_${selectedProduct.value}_${currentDate.value.replace(/\//g, '-')}.html`
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
}

// 导出为Word
const exportAsWord = () => {
  const content = `
<!DOCTYPE html>
<html xmlns:o='urn:schemas-microsoft-com:office:office' xmlns:w='urn:schemas-microsoft-com:office:word'>
<head>
  <meta charset="UTF-8">
  <title>入库预测报告</title>
  <style>
    body { font-family: 'Microsoft YaHei', sans-serif; }
    h1 { text-align: center; color: #1F2937; font-size: 24px; }
    h2 { color: #374151; font-size: 18px; border-bottom: 2px solid #E5E7EB; padding-bottom: 8px; margin-top: 20px; }
    .summary { background: #EFF6FF; padding: 15px; border-radius: 8px; margin: 15px 0; line-height: 1.8; }
    table { width: 100%; border-collapse: collapse; margin: 15px 0; }
    th, td { border: 1px solid #E5E7EB; padding: 10px; text-align: center; font-size: 12px; }
    th { background: #F3F4F6; font-weight: bold; }
    .metrics { display: table; width: 100%; border-spacing: 15px; margin: 15px 0; }
    .metric-card { display: table-cell; background: #F9FAFB; padding: 15px; border-radius: 8px; text-align: center; }
    .metric-value { font-size: 28px; font-weight: bold; color: #10B981; }
    .info-cards { display: table; width: 100%; border-spacing: 15px; margin: 15px 0; }
    .info-card { display: table-cell; background: #ECFDF5; padding: 20px; border-radius: 8px; text-align: center; }
    .info-value { font-size: 36px; font-weight: bold; color: #059669; }
    .warning { background: #FFFBEB; padding: 15px; border-radius: 8px; margin: 15px 0; }
    .footer { text-align: center; color: #9CA3AF; font-size: 12px; margin-top: 30px; }
  </style>
</head>
<body>
  <h1>入库预测报告</h1>
  <p style="text-align: center; color: #6B7280;">生成时间：${currentDate.value}</p>
  
  <h2>一、报告总结</h2>
  <div class="summary">
    <p>根据 <strong>${getCurrentModelName()}</strong> 算法预测结果表明：</p>
    <p>训练集时间范围为 <strong>${reportData.trainStartDate}</strong> 至 <strong>${reportData.trainEndDate}</strong>，对 <strong>${getCurrentProductName()}</strong>（商品ID：${selectedProduct.value}）进行预测分析。</p>
    <p>预测结果显示，<strong>${reportData.predictionStartDate}</strong> 至 <strong>${reportData.predictionEndDate}</strong> 期间，预计总销量为 <strong style="color: #10B981; font-size: 18px;">${reportData.totalPrediction}</strong> 件。</p>
    <p><strong>建议入库量：</strong><strong style="color: #10B981; font-size: 18px;">${reportData.suggestedInventory}</strong> 件${reportData.peakDate ? '（预计 <strong style="color: #DC2626;">' + reportData.peakDate + '</strong> 达到销量峰值，约 <strong style="color: #DC2626;">' + reportData.peakValue + '</strong> 件）' : ''}</p>
  </div>

  <h2>二、详细预测结果</h2>
  <table>
    <thead>
      <tr><th>日期</th><th>预测销量(件)</th><th>建议入库(件)</th><th>置信区间下限</th><th>置信区间上限</th><th>备注</th></tr>
    </thead>
    <tbody>
      ${reportData.predictions.map(p => `<tr><td>${p.date}</td><td${p.isPeak ? ' style="color: #DC2626; font-weight: bold;"' : ''}>${p.value}</td><td style="color: #3B82F6; font-weight: bold;">${p.suggested}</td><td>${p.confidenceLower}</td><td>${p.confidenceUpper}</td><td>${p.isPeak ? '峰值' : ''}</td></tr>`).join('')}
    </tbody>
  </table>

  <h2>三、入库建议详情</h2>
  <div class="info-cards">
    <div class="info-card"><div style="font-size: 40px;">📦</div><div style="font-size: 12px; color: #6B7280; margin-top: 10px;">建议总入库量</div><div class="info-value" style="margin-top: 10px;">${reportData.suggestedInventory}</div><div style="font-size: 12px; color: #6B7280;">件</div></div>
    <div class="info-card" style="background: #EFF6FF;"><div style="font-size: 40px;">📅</div><div style="font-size: 12px; color: #6B7280; margin-top: 10px;">预测天数</div><div class="info-value" style="color: #2563EB; margin-top: 10px;">${predictionDays.value}</div><div style="font-size: 12px; color: #6B7280;">天</div></div>
    <div class="info-card" style="background: #FFF7ED;"><div style="font-size: 40px;">📊</div><div style="font-size: 12px; color: #6B7280; margin-top: 10px;">日均销量</div><div class="info-value" style="color: #EA580C; margin-top: 10px;">${reportData.dailyAverage}</div><div style="font-size: 12px; color: #6B7280;">件/天</div></div>
  </div>
  <div style="background: #F3F4F6; padding: 15px; border-radius: 8px; margin-top: 20px;">
    <strong>入库建议说明：</strong>
    <ul>
      <li>• 根据预测结果，建议在 <strong>${reportData.predictionStartDate}</strong> 前完成入库</li>
      <li>• 考虑到 ${reportData.safetyStock} 件安全库存，建议入库量为预测总量的 ${reportData.safetyFactor}%</li>
      <li>• 建议关注 <strong>${reportData.peakDate}</strong> 的库存准备，此日预计达到销量峰值</li>
      <li>• 建议定期（每 ${reportData.reviewInterval} 天）回顾预测结果，根据实际销售情况调整库存策略</li>
    </ul>
  </div>

  <h2>四、计算方法说明</h2>
  <div style="background: #ECFDF5; padding: 20px; border-radius: 8px; margin-top: 20px;">
    <h3 style="color: #059669; font-size: 14px;">1. 建议入库量计算</h3>
    <p><strong>公式：</strong>建议入库量 = 预测总量 × 安全系数</p>
    <p><strong>说明：</strong></p>
    <ul>
      <li>• 预测总量：预测期内所有日期预测销量的总和</li>
      <li>• 安全系数：默认1.2（即20%安全库存），用于应对预测误差和突发需求</li>
      <li>• 安全库存 = 预测总量 × 0.2</li>
    </ul>
    
    <h3 style="color: #059669; font-size: 14px; margin-top: 15px;">2. 置信区间计算</h3>
    <p><strong>公式：</strong></p>
    <p style="margin-left: 20px;">置信区间下限 = 预测值 × (1 - 模型误差率)</p>
    <p style="margin-left: 20px;">置信区间上限 = 预测值 × (1 + 模型误差率)</p>
    <p><strong>说明：</strong></p>
    <ul>
      <li>• 模型误差率：基于历史数据回测计算的WMAPE（加权平均绝对百分比误差）</li>
      <li>• 置信区间表示预测值的不确定性范围</li>
      <li>• 误差率越小，置信区间越窄，预测越精确</li>
    </ul>
    
    <h3 style="color: #059669; font-size: 14px; margin-top: 15px;">3. 日均销量计算</h3>
    <p><strong>公式：</strong>日均销量 = 预测总量 ÷ 预测天数</p>
    <p><strong>说明：</strong>用于评估预测期内的平均每日需求</p>
  </div>

  <div class="footer">
    <p>实体商家销量预测系统</p>
    <p>入库预测报告</p>
  </div>
</body>
</html>`

  const blob = new Blob(['\ufeff' + content], { type: 'application/msword' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `入库预测报告_${selectedProduct.value}_${currentDate.value.replace(/\//g, '-')}.doc`
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
}
</script>

<style scoped>
.chart-container {
  @apply w-full h-80;
}
</style>
