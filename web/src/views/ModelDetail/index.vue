<template>
  <div class="model-detail">
    <!-- 页面标题 -->
    <header class="bg-gradient-to-r from-primary to-secondary text-white py-8 px-6">
      <div class="max-w-7xl mx-auto">
        <h1 class="text-3xl font-bold mb-2">模型预测详情</h1>
        <p class="text-white/80">查看各模型对商品的预测结果和误差分析</p>
      </div>
    </header>

    <main class="max-w-7xl mx-auto px-6 py-8">
      <!-- 筛选区域 -->
      <div class="bg-white rounded-lg shadow-md p-6 mb-6">
        <div class="flex flex-wrap gap-6 items-center">
          <div class="flex-1 min-w-[200px]">
            <label class="block text-sm font-medium text-gray-700 mb-2">选择模型</label>
            <select 
              v-model="selectedModel" 
              @change="loadPredictionData"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary"
            >
              <option v-for="model in models" :key="model.id" :value="model.id">
                {{ model.name }} (排名: {{ model.ranking }})
              </option>
            </select>
          </div>
          <div class="flex-1 min-w-[200px]">
            <label class="block text-sm font-medium text-gray-700 mb-2">选择商品</label>
            <select 
              v-model="selectedProduct" 
              @change="loadPredictionData"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary"
            >
              <option v-for="product in products" :key="product.product_id" :value="product.product_id">
                {{ product.product_name }} ({{ product.product_id }})
              </option>
            </select>
          </div>
          <div class="flex items-center gap-4">
            <button @click="loadPredictionData" class="btn btn-primary">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 inline-block mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
              执行预测
            </button>
          </div>
        </div>
      </div>

      <!-- 加载状态 -->
      <div v-if="loading" class="flex justify-center items-center h-64">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
      </div>

      <template v-else>
        <!-- 模型信息卡片 -->
        <section class="section">
          <h2>📋 当前模型信息</h2>
          <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div class="info-card">
              <span class="label">模型名称</span>
              <span class="value font-semibold">{{ currentModel.name }}</span>
            </div>
            <div class="info-card">
              <span class="label">发布单位</span>
              <span class="value">{{ currentModel.company }}</span>
            </div>
            <div class="info-card">
              <span class="label">综合排名</span>
              <span class="value">第 {{ currentModel.ranking }} 名</span>
            </div>
            <div class="info-card">
              <span class="label">当前商品</span>
              <span class="value">{{ currentProduct.product_name }}</span>
            </div>
          </div>
          <p class="mt-4 p-4 bg-blue-50 rounded-lg text-blue-800">{{ currentModel.description }}</p>
        </section>

        <!-- 误差检验指标 -->
        <section class="section">
          <h2>📈 模型误差检验</h2>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div class="stat-card" :class="getErrorClass(predictionData.error_metrics?.wmape)">
              <div class="stat-icon">🎯</div>
              <div class="stat-info">
                <span class="stat-label">WMAPE (加权平均绝对百分比误差)</span>
                <span class="stat-value">{{ predictionData.error_metrics?.wmape != null ? (predictionData.error_metrics.wmape * 100).toFixed(2) : 'N/A' }}%</span>
              </div>
            </div>
            <div class="stat-card" :class="getErrorClass(predictionData.error_metrics?.mape)">
              <div class="stat-icon">📊</div>
              <div class="stat-info">
                <span class="stat-label">MAPE (平均绝对百分比误差)</span>
                <span class="stat-value">{{ predictionData.error_metrics?.mape != null ? (predictionData.error_metrics.mape * 100).toFixed(2) : 'N/A' }}%</span>
              </div>
            </div>
            <div class="stat-card" :class="getErrorClass(predictionData.error_metrics?.smape)">
              <div class="stat-icon">📉</div>
              <div class="stat-info">
                <span class="stat-label">SMAPE (对称平均绝对百分比误差)</span>
                <span class="stat-value">{{ predictionData.error_metrics?.smape != null ? (predictionData.error_metrics.smape * 100).toFixed(2) : 'N/A' }}%</span>
              </div>
            </div>
          </div>
        </section>

        <!-- 测试集预测值与真实值时序图 -->
        <section class="section">
          <h2>📊 测试集预测值与真实值对比</h2>
          <div class="chart-container">
            <v-chart :option="comparisonChartOption" autoresize />
          </div>
        </section>

        <!-- 未来7天销量预测图 -->
        <section class="section">
          <h2>🔮 原始数据与未来7天销量预测</h2>
          <div class="chart-container">
            <v-chart :option="predictionChartOption" autoresize />
          </div>
        </section>

        <!-- 未来7天预测数据表格 -->
        <section class="section">
          <h2>📁 未来7天预测详情</h2>
          <div class="table-container">
            <table class="data-table">
              <thead>
                <tr>
                  <th>日期</th>
                  <th>预测销量(件)</th>
                  <th>置信度(%)</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(pred, index) in predictionData.predictions" :key="index">
                  <td>{{ pred.date }}</td>
                  <td class="font-semibold text-primary">{{ pred.predicted_sales }}</td>
                  <td>
                    <div class="flex items-center gap-2">
                      <div class="w-24 h-2 bg-gray-200 rounded-full overflow-hidden">
                        <div 
                          class="h-full bg-green-500 transition-all" 
                          :style="{ width: pred.confidence + '%' }"
                        ></div>
                      </div>
                      <span>{{ pred.confidence }}%</span>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
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

<script setup>import { ref, computed, onMounted } from 'vue';
import VChart from 'vue-echarts';
import { use } from 'echarts/core';
import { CanvasRenderer } from 'echarts/renderers';
import { LineChart } from 'echarts/charts';
import { TitleComponent, TooltipComponent, LegendComponent, GridComponent } from 'echarts/components';
import { models } from '@/data/models';
import { products } from '@/data/products';
import { generateFullPredictionData } from '@/data/salesData';
use([
 CanvasRenderer,
 LineChart,
 TitleComponent,
 TooltipComponent,
 LegendComponent,
 GridComponent
]);
const selectedModel = ref('timefm2.5');
const selectedProduct = ref('001_01');
const loading = ref(true);
const predictionData = ref({});
const currentModel = computed(() => {
 return models.find(m => m.id === selectedModel.value) || models[0];
});
const currentProduct = computed(() => {
 return products.find(p => p.product_id === selectedProduct.value) || products[0];
});
const loadPredictionData = () => {
 loading.value = true;
 setTimeout(() => {
 predictionData.value = generateFullPredictionData(selectedModel.value, selectedProduct.value);
 loading.value = false;
 }, 500);
};
const comparisonChartOption = computed(() => {
 const last30Days = predictionData.value.time_series?.slice(-30) || [];
 const dates = last30Days.map(t => t.date);
 const actual = last30Days.map(t => t.sales);
 const predicted = last30Days.map(t => t.predicted);
 return {
 title: {
 text: `${currentModel.value.name} - 测试集真实值与预测值对比`,
 left: 'center'
 },
 tooltip: {
 trigger: 'axis'
 },
 legend: {
 data: ['真实销量', '预测销量'],
 top: 30
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
 name: '真实销量',
 type: 'line',
 smooth: true,
 data: actual,
 lineStyle: {
 color: '#4CAF50',
 width: 2
 },
 itemStyle: {
 color: '#4CAF50'
 }
 },
 {
 name: '预测销量',
 type: 'line',
 smooth: true,
 data: predicted,
 lineStyle: {
 color: '#FF9800',
 width: 2,
 type: 'dashed'
 },
 itemStyle: {
 color: '#FF9800'
 }
 }
 ]
 };
});
const predictionChartOption = computed(() => {
 const timeSeries = predictionData.value.time_series || [];
 const predictions = predictionData.value.predictions || [];
 const allDates = [...timeSeries.map(t => t.date), ...predictions.map(p => p.date)];
 const allSales = [...timeSeries.map(t => t.sales), ...Array(predictions.length).fill(null)];
 const predictedSales = [...Array(timeSeries.length).fill(null), ...predictions.map(p => p.predicted_sales)];
 return {
 title: {
 text: `${currentModel.value.name} - 历史数据与未来7天预测`,
 left: 'center'
 },
 tooltip: {
 trigger: 'axis'
 },
 legend: {
 data: ['历史销量', '预测销量'],
 top: 30
 },
 grid: {
 left: '3%',
 right: '4%',
 bottom: '3%',
 containLabel: true
 },
 xAxis: {
 type: 'category',
 data: allDates,
 axisLabel: {
 rotate: 45,
 fontSize: 8
 },
 splitLine: {
 show: true,
 lineStyle: {
 color: ['transparent', 'transparent', '#FF9800'],
 width: [0, 0, 2],
 type: ['solid', 'solid', 'dashed']
 }
 }
 },
 yAxis: {
 type: 'value',
 name: '销量(件)'
 },
 series: [
 {
 name: '历史销量',
 type: 'line',
 smooth: true,
 data: allSales,
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
 },
 {
 name: '预测销量',
 type: 'line',
 smooth: true,
 data: predictedSales,
 lineStyle: {
 color: '#FF9800',
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
 { offset: 0, color: 'rgba(255, 152, 0, 0.3)' },
 { offset: 1, color: 'rgba(255, 152, 0, 0.05)' }
 ]
 }
 },
 markLine: {
 silent: true,
 symbol: 'none',
 lineStyle: {
 color: '#FF9800',
 type: 'dashed',
 width: 2
 },
 data: [{
 yAxis: 0,
 lineStyle: {
 type: 'dashed'
 }
 }]
 }
 }
 ],
 graphic: [
 {
 type: 'text',
 left: 'center',
 bottom: 40,
 style: {
 text: '预测区域',
 fill: '#FF9800',
 fontSize: 12
 }
 }
 ]
 };
});
const getErrorClass = (value) => {
 if (value < 0.2)
 return 'border-green-200 bg-green-50';
 if (value < 0.25)
 return 'border-yellow-200 bg-yellow-50';
 return 'border-red-200 bg-red-50';
};
onMounted(() => {
 loadPredictionData();
});
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
  @apply rounded-lg p-4 flex items-center gap-4 border;
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

.chart-container {
  @apply w-full h-96;
}
</style>
