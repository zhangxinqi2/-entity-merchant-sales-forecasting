<template>
  <div class="data-management">
    <!-- 页面标题 -->
    <header class="bg-gradient-to-r from-primary to-secondary text-white py-8 px-6">
      <div class="max-w-7xl mx-auto">
        <h1 class="text-3xl font-bold mb-2">数据管理</h1>
        <p class="text-white/80">新店家数据载入与旧店家数据更新</p>
      </div>
    </header>

    <main class="max-w-7xl mx-auto px-6 py-8">
      <!-- 选项卡切换 -->
      <div class="flex gap-4 mb-8">
        <button
          @click="activeTab = 'new-store'"
          class="px-6 py-3 rounded-lg font-semibold transition-all"
          :class="activeTab === 'new-store' ? 'bg-primary text-white shadow-lg' : 'bg-white text-gray-700 hover:bg-gray-50'"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 inline-block mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
          </svg>
          新店家数据载入
        </button>
        <button
          @click="activeTab = 'update-store'"
          class="px-6 py-3 rounded-lg font-semibold transition-all"
          :class="activeTab === 'update-store' ? 'bg-primary text-white shadow-lg' : 'bg-white text-gray-700 hover:bg-gray-50'"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 inline-block mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          旧店家数据更新
        </button>
      </div>

      <!-- 新店家数据载入 -->
      <div v-if="activeTab === 'new-store'" class="space-y-6">
        <!-- 表单 -->
        <div class="bg-white rounded-lg shadow-md p-6">
          <h2 class="text-xl font-semibold mb-6">📋 新店家信息录入</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">行业 <span class="text-red-500">*</span></label>
              <input
                v-model="newStoreForm.industry"
                type="text"
                placeholder="请输入行业名称"
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary"
              />
              <p class="text-xs text-gray-500 mt-1">参考行业: 烘焙行业、餐饮行业、茶饮行业</p>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">地址 <span class="text-red-500">*</span></label>
              <input
                v-model="newStoreForm.address"
                type="text"
                placeholder="请输入店铺地址"
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">商品名称 <span class="text-red-500">*</span></label>
              <input
                v-model="newStoreForm.productName"
                type="text"
                placeholder="请输入商品名称"
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">商品ID</label>
              <div class="w-full px-4 py-2 border border-gray-300 rounded-lg bg-gray-50">
                <span v-if="autoProductId" class="text-primary font-semibold">{{ autoProductId }}</span>
                <span v-else class="text-gray-400">请先选择行业</span>
              </div>
              <p class="text-xs text-gray-500 mt-1">编号规则: 每6个编号一组，同组行业一致</p>
            </div>
          </div>

          <!-- Excel文件上传 -->
          <div class="mt-6">
            <label class="block text-sm font-medium text-gray-700 mb-2">📊 Excel文件识别</label>
            <div class="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-primary transition-colors">
              <input
                type="file"
                accept=".xlsx,.xls"
                @change="handleFileUpload"
                class="hidden"
                id="excel-upload"
              />
              <label for="excel-upload" class="cursor-pointer">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 mx-auto text-gray-400 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                </svg>
                <p class="text-gray-600 mb-2">点击或拖拽上传Excel文件</p>
                <p class="text-sm text-gray-400">支持 .xlsx, .xls 格式</p>
              </label>
              <div v-if="uploadedFile" class="mt-4 text-green-600">
                ✅ 文件已上传: {{ uploadedFile.name }}
              </div>
            </div>
          </div>

          <!-- 提交按钮 -->
          <div class="mt-6 flex justify-end gap-4">
            <button
              @click="resetNewStoreForm"
              class="px-6 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
            >
              重置
            </button>
            <button
              @click="submitNewStore"
              :disabled="!validateNewStoreForm()"
              class="px-6 py-2 bg-primary text-white rounded-lg hover:bg-primary-dark transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 inline-block mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
              </svg>
              提交保存
            </button>
          </div>
        </div>

        <!-- 提示信息 -->
        <div class="bg-blue-50 rounded-lg p-4">
          <h3 class="font-semibold text-blue-800 mb-2">📌 编号规则说明</h3>
          <ul class="text-sm text-blue-700 space-y-1">
            <li>• 商品ID格式: 三位数字_两位数字（如 001_01）</li>
            <li>• 每6个编号为一组（如 001_01 至 001_06）</li>
            <li>• 同一组编号的商品行业必须一致</li>
            <li>• 当前最大编号组: {{ maxGroupId }}</li>
            <li>• 建议新店家从 {{ nextGroupId }}_01 开始编号</li>
          </ul>
        </div>

        <!-- 提交成功提示 -->
        <div v-if="newStoreSuccess" class="bg-green-50 rounded-lg p-4 border border-green-200">
          <div class="flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-green-600 mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
            <div>
              <p class="font-semibold text-green-800">数据提交成功！</p>
              <p class="text-sm text-green-600">新商品 "{{ newStoreForm.productName }}" ({{ autoProductId }}) 已添加到本地演示数据。</p>
            </div>
          </div>
        </div>
      </div>

      <!-- 旧店家数据更新 -->
      <div v-if="activeTab === 'update-store'" class="space-y-6">
        <!-- 查询表单 -->
        <div class="bg-white rounded-lg shadow-md p-6">
          <h2 class="text-xl font-semibold mb-6">🔍 查询历史数据</h2>
          <div class="flex gap-4">
            <div class="flex-1 max-w-md">
              <label class="block text-sm font-medium text-gray-700 mb-2">商品ID <span class="text-red-500">*</span></label>
              <input
                v-model="updateStoreForm.productId"
                type="text"
                placeholder="请输入商品ID（如: 001_01）"
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary"
              />
            </div>
            <div class="flex items-center self-end">
              <button
                @click="searchProduct"
                :disabled="!updateStoreForm.productId"
                class="px-6 py-2 bg-primary text-white rounded-lg hover:bg-primary-dark transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 inline-block mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
                查询
              </button>
            </div>
          </div>
        </div>

        <!-- 历史数据展示 -->
        <div v-if="foundProduct" class="bg-white rounded-lg shadow-md p-6">
          <div class="flex justify-between items-center mb-6">
            <h2 class="text-xl font-semibold">📋 历史数据</h2>
            <button
              @click="toggleEditMode"
              class="px-4 py-2 rounded-lg transition-colors"
              :class="editMode ? 'bg-red-500 text-white' : 'bg-primary text-white'"
            >
              {{ editMode ? '取消编辑' : '编辑数据' }}
            </button>
          </div>

          <!-- 商品基本信息 -->
          <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6 p-4 bg-gray-50 rounded-lg">
            <div>
              <span class="text-sm text-gray-500">商品ID</span>
              <p class="font-semibold">{{ foundProduct.product_id }}</p>
            </div>
            <div>
              <span class="text-sm text-gray-500">商品名称</span>
              <p class="font-semibold">{{ foundProduct.product_name }}</p>
            </div>
            <div>
              <span class="text-sm text-gray-500">行业</span>
              <p class="font-semibold">{{ foundProduct.industry }}</p>
            </div>
            <div>
              <span class="text-sm text-gray-500">地址</span>
              <p class="font-semibold">{{ foundProduct.address }}</p>
            </div>
          </div>

          <!-- 数据表格 -->
          <div class="table-container max-h-96 overflow-y-auto">
            <table class="data-table">
              <thead>
                <tr>
                  <th>日期</th>
                  <th>销量</th>
                  <th>日平均气温(°C)</th>
                  <th>平均售价(¥)</th>
                  <th>节假日</th>
                  <th>打折</th>
                  <th v-if="editMode">操作</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(row, index) in foundProduct.data" :key="index">
                  <td>{{ row.date }}</td>
                  <td>
                    <input
                      v-if="editMode"
                      v-model.number="row.sales"
                      type="number"
                      class="w-full px-2 py-1 border border-gray-300 rounded text-center"
                    />
                    <span v-else>{{ row.sales }}</span>
                  </td>
                  <td>
                    <input
                      v-if="editMode"
                      v-model.number="row.temperature"
                      type="number"
                      step="0.1"
                      class="w-full px-2 py-1 border border-gray-300 rounded text-center"
                    />
                    <span v-else>{{ row.temperature }}</span>
                  </td>
                  <td>
                    <input
                      v-if="editMode"
                      v-model.number="row.price"
                      type="number"
                      step="0.01"
                      class="w-full px-2 py-1 border border-gray-300 rounded text-center"
                    />
                    <span v-else>{{ row.price }}</span>
                  </td>
                  <td>
                    <select
                      v-if="editMode"
                      v-model="row.holiday"
                      class="w-full px-2 py-1 border border-gray-300 rounded text-center text-sm"
                    >
                      <option value="是">是</option>
                      <option value="否">否</option>
                    </select>
                    <span v-else>{{ row.holiday }}</span>
                  </td>
                  <td>
                    <select
                      v-if="editMode"
                      v-model="row.discount"
                      class="w-full px-2 py-1 border border-gray-300 rounded text-center text-sm"
                    >
                      <option value="是">是</option>
                      <option value="否">否</option>
                    </select>
                    <span v-else>{{ row.discount }}</span>
                  </td>
                  <td v-if="editMode">
                    <button
                      @click="removeRow(index)"
                      class="text-red-500 hover:text-red-700"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                      </svg>
                    </button>
                  </td>
                </tr>
                <!-- 添加新行 -->
                <tr v-if="editMode">
                  <td>
                    <input
                      v-model="newRow.date"
                      type="date"
                      class="w-full px-2 py-1 border border-gray-300 rounded text-center"
                    />
                  </td>
                  <td>
                    <input
                      v-model.number="newRow.sales"
                      type="number"
                      placeholder="销量"
                      class="w-full px-2 py-1 border border-gray-300 rounded text-center"
                    />
                  </td>
                  <td>
                    <input
                      v-model.number="newRow.temperature"
                      type="number"
                      step="0.1"
                      placeholder="气温"
                      class="w-full px-2 py-1 border border-gray-300 rounded text-center"
                    />
                  </td>
                  <td>
                    <input
                      v-model.number="newRow.price"
                      type="number"
                      step="0.01"
                      placeholder="售价"
                      class="w-full px-2 py-1 border border-gray-300 rounded text-center"
                    />
                  </td>
                  <td>
                    <select
                      v-model="newRow.holiday"
                      class="w-full px-2 py-1 border border-gray-300 rounded text-center text-sm"
                    >
                      <option value="否">否</option>
                      <option value="是">是</option>
                    </select>
                  </td>
                  <td>
                    <select
                      v-model="newRow.discount"
                      class="w-full px-2 py-1 border border-gray-300 rounded text-center text-sm"
                    >
                      <option value="否">否</option>
                      <option value="是">是</option>
                    </select>
                  </td>
                  <td>
                    <button
                      @click="addRow"
                      class="text-green-500 hover:text-green-700"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                      </svg>
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- 保存按钮 -->
          <div v-if="editMode" class="mt-6 flex justify-end">
            <button
              @click="saveUpdatedData"
              class="px-6 py-2 bg-primary text-white rounded-lg hover:bg-primary-dark transition-colors"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 inline-block mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3 3m0 0l-3-3m3 3V4" />
              </svg>
              保存更新
            </button>
          </div>
        </div>

        <!-- 未找到提示 -->
        <div v-if="searchError" class="bg-red-50 rounded-lg p-4 border border-red-200">
          <div class="flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-red-600 mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <p class="text-red-800">未找到商品ID为 "{{ updateStoreForm.productId }}" 的数据，请检查输入是否正确。</p>
          </div>
        </div>

        <!-- 更新成功提示 -->
        <div v-if="updateSuccess" class="bg-green-50 rounded-lg p-4 border border-green-200">
          <div class="flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-green-600 mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
            <div>
              <p class="font-semibold text-green-800">数据更新成功！</p>
              <p class="text-sm text-green-600">商品 "{{ foundProduct.product_name }}" 的数据已更新。</p>
            </div>
          </div>
        </div>
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
import { products } from '@/data/products'

// 选项卡状态
const activeTab = ref('new-store')

// 新店家表单
const newStoreForm = reactive({
  industry: '',
  address: '',
  productName: '',
  productId: ''
})

const uploadedFile = ref(null)
const newStoreSuccess = ref(false)

// 旧店家表单
const updateStoreForm = reactive({
  productId: ''
})

const foundProduct = ref(null)
const editMode = ref(false)
const searchError = ref(false)
const updateSuccess = ref(false)

// 新行数据
const newRow = reactive({
  date: '',
  sales: '',
  temperature: '',
  price: '',
  holiday: '否',
  discount: '否'
})

// 根据行业计算下一个可用的商品ID
const autoProductId = computed(() => {
  if (!newStoreForm.industry) return ''
  
  // 获取该行业现有的所有商品ID
  const industryProducts = products.filter(p => p.industry === newStoreForm.industry)
  
  if (industryProducts.length === 0) {
    // 如果该行业还没有商品，从下一个可用的编号组开始
    const allGroups = products.map(p => p.product_id.split('_')[0])
    const maxGroup = allGroups.length > 0 ? Math.max(...allGroups.map(g => parseInt(g))) : 0
    const nextGroup = String(maxGroup + 1).padStart(3, '0')
    return `${nextGroup}_01`
  }
  
  // 提取该行业的所有编号组
  const groups = industryProducts.map(p => p.product_id.split('_')[0])
  const uniqueGroups = [...new Set(groups)]
  uniqueGroups.sort()
  
  const lastGroup = uniqueGroups[uniqueGroups.length - 1]
  const productsInLastGroup = industryProducts.filter(p => p.product_id.startsWith(lastGroup + '_'))
  
  if (productsInLastGroup.length < 6) {
    // 当前组还没满6个，继续添加
    const nextNumber = String(productsInLastGroup.length + 1).padStart(2, '0')
    return `${lastGroup}_${nextNumber}`
  } else {
    // 当前组已满，创建新组
    const nextGroup = String(parseInt(lastGroup) + 1).padStart(3, '0')
    return `${nextGroup}_01`
  }
})

// 计算最大编号组（用于提示信息）
const maxGroupId = computed(() => {
  const groups = products.map(p => p.product_id.split('_')[0])
  const uniqueGroups = [...new Set(groups)]
  return uniqueGroups.sort().pop() || '000'
})

const nextGroupId = computed(() => {
  const current = parseInt(maxGroupId.value) + 1
  return String(current).padStart(3, '0')
})

// 新店家表单验证
const validateNewStoreForm = () => {
  return newStoreForm.industry && 
         newStoreForm.address && 
         newStoreForm.productName &&
         autoProductId.value
}

// 处理文件上传
const handleFileUpload = (event) => {
  const file = event.target.files[0]
  if (file) {
    uploadedFile.value = file
  }
}

// 重置新店家表单
const resetNewStoreForm = () => {
  newStoreForm.industry = ''
  newStoreForm.address = ''
  newStoreForm.productName = ''
  uploadedFile.value = null
  newStoreSuccess.value = false
}

// 提交新店家数据
const submitNewStore = () => {
  if (!validateNewStoreForm()) return
  
  // 模拟保存数据（使用自动生成的商品ID）
  const submitData = {
    ...newStoreForm,
    productId: autoProductId.value
  }
  console.log('提交新店家数据:', submitData)
  
  newStoreSuccess.value = true
  
  setTimeout(() => {
    resetNewStoreForm()
  }, 3000)
}

// 搜索商品
const searchProduct = () => {
  const productId = updateStoreForm.productId.trim()
  if (!productId) return
  
  searchError.value = false
  updateSuccess.value = false
  
  // 查找商品
  const product = products.find(p => p.product_id === productId)
  
  if (product) {
    // 生成模拟历史数据
    const startDate = new Date('2025-01-01')
    const data = []
    for (let i = 0; i < 10; i++) {
      const date = new Date(startDate)
      date.setDate(date.getDate() + i)
      data.push({
        date: date.toISOString().split('T')[0],
        sales: Math.round(80 + Math.random() * 60),
        temperature: Math.round((15 + Math.random() * 10) * 10) / 10,
        price: Math.round((8 + Math.random() * 6) * 100) / 100,
        holiday: Math.random() > 0.8 ? '是' : '否',
        discount: Math.random() > 0.7 ? '是' : '否'
      })
    }
    
    foundProduct.value = {
      ...product,
      data: data
    }
    editMode.value = false
  } else {
    foundProduct.value = null
    searchError.value = true
  }
}

// 切换编辑模式
const toggleEditMode = () => {
  editMode.value = !editMode.value
  if (!editMode.value) {
    // 重置新行
    newRow.date = ''
    newRow.sales = ''
    newRow.temperature = ''
    newRow.price = ''
    newRow.holiday = '否'
    newRow.discount = '否'
  }
}

// 添加新行
const addRow = () => {
  if (!newRow.date || !newRow.sales || !newRow.temperature || !newRow.price) {
    alert('请填写完整的新行数据')
    return
  }
  
  foundProduct.value.data.push({
    date: newRow.date,
    sales: Number(newRow.sales),
    temperature: Number(newRow.temperature),
    price: Number(newRow.price),
    holiday: newRow.holiday,
    discount: newRow.discount
  })
  
  // 重置新行
  newRow.date = ''
  newRow.sales = ''
  newRow.temperature = ''
  newRow.price = ''
  newRow.holiday = '否'
  newRow.discount = '否'
}

// 删除行
const removeRow = (index) => {
  foundProduct.value.data.splice(index, 1)
}

// 保存更新数据
const saveUpdatedData = () => {
  console.log('保存更新数据:', foundProduct.value)
  updateSuccess.value = true
  editMode.value = false
  
  setTimeout(() => {
    updateSuccess.value = false
  }, 3000)
}
</script>

<style scoped>
.table-container {
  @apply overflow-x-auto;
}
</style>
