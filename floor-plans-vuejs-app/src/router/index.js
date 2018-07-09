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
  }
]

const router = new Router({
  // mode: 'history',
  routes
})

export default router
