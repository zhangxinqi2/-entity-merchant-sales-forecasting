import { createRouter, createWebHashHistory } from 'vue-router'
import Dashboard from '@/views/Dashboard/index.vue'
import ProductDetail from '@/views/ProductDetail/index.vue'
import ModelCalling from '@/views/ModelCalling/index.vue'
import ModelDetail from '@/views/ModelDetail/index.vue'
import DataManagement from '@/views/DataManagement/index.vue'
import Inventory from '@/views/Inventory/index.vue'
import Guide from '@/views/Guide/index.vue'

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard
  },
  {
    path: '/product/:productId',
    name: 'ProductDetail',
    component: ProductDetail
  },
  {
    path: '/data-management',
    name: 'DataManagement',
    component: DataManagement
  },
  {
    path: '/model-calling',
    name: 'ModelCalling',
    component: ModelCalling
  },
  {
    path: '/model-detail',
    name: 'ModelDetail',
    component: ModelDetail
  },
  {
    path: '/inventory',
    name: 'Inventory',
    component: Inventory
  },
  {
    path: '/guide',
    name: 'Guide',
    component: Guide
  }
]

const router = createRouter({
  // Hash history keeps deep links working on GitHub Pages without a server rewrite.
  history: createWebHashHistory(),
  routes
})

export default router
