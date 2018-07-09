/* eslint-disable */

import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/Home'
import ImageRecordList from '@/components/ImageRecordList'
import Classify from '@/components/Classify'

Vue.use(Router)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/image-record-list/page/:pk',
    name: 'ImageRecordList',
    component: ImageRecordList
  },
  {
    path: '/image-record-list/',
    name: 'ImageRecordList',
    component: ImageRecordList
  },
  {
    path: '/image-record-classify',
    name: 'Classify',
    component: Classify
  },
  // {path: '/image-record-list', redirect: '/image-record-list/1'}
]

const router = new Router({
  // mode: 'history',
  // base: '/',
  // hashbang: false,
  //abstract: true,
  // history: true,
  // mode: 'html5',
  // linkActiveClass: 'active',
  // transitionOnLoad: true,
  // root: '/',
  routes
})

export default router
//
// router.beforeEach((to, from, next) => {
//   console.log('routing ', from, AuthService.authenticated())
//   if(to.meta.requiresAuth)
//   {
//     if(!AuthService.authenticated())
//     {
//       next('/');
//     }
//   }
//   next()
// })
//
// export function authGuard(to, from, next) {
//
//   if(!AuthService.authenticated()){
//     next('/');
//   }
//   next()
//
// }

// export default new Router({
//   routes: [
//     {
//       path: '/',
//       name: 'Home',
//       component: Home
//     }
//   ]
// })
