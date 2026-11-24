<template>
  <div class="guide">
    <!-- 页面标题 -->
    <header class="bg-gradient-to-r from-primary to-secondary text-white py-8 px-6">
      <div class="max-w-7xl mx-auto flex items-center gap-6">
        <!-- 虚拟形象 -->
        <div class="avatar-container">
          <div class="w-24 h-24 rounded-full border-4 border-white shadow-lg bg-white flex items-center justify-center overflow-hidden">
            <svg viewBox="0 0 100 100" class="w-20 h-20">
              <!-- Cat ears hat -->
              <ellipse cx="50" cy="25" rx="40" ry="20" fill="#d4d4d4"/>
              <ellipse cx="25" cy="15" rx="10" ry="15" fill="#d4d4d4"/>
              <ellipse cx="75" cy="15" rx="10" ry="15" fill="#d4d4d4"/>
              <ellipse cx="25" cy="18" rx="5" ry="10" fill="#fcd9d9"/>
              <ellipse cx="75" cy="18" rx="5" ry="10" fill="#fcd9d9"/>
              <!-- Green ribbon on hat -->
              <rect x="20" y="22" width="60" height="3" rx="1" fill="#4ade80"/>
              <rect x="48" y="8" width="4" height="25" rx="1" fill="#4ade80"/>
              <polygon points="46,18 54,18 50,10" fill="#4ade80"/>
              <!-- Hair -->
              <ellipse cx="50" cy="45" rx="38" ry="18" fill="#1f2937"/>
              <path d="M15 40 Q10 55 15 75" stroke="#1f2937" stroke-width="12" fill="none"/>
              <path d="M85 40 Q90 55 85 75" stroke="#1f2937" stroke-width="12" fill="none"/>
              <!-- Face -->
              <ellipse cx="50" cy="65" rx="32" ry="30" fill="#ffe4e1"/>
              <!-- Eyes -->
              <ellipse cx="38" cy="58" rx="7" ry="9" fill="white"/>
              <ellipse cx="62" cy="58" rx="7" ry="9" fill="white"/>
              <circle cx="40" cy="60" r="5" fill="#1f2937"/>
              <circle cx="64" cy="60" r="5" fill="#1f2937"/>
              <circle cx="41" cy="58" r="2" fill="white"/>
              <circle cx="65" cy="58" r="2" fill="white"/>
              <!-- Nose -->
              <polygon points="50,65 47,70 53,70" fill="#ffb3ba"/>
              <!-- Mouth -->
              <path d="M42 75 Q50 82 58 75" stroke="#d69e2e" stroke-width="2" fill="none"/>
              <!-- Cheeks -->
              <ellipse cx="28" cy="70" rx="6" ry="3" fill="#ffcbd3" opacity="0.7"/>
              <ellipse cx="72" cy="70" rx="6" ry="3" fill="#ffcbd3" opacity="0.7"/>
              <!-- Whiskers -->
              <line x1="18" y1="62" x2="32" y2="64" stroke="#1f2937" stroke-width="1.5"/>
              <line x1="18" y1="67" x2="32" y2="67" stroke="#1f2937" stroke-width="1.5"/>
              <line x1="18" y1="72" x2="32" y2="70" stroke="#1f2937" stroke-width="1.5"/>
              <line x1="68" y1="64" x2="82" y2="62" stroke="#1f2937" stroke-width="1.5"/>
              <line x1="68" y1="67" x2="82" y2="67" stroke="#1f2937" stroke-width="1.5"/>
              <line x1="68" y1="70" x2="82" y2="72" stroke="#1f2937" stroke-width="1.5"/>
              <!-- Hair decorations -->
              <circle cx="32" cy="40" r="3" fill="#eab308"/>
              <circle cx="68" cy="40" r="3" fill="#eab308"/>
              <!-- Body/clothes -->
              <rect x="35" y="90" width="30" height="8" rx="2" fill="#9ca3af"/>
              <rect x="30" y="88" width="10" height="12" rx="1" fill="#9ca3af"/>
              <rect x="60" y="88" width="10" height="12" rx="1" fill="#9ca3af"/>
              <rect x="32" y="88" width="36" height="4" rx="1" fill="#dc2626"/>
            </svg>
          </div>
        </div>
        <div>
          <h1 class="text-3xl font-bold mb-2">新手指南</h1>
          <p class="text-white/80">欢迎使用实体商家销量预测系统！我是您的智能助手喵酱~</p>
        </div>
      </div>
    </header>

    <main class="max-w-7xl mx-auto px-6 py-8">
      <!-- 欢迎语 -->
      <div class="bg-white rounded-lg shadow-md p-8 mb-8">
        <div class="flex gap-6">
          <div class="flex-shrink-0">
            <div class="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center">
              <span class="text-3xl">👋</span>
            </div>
          </div>
          <div>
            <h2 class="text-xl font-semibold text-gray-800 mb-2">欢迎来到销量预测系统！</h2>
            <p class="text-gray-600 leading-relaxed">
              嗨~ 我是喵酱，您的专属智能助手！这个系统可以帮助您进行商品销量预测、数据分析和入库管理。
              下面我将为您介绍系统的各个功能模块和操作步骤，让您快速上手使用！
            </p>
          </div>
        </div>
      </div>

      <!-- 功能模块介绍 -->
      <div class="space-y-8">
        <!-- 数据解构 -->
        <section class="bg-white rounded-lg shadow-md p-8">
          <div class="flex items-center gap-4 mb-6">
            <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
            </div>
            <div>
              <h2 class="text-xl font-semibold text-gray-800">📊 数据解构</h2>
              <p class="text-gray-500">了解您的商品数据和分析结果</p>
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="bg-blue-50 rounded-lg p-6">
              <h3 class="font-semibold text-blue-800 mb-3">📍 基础数据</h3>
              <ul class="space-y-2 text-sm text-blue-700">
                <li class="flex items-start gap-2">
                  <span class="text-blue-500">•</span>
                  <span>查看48个商品的详细信息，包括商品编码、行业、名称和店铺地址</span>
                </li>
                <li class="flex items-start gap-2">
                  <span class="text-blue-500">•</span>
                  <span>浏览三个行业（烘焙、餐饮、茶饮）的热力图和箱线图</span>
                </li>
                <li class="flex items-start gap-2">
                  <span class="text-blue-500">•</span>
                  <span>点击商品卡片查看该商品的详细分析报告</span>
                </li>
              </ul>
              <div class="mt-4 p-3 bg-blue-100 rounded-lg">
                <p class="text-sm text-blue-800"><strong>操作步骤：</strong>左侧菜单 → 数据解构 → 基础数据</p>
              </div>
            </div>

            <div class="bg-green-50 rounded-lg p-6">
              <h3 class="font-semibold text-green-800 mb-3">📥 数据管理</h3>
              <ul class="space-y-2 text-sm text-green-700">
                <li class="flex items-start gap-2">
                  <span class="text-green-500">•</span>
                  <span><strong>新店家数据载入：</strong>填写行业、地址、商品名称，系统自动生成商品ID</span>
                </li>
                <li class="flex items-start gap-2">
                  <span class="text-green-500">•</span>
                  <span><strong>旧店家数据更新：</strong>输入商品ID查询历史数据，支持修改和添加新数据</span>
                </li>
                <li class="flex items-start gap-2">
                  <span class="text-green-500">•</span>
                  <span>支持Excel文件识别导入数据</span>
                </li>
              </ul>
              <div class="mt-4 p-3 bg-green-100 rounded-lg">
                <p class="text-sm text-green-800"><strong>操作步骤：</strong>左侧菜单 → 数据解构 → 数据管理</p>
              </div>
            </div>
          </div>
        </section>

        <!-- 模型调用 -->
        <section class="bg-white rounded-lg shadow-md p-8">
          <div class="flex items-center gap-4 mb-6">
            <div class="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-purple-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
              </svg>
            </div>
            <div>
              <h2 class="text-xl font-semibold text-gray-800">🤖 模型调用</h2>
              <p class="text-gray-500">使用AI模型进行销量预测分析</p>
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="bg-purple-50 rounded-lg p-6">
              <h3 class="font-semibold text-purple-800 mb-3">📋 模型列表</h3>
              <ul class="space-y-2 text-sm text-purple-700">
                <li class="flex items-start gap-2">
                  <span class="text-purple-500">•</span>
                  <span>查看14种预测模型的详细信息，包括模型介绍、发布单位和排名</span>
                </li>
                <li class="flex items-start gap-2">
                  <span class="text-purple-500">•</span>
                  <span>查看综合WMAPE排名前五的模型回测结果</span>
                </li>
                <li class="flex items-start gap-2">
                  <span class="text-purple-500">•</span>
                  <span>了解各模型的误差指标（WMAPE、MAPE、SMAPE）</span>
                </li>
              </ul>
              <div class="mt-4 p-3 bg-purple-100 rounded-lg">
                <p class="text-sm text-purple-800"><strong>操作步骤：</strong>左侧菜单 → 模型调用 → 模型列表</p>
              </div>
            </div>

            <div class="bg-orange-50 rounded-lg p-6">
              <h3 class="font-semibold text-orange-800 mb-3">🔮 模型预测</h3>
              <ul class="space-y-2 text-sm text-orange-700">
                <li class="flex items-start gap-2">
                  <span class="text-orange-500">•</span>
                  <span><strong>模型选择：</strong>从14个模型中选择用于预测的模型</span>
                </li>
                <li class="flex items-start gap-2">
                  <span class="text-orange-500">•</span>
                  <span><strong>商品筛选：</strong>选择要预测的商品</span>
                </li>
                <li class="flex items-start gap-2">
                  <span class="text-orange-500">•</span>
                  <span>查看模型误差检验、时序图和未来7天预测结果</span>
                </li>
              </ul>
              <div class="mt-4 p-3 bg-orange-100 rounded-lg">
                <p class="text-sm text-orange-800"><strong>操作步骤：</strong>左侧菜单 → 模型调用 → 模型预测</p>
              </div>
            </div>
          </div>
        </section>

        <!-- 入库管理 -->
        <section class="bg-white rounded-lg shadow-md p-8">
          <div class="flex items-center gap-4 mb-6">
            <div class="w-12 h-12 bg-teal-100 rounded-lg flex items-center justify-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-teal-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
              </svg>
            </div>
            <div>
              <h2 class="text-xl font-semibold text-gray-800">📦 入库管理</h2>
              <p class="text-gray-500">基于模型预测生成智能入库报告</p>
            </div>
          </div>

          <div class="bg-teal-50 rounded-lg p-6">
            <h3 class="font-semibold text-teal-800 mb-3">📊 入库报告</h3>
            <ul class="space-y-3 text-sm text-teal-700">
              <li class="flex items-start gap-2">
                <span class="text-teal-500">•</span>
                <span><strong>筛选条件：</strong>选择预测模型和商品，设置预测天数（1-30天）</span>
              </li>
              <li class="flex items-start gap-2">
                <span class="text-teal-500">•</span>
                <span><strong>报告内容：</strong>包含总结、详细预测结果、模型检验、时序图和入库建议</span>
              </li>
              <li class="flex items-start gap-2">
                <span class="text-teal-500">•</span>
                <span><strong>峰值预测：</strong>自动识别销量峰值日期，提醒重点备货</span>
              </li>
              <li class="flex items-start gap-2">
                <span class="text-teal-500">•</span>
                <span><strong>导出功能：</strong>支持导出为HTML或Word格式报告</span>
              </li>
            </ul>
            <div class="mt-4 p-3 bg-teal-100 rounded-lg">
              <p class="text-sm text-teal-800"><strong>操作步骤：</strong>左侧菜单 → 入库管理 → 入库报告</p>
            </div>
          </div>
        </section>

        <!-- 使用流程图 -->
        <section class="bg-white rounded-lg shadow-md p-8">
          <div class="flex items-center gap-4 mb-6">
            <div class="w-12 h-12 bg-pink-100 rounded-lg flex items-center justify-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-pink-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <div>
              <h2 class="text-xl font-semibold text-gray-800">🚀 快速上手流程图</h2>
              <p class="text-gray-500">一步步教您使用系统</p>
            </div>
          </div>

          <div class="relative">
            <div class="flex flex-col md:flex-row items-center justify-between gap-4">
              <!-- 步骤1 -->
              <div class="flex flex-col items-center">
                <div class="w-16 h-16 bg-blue-500 rounded-full flex items-center justify-center text-white font-bold text-xl shadow-lg">1</div>
                <p class="mt-3 text-center text-gray-700 font-medium">浏览数据</p>
                <p class="text-sm text-gray-500 text-center max-w-xs">查看基础数据页面了解商品信息</p>
              </div>
              <div class="hidden md:block w-16 h-0.5 bg-gray-300"></div>
              <div class="hidden md:block text-2xl text-gray-400">→</div>

              <!-- 步骤2 -->
              <div class="flex flex-col items-center">
                <div class="w-16 h-16 bg-green-500 rounded-full flex items-center justify-center text-white font-bold text-xl shadow-lg">2</div>
                <p class="mt-3 text-center text-gray-700 font-medium">管理数据</p>
                <p class="text-sm text-gray-500 text-center max-w-xs">添加新商品或更新历史数据</p>
              </div>
              <div class="hidden md:block w-16 h-0.5 bg-gray-300"></div>
              <div class="hidden md:block text-2xl text-gray-400">→</div>

              <!-- 步骤3 -->
              <div class="flex flex-col items-center">
                <div class="w-16 h-16 bg-purple-500 rounded-full flex items-center justify-center text-white font-bold text-xl shadow-lg">3</div>
                <p class="mt-3 text-center text-gray-700 font-medium">选择模型</p>
                <p class="text-sm text-gray-500 text-center max-w-xs">在模型列表中选择合适的预测模型</p>
              </div>
              <div class="hidden md:block w-16 h-0.5 bg-gray-300"></div>
              <div class="hidden md:block text-2xl text-gray-400">→</div>

              <!-- 步骤4 -->
              <div class="flex flex-col items-center">
                <div class="w-16 h-16 bg-orange-500 rounded-full flex items-center justify-center text-white font-bold text-xl shadow-lg">4</div>
                <p class="mt-3 text-center text-gray-700 font-medium">生成报告</p>
                <p class="text-sm text-gray-500 text-center max-w-xs">生成入库预测报告并导出</p>
              </div>
            </div>
          </div>
        </section>

        <!-- 常见问题 -->
        <section class="bg-white rounded-lg shadow-md p-8">
          <div class="flex items-center gap-4 mb-6">
            <div class="w-12 h-12 bg-yellow-100 rounded-lg flex items-center justify-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-yellow-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div>
              <h2 class="text-xl font-semibold text-gray-800">❓ 常见问题</h2>
              <p class="text-gray-500">喵酱为您解答常见疑问</p>
            </div>
          </div>

          <div class="space-y-4">
            <div class="border border-gray-200 rounded-lg overflow-hidden">
              <button 
                @click="toggleFAQ(0)" 
                class="w-full px-6 py-4 text-left flex items-center justify-between hover:bg-gray-50 transition-colors"
              >
                <span class="font-medium text-gray-800">什么是WMAPE指标？</span>
                <svg 
                  xmlns="http://www.w3.org/2000/svg" 
                  class="h-5 w-5 text-gray-500 transition-transform"
                  :class="{ 'rotate-180': faqOpen[0] }"
                  fill="none" viewBox="0 0 24 24" stroke="currentColor"
                >
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
              </button>
              <div v-show="faqOpen[0]" class="px-6 pb-4 text-gray-600 text-sm">
                <p>WMAPE（Weighted Mean Absolute Percentage Error）即加权平均绝对百分比误差，是衡量预测准确性的重要指标。</p>
                <p class="mt-2">• WMAPE < 10%: 优秀</p>
                <p>• 10% ≤ WMAPE < 20%: 良好</p>
                <p>• 20% ≤ WMAPE < 30%: 一般</p>
                <p>• WMAPE ≥ 30%: 较差</p>
              </div>
            </div>

            <div class="border border-gray-200 rounded-lg overflow-hidden">
              <button 
                @click="toggleFAQ(1)" 
                class="w-full px-6 py-4 text-left flex items-center justify-between hover:bg-gray-50 transition-colors"
              >
                <span class="font-medium text-gray-800">如何选择合适的预测模型？</span>
                <svg 
                  xmlns="http://www.w3.org/2000/svg" 
                  class="h-5 w-5 text-gray-500 transition-transform"
                  :class="{ 'rotate-180': faqOpen[1] }"
                  fill="none" viewBox="0 0 24 24" stroke="currentColor"
                >
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
              </button>
              <div v-show="faqOpen[1]" class="px-6 pb-4 text-gray-600 text-sm">
                <p>建议参考模型列表中的综合排名，选择WMAPE较低的模型。通常TimeFM 2.5、Chronos等模型表现较好。</p>
                <p class="mt-2">您也可以在模型预测页面尝试不同模型，比较它们对同一商品的预测结果，选择最适合您业务场景的模型。</p>
              </div>
            </div>

            <div class="border border-gray-200 rounded-lg overflow-hidden">
              <button 
                @click="toggleFAQ(2)" 
                class="w-full px-6 py-4 text-left flex items-center justify-between hover:bg-gray-50 transition-colors"
              >
                <span class="font-medium text-gray-800">商品ID是如何生成的？</span>
                <svg 
                  xmlns="http://www.w3.org/2000/svg" 
                  class="h-5 w-5 text-gray-500 transition-transform"
                  :class="{ 'rotate-180': faqOpen[2] }"
                  fill="none" viewBox="0 0 24 24" stroke="currentColor"
                >
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
              </button>
              <div v-show="faqOpen[2]" class="px-6 pb-4 text-gray-600 text-sm">
                <p>商品ID由系统自动生成，格式为三位数字_两位数字（如 001_01）。</p>
                <p class="mt-2">• 每6个编号为一组，同一组编号的商品行业必须一致</p>
                <p>• 当您选择行业后，系统会自动计算并分配下一个可用的编号</p>
                <p>• 这样可以确保商品分类清晰，便于管理和查询</p>
              </div>
            </div>

            <div class="border border-gray-200 rounded-lg overflow-hidden">
              <button 
                @click="toggleFAQ(3)" 
                class="w-full px-6 py-4 text-left flex items-center justify-between hover:bg-gray-50 transition-colors"
              >
                <span class="font-medium text-gray-800">入库建议是如何计算的？</span>
                <svg 
                  xmlns="http://www.w3.org/2000/svg" 
                  class="h-5 w-5 text-gray-500 transition-transform"
                  :class="{ 'rotate-180': faqOpen[3] }"
                  fill="none" viewBox="0 0 24 24" stroke="currentColor"
                >
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
              </button>
              <div v-show="faqOpen[3]" class="px-6 pb-4 text-gray-600 text-sm">
                <p>入库建议 = 预测总销量 × 安全系数（默认120%）</p>
                <p class="mt-2">安全系数考虑了预测误差和突发情况，建议根据实际销售情况调整。同时系统会识别销量峰值日期，提醒您重点备货。</p>
              </div>
            </div>
          </div>
        </section>

        <!-- 结语 -->
        <section class="bg-gradient-to-r from-primary/10 to-secondary/10 rounded-lg p-8 text-center">
          <div class="flex justify-center mb-4">
            <div class="w-20 h-20 rounded-full border-4 border-white shadow-lg bg-white flex items-center justify-center overflow-hidden">
              <svg viewBox="0 0 100 100" class="w-16 h-16">
                <!-- Cat ears hat -->
                <ellipse cx="50" cy="25" rx="40" ry="20" fill="#d4d4d4"/>
                <ellipse cx="25" cy="15" rx="10" ry="15" fill="#d4d4d4"/>
                <ellipse cx="75" cy="15" rx="10" ry="15" fill="#d4d4d4"/>
                <ellipse cx="25" cy="18" rx="5" ry="10" fill="#fcd9d9"/>
                <ellipse cx="75" cy="18" rx="5" ry="10" fill="#fcd9d9"/>
                <!-- Green ribbon on hat -->
                <rect x="20" y="22" width="60" height="3" rx="1" fill="#4ade80"/>
                <rect x="48" y="8" width="4" height="25" rx="1" fill="#4ade80"/>
                <polygon points="46,18 54,18 50,10" fill="#4ade80"/>
                <!-- Hair -->
                <ellipse cx="50" cy="45" rx="38" ry="18" fill="#1f2937"/>
                <path d="M15 40 Q10 55 15 75" stroke="#1f2937" stroke-width="12" fill="none"/>
                <path d="M85 40 Q90 55 85 75" stroke="#1f2937" stroke-width="12" fill="none"/>
                <!-- Face -->
                <ellipse cx="50" cy="65" rx="32" ry="30" fill="#ffe4e1"/>
                <!-- Eyes -->
                <ellipse cx="38" cy="58" rx="7" ry="9" fill="white"/>
                <ellipse cx="62" cy="58" rx="7" ry="9" fill="white"/>
                <circle cx="40" cy="60" r="5" fill="#1f2937"/>
                <circle cx="64" cy="60" r="5" fill="#1f2937"/>
                <circle cx="41" cy="58" r="2" fill="white"/>
                <circle cx="65" cy="58" r="2" fill="white"/>
                <!-- Nose -->
                <polygon points="50,65 47,70 53,70" fill="#ffb3ba"/>
                <!-- Mouth -->
                <path d="M42 75 Q50 82 58 75" stroke="#d69e2e" stroke-width="2" fill="none"/>
                <!-- Cheeks -->
                <ellipse cx="28" cy="70" rx="6" ry="3" fill="#ffcbd3" opacity="0.7"/>
                <ellipse cx="72" cy="70" rx="6" ry="3" fill="#ffcbd3" opacity="0.7"/>
                <!-- Whiskers -->
                <line x1="18" y1="62" x2="32" y2="64" stroke="#1f2937" stroke-width="1.5"/>
                <line x1="18" y1="67" x2="32" y2="67" stroke="#1f2937" stroke-width="1.5"/>
                <line x1="18" y1="72" x2="32" y2="70" stroke="#1f2937" stroke-width="1.5"/>
                <line x1="68" y1="64" x2="82" y2="62" stroke="#1f2937" stroke-width="1.5"/>
                <line x1="68" y1="67" x2="82" y2="67" stroke="#1f2937" stroke-width="1.5"/>
                <line x1="68" y1="70" x2="82" y2="72" stroke="#1f2937" stroke-width="1.5"/>
                <!-- Hair decorations -->
                <circle cx="32" cy="40" r="3" fill="#eab308"/>
                <circle cx="68" cy="40" r="3" fill="#eab308"/>
                <!-- Body/clothes -->
                <rect x="35" y="90" width="30" height="8" rx="2" fill="#9ca3af"/>
                <rect x="30" y="88" width="10" height="12" rx="1" fill="#9ca3af"/>
                <rect x="60" y="88" width="10" height="12" rx="1" fill="#9ca3af"/>
                <rect x="32" y="88" width="36" height="4" rx="1" fill="#dc2626"/>
              </svg>
            </div>
          </div>
          <h3 class="text-xl font-semibold text-gray-800 mb-3">💝 祝您使用愉快！</h3>
          <p class="text-gray-600 mb-4">
            如果您在使用过程中有任何问题，随时可以查看本指南，或联系我们的技术支持团队。
          </p>
          <p class="text-primary font-medium">喵酱期待为您服务！🐱✨</p>
        </section>
      </div>
    </main>

    <!-- 页脚 -->
    <footer class="bg-gray-800 text-white py-4 px-6">
      <div class="max-w-7xl mx-auto text-center text-sm">
        <p>实体商家销量预测系统 © 2025 | 喵酱陪您一起做预测 🐱</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref } from 'vue'

// FAQ展开状态
const faqOpen = ref([false, false, false, false])

const toggleFAQ = (index) => {
  faqOpen.value[index] = !faqOpen.value[index]
}
</script>

<style scoped>
.avatar-container {
  animation: bounce 2s infinite;
}

@keyframes bounce {
  0%, 20%, 50%, 80%, 100% {
    transform: translateY(0);
  }
  40% {
    transform: translateY(-10px);
  }
  60% {
    transform: translateY(-5px);
  }
}
</style>
