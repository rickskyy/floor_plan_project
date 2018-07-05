/* eslint-disable */

import axios from 'axios'
// import AuthService from '../auth/AuthService';
const API_URL = 'http://localhost:8000/floor_plans/api'

export class APIService {
  constructor () {

  }

  getImageRecords () {
    const url = `${API_URL}/image_records/`
    return axios.get(url).then(response => response.data)
  }

  getImageRecord (pk) {
    const url = `${API_URL}/image_records/${pk}`
    return axios.get(url).then(response => response.data)
  }

  getClassifications () {
    const url = `${API_URL}/image_records/`
    return axios.get(url).then(response => response.data)
  }

  getClassification (pk) {
    const url = `${API_URL}/classifications/${pk}`
    return axios.get(url).then(response => response.data)
  }

  createImageRecord (classification) {
    const url = `${API_URL}/classifications/`
    return axios.post(url, classification)
  }

  createClassification (classification) {
    const url = `${API_URL}/classifications/`
    return axios.post(url, classification)
  }

  // getProductsByURL(link){
  //     const url = `${API_URL}${link}`;
  //     return axios.get(url, { headers: { Authorization: `Bearer ${AuthService.getAuthToken()}` }}).then(response => response.data);
  //
  // }
}
