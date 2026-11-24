<template>
  <div class="dashboard">
    <!-- 页面标题 -->
    <header class="bg-gradient-to-r from-primary to-secondary text-white py-8 px-6">
      <div class="max-w-7xl mx-auto">
        <h1 class="text-3xl font-bold mb-2">实体商家销量预测系统</h1>
        <p class="text-white/80">基于多模型融合的智能销量预测分析平台</p>
      </div>
    </header>

    <main class="max-w-7xl mx-auto px-6 py-8">
      <!-- 商品信息表格 -->
      <section class="section">
        <h2>📦 商品列表（48个商品）</h2>
        <div class="table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th>商品编码</th>
                <th>行业</th>
                <th>商品名称</th>
                <th>店铺地址</th>
                <th>操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="product in products" :key="product.product_id">
                <td class="font-mono">{{ product.product_id }}</td>
                <td>
                  <span 
                    class="px-2 py-1 rounded-full text-xs font-medium"
                    :class="getIndustryClass(product.industry)"
                  >
                    {{ product.industry }}
                  </span>
                </td>
                <td>{{ product.product_name }}</td>
                <td class="max-w-xs truncate" :title="product.address">{{ product.address }}</td>
                <td>
                  <button 
                    @click="viewProduct(product.product_id)" 
                    class="btn btn-primary btn-sm"
                  >
                    查看详情
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <!-- 行业热力图 -->
      <section class="section">
        <h2>🔥 行业销量与气温相关性热力图</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div v-for="industry in industries" :key="industry.name" class="card" :style="{ borderColor: industry.borderColor }">
            <h3 class="text-lg font-semibold mb-3">{{ industry.name }} ({{ industry.product_count }}个商品)</h3>
            <div class="chart-container-small">
              <v-chart :option="getHeatmapOption(industry)" autoresize />
            </div>
            <p class="text-sm text-gray-600 mt-3">{{ industry.description }}</p>
          </div>
        </div>
      </section>

      <!-- 行业箱线图 -->
      <section class="section">
        <h2>📊 行业销量分布箱线图</h2>
        <div v-for="industry in industries" :key="industry.name" class="mb-6">
          <h3 class="text-lg font-semibold mb-3">{{ industry.name }}</h3>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div class="card" :style="{ borderColor: industry.borderColor, backgroundColor: industry.bgColor }">
              <h4 class="text-sm font-medium text-gray-700 mb-2">商品对数平均销量对比</h4>
              <div class="aspect-video bg-white rounded-lg overflow-hidden">
                <img 
                  :src="industry.salesImage" 
                  :alt="industry.name + '销量箱线图'"
                  class="w-full h-full object-contain"
                  @error="handleImageError($event, industry)"
                />
              </div>
            </div>
            <div class="card" :style="{ borderColor: industry.borderColor, backgroundColor: industry.bgColor }">
              <h4 class="text-sm font-medium text-gray-700 mb-2">节假日和打折对比</h4>
              <div class="aspect-video bg-white rounded-lg overflow-hidden">
                <img 
                  :src="industry.holidayImage" 
                  :alt="industry.name + '节假日箱线图'"
                  class="w-full h-full object-contain"
                  @error="handleImageError($event, industry)"
                />
              </div>
            </div>
          </div>
          <div class="mt-3 p-3 rounded-lg" :style="{ backgroundColor: industry.hintBgColor }">
            <p class="text-sm" :style="{ color: industry.hintTextColor }">
              <strong>分析结论：</strong>{{ getBoxplotAnalysis(industry.name) }}
            </p>
          </div>
        </div>
      </section>

      <!-- 工作簿选择按钮区 -->
      <section class="section">
        <h2>⚡ 快速选择商品工作簿</h2>
        <div class="flex flex-wrap gap-2">
          <button 
            v-for="product in products" 
            :key="product.product_id"
            @click="viewProduct(product.product_id)"
            class="workbook-btn px-4 py-2 bg-gray-100 hover:bg-primary hover:text-white rounded-lg transition-colors text-sm font-medium"
            :class="getIndustryBtnClass(product.industry)"
          >
            {{ product.product_id }}
          </button>
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
import { useRouter } from 'vue-router'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { HeatmapChart } from 'echarts/charts'
import { TitleComponent, TooltipComponent, LegendComponent, GridComponent, VisualMapComponent } from 'echarts/components'
import { products } from '@/data/products'

use([CanvasRenderer, HeatmapChart, TitleComponent, TooltipComponent, LegendComponent, GridComponent, VisualMapComponent])

const router = useRouter()

// 行业信息 - 使用指定的颜色方案
const industries = [
  {
    name: '烘焙行业',
    product_count: 18,
    salesImage: `${import.meta.env.BASE_URL}images/boxplots/bakery_sales.png`,
    holidayImage: `${import.meta.env.BASE_URL}images/boxplots/bakery_holiday.png`,
    borderColor: 'rgb(160, 208, 208)',
    bgColor: 'rgba(160, 208, 208, 0.1)',
    hintBgColor: 'rgba(160, 208, 208, 0.2)',
    hintTextColor: '#1f2937',
    description: '合成示例：烘焙商品销量相对稳定，受节假日影响较大。黄油可颂、海盐卷等示例商品表现突出，周末销量高于工作日。'
  },
  {
    name: '餐饮行业',
    product_count: 18,
    salesImage: `${import.meta.env.BASE_URL}images/boxplots/catering_sales.png`,
    holidayImage: `${import.meta.env.BASE_URL}images/boxplots/catering_holiday.png`,
    borderColor: 'rgb(183, 245, 222)',
    bgColor: 'rgba(183, 245, 222, 0.1)',
    hintBgColor: 'rgba(183, 245, 222, 0.2)',
    hintTextColor: '#1f2937',
    description: '合成示例：餐饮商品销量波动较大，午晚高峰明显。番茄鸡蛋面、鲜肉小笼包等示例商品在午餐时段销量较高。'
  },
  {
    name: '茶饮行业',
    product_count: 12,
    salesImage: `${import.meta.env.BASE_URL}images/boxplots/tea_sales.png`,
    holidayImage: `${import.meta.env.BASE_URL}images/boxplots/tea_holiday.png`,
    borderColor: 'rgb(167, 192, 223)',
    bgColor: 'rgba(167, 192, 223, 0.1)',
    hintBgColor: 'rgba(167, 192, 223, 0.2)',
    hintTextColor: '#1f2937',
    description: '合成示例：茶饮商品季节性明显，茉莉奶绿、桂花乌龙等示例饮品在下午茶时段销量较高。'
  }
]

const viewProduct = (productId) => {
  router.push(`/product/${productId}`)
}

const getIndustryClass = (industry) => {
  switch (industry) {
    case '烘焙行业':
      return 'bg-[rgb(160,208,208)] text-gray-800'
    case '餐饮行业':
      return 'bg-[rgb(183,245,222)] text-gray-800'
    case '茶饮行业':
      return 'bg-[rgb(167,192,223)] text-gray-800'
    default:
      return 'bg-gray-100 text-gray-800'
  }
}

const getIndustryBtnClass = (industry) => {
  switch (industry) {
    case '烘焙行业':
      return 'hover:bg-[rgb(160,208,208)] hover:text-gray-800'
    case '餐饮行业':
      return 'hover:bg-[rgb(183,245,222)] hover:text-gray-800'
    case '茶饮行业':
      return 'hover:bg-[rgb(167,192,223)] hover:text-gray-800'
    default:
      return ''
  }
}

const getBoxplotAnalysis = (industry) => {
  switch (industry) {
    case '烘焙行业':
      return '合成示例：不同烘焙商品的销量差异较大，节假日促销对销量有明显提升作用。'
    case '餐饮行业':
      return '合成示例：餐饮商品整体销量较为均衡，套餐类商品波动较大，节假日期间销量上升。'
    case '茶饮行业':
      return '合成示例：茶饮商品销量分布相对集中，周末销量高于工作日。'
    default:
      return ''
  }
}

const handleImageError = (event, industry) => {
  const target = event.target
  target.src = `data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="400" height="300" viewBox="0 0 400 300"%3E%3Crect fill="${industry.bgColor.replace('rgba', 'rgb').replace('0.1', '0.2')}" width="400" height="300"/%3E%3Ctext fill="%239ca3af" font-family="sans-serif" font-size="14" x="50%25" y="50%25" text-anchor="middle" dominant-baseline="middle"%3E图片加载失败%3C/text%3E%3C/svg%3E`
}

// 生成热力图数据
const generateHeatmapData = (seed) => {
  const data = []
  for (let i = 0; i < 12; i++) {
    for (let j = 0; j < 8; j++) {
      const value = Math.sin((i + seed) * 0.5) * 30 + Math.cos((j + seed) * 0.3) * 20 + Math.random() * 20
      data.push([i, j, Math.round(value)])
    }
  }
  return data
}

// 获取热力图配置
const getHeatmapOption = (industry) => {
  return {
    title: {
      text: `${industry.name} - 销量与气温相关性`,
      left: 'center',
      textStyle: {
        fontSize: 12,
        fontWeight: 'normal'
      }
    },
    tooltip: {
      position: 'top',
      formatter: function(params) {
        return `指标: ${params.data[0]}-${params.data[1]}<br/>相关性: ${params.data[2]}`
      }
    },
    grid: {
      left: '10%',
      right: '10%',
      bottom: '15%',
      top: '20%'
    },
    xAxis: {
      type: 'category',
      data: ['商品1', '商品2', '商品3', '商品4', '商品5', '商品6', '商品7', '商品8', '商品9', '商品10', '商品11', '商品12'],
      splitArea: {
        show: true
      },
      axisLabel: {
        fontSize: 8
      }
    },
    yAxis: {
      type: 'category',
      data: ['气温1', '气温2', '气温3', '气温4', '气温5', '气温6', '气温7', '气温8'],
      splitArea: {
        show: true
      },
      axisLabel: {
        fontSize: 8
      }
    },
    visualMap: {
      min: -20,
      max: 80,
      calculable: true,
      orient: 'horizontal',
      left: 'center',
      bottom: '0%',
      inRange: {
        color: ['#3CB371', '#4CAF50', '#66BB6A', '#81C784', '#A5D6A7', '#C8E6C9', '#E8F5E9']
      }
    },
    series: [{
      name: '相关性',
      type: 'heatmap',
      data: generateHeatmapData(industries.indexOf(industry)),
      label: {
        show: false
      },
      emphasis: {
        itemStyle: {
          shadowBlur: 10,
          shadowColor: 'rgba(0, 0, 0, 0.5)'
        }
      }
    }]
  }
}
</script>

<style scoped>
.workbook-btn {
  min-width: 80px;
}

.chart-container-small {
  @apply w-full h-48;
}
</style>
