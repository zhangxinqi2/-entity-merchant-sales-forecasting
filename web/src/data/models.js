// 模型对比结果：来自作者在原比赛数据上的聚合评测（不含任何商家级明细）。
export const models = [
  {
    id: 'elpa',
    name: 'ELPA',
    description: '集成学习预测算法框架，结合SMA、LR、RF、GBDT模型，表现最优。',
    company: '综合方法',
    ranking: 1,
    wmape: 17.56
  },
  {
    id: 'xgboost',
    name: 'XGBoost',
    description: '极端梯度提升树模型，高性能的梯度提升框架。',
    company: 'DMLC',
    ranking: 2,
    wmape: 18.44
  },
  {
    id: 'xgboost-rf',
    name: 'XGBoost+RF',
    description: 'XGBoost与随机森林的集成模型，结合了梯度提升和随机森林的优势。',
    company: '综合方法',
    ranking: 3,
    wmape: 18.61
  },
  {
    id: 'catboost',
    name: 'CatBoost',
    description: 'Yandex开发的梯度提升算法，自动处理类别特征，内置正则化。',
    company: 'Yandex',
    ranking: 4,
    wmape: 19.64
  },
  {
    id: 'timehf-pctlm',
    name: 'TimeHF-PCTLM',
    description: '结合Transformer和卷积的时间序列预测框架，包含Patch Convolution Layer。',
    company: '学术界',
    ranking: 5,
    wmape: 37.85
  },
  {
    id: 'timefm2.5',
    name: 'TimeFM 2.5',
    description: '基于频率调制的时序预测模型，结合了傅里叶分析和深度学习技术。',
    company: '微软',
    ranking: 6,
    wmape: 39.76
  },
  {
    id: 'sarima',
    name: 'SARIMA',
    description: '季节性自回归综合移动平均模型，经典的统计时序预测方法。',
    company: '统计领域经典方法',
    ranking: 7,
    wmape: 24.94
  },
  {
    id: 'tirex',
    name: 'TiRex',
    description: '时间序列正则化表达模型，结合了正则化和深度学习技术。',
    company: '学术界',
    ranking: 8,
    wmape: 29.94
  },
  {
    id: 'chronos',
    name: 'Chronos',
    description: '亚马逊公司发布的大语言模型时序预测框架。',
    company: '亚马逊',
    ranking: 9,
    wmape: 31.17
  },
  {
    id: 'lstm',
    name: 'LSTM',
    description: '长短期记忆网络，深度学习领域经典的时序预测模型。',
    company: '学术界',
    ranking: 10,
    wmape: 32.00
  },
  {
    id: 'lag-llama',
    name: 'Lag-Llama',
    description: '基于Llama架构的时序预测模型，利用注意力机制捕捉时序依赖。',
    company: 'Meta',
    ranking: 11,
    wmape: 32.26
  },
  {
    id: 'extratrees',
    name: 'ExtraTrees',
    description: '极端随机树集成模型，基于决策树的集成学习方法。',
    company: '学术界',
    ranking: 12,
    wmape: 32.92
  },
  {
    id: 'patchtst',
    name: 'PatchTST',
    description: '基于Patch的时序Transformer模型，将时序数据分割为patch进行处理。',
    company: '学术界',
    ranking: 13,
    wmape: 33.07
  },
  {
    id: 'timegpt-1',
    name: 'TimeGPT-1',
    description: 'Salesforce发布的大语言模型时序预测模型。',
    company: 'Salesforce',
    ranking: 14,
    wmape: 33.64
  },
  {
    id: 'prophet',
    name: 'Prophet',
    description: 'Facebook发布的时序预测工具，专为业务场景设计。',
    company: 'Meta',
    ranking: 15,
    wmape: 54.23
  },
  {
    id: 'itransformer',
    name: 'iTransformer',
    description: '逆Transformer架构，适用于长序列预测。',
    company: '学术界',
    ranking: 16,
    wmape: 67.09
  },
  {
    id: 'llama',
    name: 'Llama',
    description: 'Meta发布的大型语言模型，通过微调可用于时序预测任务。',
    company: 'Meta',
    ranking: 17,
    wmape: 99.97
  }
]

// 滚动窗口回测结果：聚合指标，不含任何商家级明细。
// 展示全部结果
export const backtestResults = [
  {
    rank: 1,
    model_name: 'TimeFM 2.5',
    wmape: 33.677999,
    description: '综合表现最优，滚动窗口回测中WMAPE最低'
  },
  {
    rank: 2,
    model_name: 'TiRex',
    wmape: 33.860221,
    description: '正则化方法表现优秀，稳定性好'
  },
  {
    rank: 3,
    model_name: 'iTransformer',
    wmape: 35.041410,
    description: 'Transformer架构在时序任务上表现良好'
  },
  {
    rank: 4,
    model_name: 'TimeHF-PCTLM',
    wmape: 35.694693,
    description: '结合Transformer和卷积的时序模型'
  },
  {
    rank: 5,
    model_name: 'ELPA',
    wmape: 36.298534,
    description: '集成学习方法，综合性能优秀'
  },
  {
    rank: 6,
    model_name: 'Chronos',
    wmape: 36.307328,
    description: '大语言模型方法，泛化能力强'
  },
  {
    rank: 7,
    model_name: 'CatBoost',
    wmape: 36.356756,
    description: '梯度提升算法，自动处理类别特征'
  },
  {
    rank: 8,
    model_name: 'SMA',
    wmape: 37.048913,
    description: '简单移动平均，基准方法'
  },
  {
    rank: 9,
    model_name: 'XGBoost',
    wmape: 37.178784,
    description: '极端梯度提升树，高性能框架'
  },
  {
    rank: 10,
    model_name: 'XGBoost+RF',
    wmape: 37.558698,
    description: 'XGBoost与随机森林的集成'
  },
  {
    rank: 11,
    model_name: 'PatchTST',
    wmape: 37.794798,
    description: 'Patch方法在滚动回测中表现稳定'
  },
  {
    rank: 12,
    model_name: 'Chronos',
    wmape: 38.452634,
    description: '大语言模型方法中的佼佼者'
  },
  {
    rank: 13,
    model_name: 'Prophet',
    wmape: 46.304273,
    description: 'Facebook时序预测工具'
  },
  {
    rank: 14,
    model_name: 'Lag-Llama',
    wmape: 55.707987,
    description: '基于Llama架构的时序预测模型'
  }
]

// 可用于预测的模型列表（对应目录中的模型）
export const availableModels = [
  { id: 'elpa', name: 'ELPA', path: 'ELPA_预测结果' },
  { id: 'xgboost', name: 'XGBoost', path: 'XGBoost_预测结果' },
  { id: 'xgboost-rf', name: 'XGBoost+RF', path: 'XGBoost_RF_预测结果' },
  { id: 'catboost', name: 'CatBoost', path: 'CatBoost_预测结果' },
  { id: 'timehf-pctlm', name: 'TimeHF-PCTLM', path: 'TimeHF_PCTLM_预测结果' },
  { id: 'timefm2.5', name: 'TimeFM 2.5', path: 'TimeFM2.5_预测结果' },
  { id: 'sarima', name: 'SARIMA', path: 'SARIMA_预测结果' },
  { id: 'tirex', name: 'TiRex', path: 'TiRex' },
  { id: 'chronos', name: 'Chronos', path: 'Chronos' },
  { id: 'lstm', name: 'LSTM', path: 'LSTM' },
  { id: 'lag-llama', name: 'Lag-Llama', path: 'LagLlama' },
  { id: 'extratrees', name: 'ExtraTrees', path: 'ExtraTrees' },
  { id: 'patchtst', name: 'PatchTST', path: 'PatchTST' },
  { id: 'llama', name: 'Llama', path: 'Llama_预测结果' },
  { id: 'prophet', name: 'Prophet', path: 'Prophet' }
]

// 可用于入库管理的模型
export const inventoryModels = [
  { id: 'elpa', name: 'ELPA', recommended: true },
  { id: 'xgboost', name: 'XGBoost', recommended: true },
  { id: 'catboost', name: 'CatBoost', recommended: true },
  { id: 'timehf-pctlm', name: 'TimeHF-PCTLM', recommended: false },
  { id: 'chronos', name: 'Chronos', recommended: false },
  { id: 'tirex', name: 'TiRex', recommended: false }
]

// 生成模拟预测数据
export const generatePredictionData = (modelId, productId) => {
  const model = models.find(m => m.id === modelId) || models[0]
  const startDate = new Date('2025-01-01')
  const timeSeries = []
  const predictions = []
  
  // 生成历史数据（126天）
  for (let i = 0; i < 126; i++) {
    const date = new Date(startDate)
    date.setDate(date.getDate() + i)
    const baseSales = 100 + Math.random() * 100
    const temperature = 15 + Math.sin(i / 30) * 10 + Math.random() * 5
    const isWeekend = date.getDay() === 0 || date.getDay() === 6
    const sales = Math.round(baseSales * (isWeekend ? 1.3 : 1))
    
    timeSeries.push({
      date: date.toISOString().split('T')[0],
      sales,
      temperature: Math.round(temperature * 10) / 10,
      predicted: Math.round(sales * (0.9 + Math.random() * 0.2))
    })
  }
  
  // 生成未来7天预测
  const lastDate = new Date(startDate)
  lastDate.setDate(lastDate.getDate() + 125)
  for (let i = 1; i <= 7; i++) {
    const date = new Date(lastDate)
    date.setDate(date.getDate() + i)
    const baseSales = 100 + Math.random() * 80
    const temperature = 18 + Math.sin((125 + i) / 30) * 10 + Math.random() * 5
    const isWeekend = date.getDay() === 0 || date.getDay() === 6
    const prediction = Math.round(baseSales * (isWeekend ? 1.3 : 1))
    
    predictions.push({
      date: date.toISOString().split('T')[0],
      predicted_sales: prediction,
      temperature: Math.round(temperature * 10) / 10,
      confidence: Math.round((85 + Math.random() * 10) * 10) / 10
    })
  }
  
  // 计算误差指标
  const actualValues = timeSeries.slice(-30).map(t => t.sales)
  const predictedValues = timeSeries.slice(-30).map(t => t.predicted)
  const wmape = calculateWMAPE(actualValues, predictedValues)
  const mape = calculateMAPE(actualValues, predictedValues)
  const smape = calculateSMAPE(actualValues, predictedValues)
  
  return {
    model_id: model.id,
    model_name: model.name,
    product_id: productId || '001_01',
    time_series: timeSeries,
    predictions: predictions,
    error_metrics: {
      wmape: Math.round(wmape * 1000) / 1000,
      mape: Math.round(mape * 1000) / 1000,
      smape: Math.round(smape * 1000) / 1000
    }
  }
}

// 计算WMAPE
function calculateWMAPE(actual, predicted) {
  let numerator = 0
  let denominator = 0
  for (let i = 0; i < actual.length; i++) {
    numerator += Math.abs(actual[i] - predicted[i])
    denominator += Math.abs(actual[i])
  }
  return denominator === 0 ? 0 : numerator / denominator
}

// 计算MAPE
function calculateMAPE(actual, predicted) {
  let sum = 0
  let count = 0
  for (let i = 0; i < actual.length; i++) {
    if (actual[i] !== 0) {
      sum += Math.abs((actual[i] - predicted[i]) / actual[i])
      count++
    }
  }
  return count === 0 ? 0 : sum / count
}

// 计算SMAPE
function calculateSMAPE(actual, predicted) {
  let sum = 0
  for (let i = 0; i < actual.length; i++) {
    const denominator = (Math.abs(actual[i]) + Math.abs(predicted[i])) / 2
    sum += denominator === 0 ? 0 : Math.abs(actual[i] - predicted[i]) / denominator
  }
  return actual.length === 0 ? 0 : sum / actual.length
}