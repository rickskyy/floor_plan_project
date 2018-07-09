import axios from 'axios'
const API_URL = 'http://localhost:8000/floor_plans/api'

export class APIService {
  getImageRecords (page) {
    const url = `${API_URL}/image_records/?page=` + page
    return axios.get(url).then(response => response.data)
  }

  getImageRecord (pk) {
    const url = `${API_URL}/image_records/${pk}`
    return axios.get(url).then(response => response.data)
  }

  getClassifications () {
    const url = `${API_URL}/classifications/`
    return axios.get(url).then(response => response.data)
  }

  getClassification (pk) {
    const url = `${API_URL}/classifications/${pk}`
    return axios.get(url).then(response => response.data)
  }

  createImageRecord (data, config) {
    const url = `${API_URL}/image_records/`
    return axios.post(url, data, config)
  }

  createClassification (classification) {
    const url = `${API_URL}/classifications/`
    return axios.post(url, classification)
  }

  getByURL (url) {
    return axios.get(url).then(response => response.data)
  }
}
