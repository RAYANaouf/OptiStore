import { createRouter, createWebHistory } from "vue-router";
import Dashboard from "../views/Dashboard.vue";
import POS from "../views/POS.vue";
import StockLevel from "../views/StockLevel.vue";
import Pricing from "../views/Pricing.vue";
import authRoutes from './auth';

const routes = [
  {
    path: "/",
    redirect: "/dashboard"
  },
  {
    path: "/dashboard",
    name: "Dashboard", 
    component: Dashboard,
  },
  {
    path: "/pos",
    name: "POS",
    component: POS,
  },
  {
    path: "/stock",
    name: "StockLevel",
    component: StockLevel,
  },
  {
    path: "/pricing",
    name: "Pricing",
    component: Pricing,
  },
  ...authRoutes,
];

const router = createRouter({
  history: createWebHistory("/OpticStock"),
  routes,
});

export default router;
