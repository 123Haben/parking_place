import { createRouter, createWebHistory } from 'vue-router'

// Komponenten importieren
import SmartParking from '../components/SmartParking.vue'
import Analytics from '../components/Analytics.vue'
import gate from '../components/Gate.vue'

const routes = [
    {
        path: '/dashboard',
        name: 'dashboard',
        component: SmartParking
    },
  { path: '/analytics', name: 'analytics', component: Analytics },
    { path: '/gate', name: 'gate', component: gate },
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

export default router
