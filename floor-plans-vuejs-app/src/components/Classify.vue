<template>
  <div id="container" class="container">
    <div class="row">
      <div class="col-sm-8 offset-sm-2">
        <div class="alert alert-warning" v-show="showClassifiedMessage"  >
          <button type="button" class="close" @click="hideMessage()">X</button>
          <strong>Image classified! Is floor plan: {{currentImageResult.toString()}}</strong>
        </div>
        <div class="alert alert-warning" v-show="showError">
          <button type="button" class="close" @click="hideMessage()">X</button>
          <strong>Error! {{errorMessage}}</strong>
        </div>

        <div class="form-group">
          <Loading :loading="loading"></Loading>
          <h1>Classify image</h1>
          <h4>Upload file from file storage or enter the url. <br>If both specified, file will be used.</h4>
          <div class="info-form">
            <form id="classifyForm">
              <label>Select file</label>
              <!-- Accept all image formats by IANA media type wildcard-->
              <b-form-file v-if="loading === false" v-model="file" id="fileUpload" :state="Boolean(file)" placeholder="Choose a file..."
                           accept="image/*" @change="previewImage"></b-form-file>
              <div class="mt-3" v-if="file">Selected file: {{file && file.name}}</div>
              <div v-if="imageData.length > 0">
                <b-img id="uploaded" rounded :src="imageData"/>
              </div>

              <label for="urlInput">Enter Url</label>
              <input type="url" id="urlInput" v-model="imageUrl" class="form-control" placeholder="Enter image source URL">

              <label for="selCls">Select classifier:</label>
              <select class="form-control" v-model="classifierId" id="selCls">
                <option v-for="cls in implementedClassifiers" v-bind:key="cls.id"
                        v-bind:value="cls.id">
                  {{cls.algorithm}}
                </option>
              </select>
            </form>
            <button class="btn btn-primary" @click="classify()" >Classify</button>
          </div>

        </div>
      </div>
    </div>
  </div>
</template>

<script>

import bFormFile from 'bootstrap-vue/es/components/form-file/form-file'
import bImg from 'bootstrap-vue/es/components/image/img'
import {APIService} from '../http/APIService'
import Loading from './Loading'

const apiService = new APIService()
const API_URL = 'http://localhost:8000/floor_plans/api/'

export default {
  name: 'Classify',
  components: {
    'b-form-file': bFormFile,
    'b-img': bImg,
    Loading
  },
  data () {
    return {
      showClassifiedMessage: false,
      showError: false,
      errorMessage: '',
      loading: false,

      file: null,
      imageData: '',
      imageUrl: '',
      currentImageResult: '',

      implementedClassifiers: '',
      classifierId: '',
      classifierUrl: ''
    }
  },
  methods: {
    hideMessage () {
      this.showClassifiedMessage = false
      this.showError = false
      this.currentImageResult = ''
    },
    previewImage: function (event) {
      let input = event.target
      if (input.files && input.files[0]) {
        let readerURL = new FileReader()
        readerURL.onload = (e) => {
          this.imageData = e.target.result
        }
        readerURL.readAsDataURL(input.files[0])
      }
    },
    classify () {
      if (this.file !== null) {
        let formData = new FormData()
        formData.append('file', this.file)
        let config = {headers: {'Content-Type': 'multipart/form-data'}}
        return this._classify(formData, config)
      } else if (this.imageUrl.length > 0) {
        return this._classify({'origin_url': this.imageUrl}, {})
      } else {
        this.showError = true
        this.errorMessage = 'Please add either image or image URL'
      }
    },
    _classify (obj, config) {
      this.loading = true
      apiService.createImageRecord(obj, config)
        .then((imageRecord) => {
          if (imageRecord.status === 201 || imageRecord.status === 200) {
            this._createClassification(imageRecord)
          } else {
            this.handleError('Could not create image record ' + JSON.stringify(imageRecord.data))
          }
        },
        (error) => {
          this.handleError('Could not create image record ' + JSON.stringify(error.response.data))
        })
    },
    _createClassification (imageRecord) {
      apiService.createClassification({'image_record': imageRecord.data.url, 'classifier': this.classifierUrl})
        .then((result) => {
          if (result.status === 201 || result.status === 200) {
            this.currentImageResult = result.data.is_floor_plan
            this.showClassifiedMessage = true
            this.reset_form()
          } else {
            this.handleError('Could not classify image record ' + JSON.stringify(result.data))
          }
        },
        (error) => {
          this.handleError('Could not classify image record ' + JSON.stringify(error.response.data))
        })
    },
    reset_form () {
      this.file = null
      this.imageData = ''
      this.imageUrl = ''
      this.loading = false
    },
    getClassifiers () {
      apiService.getByURL(API_URL + 'classifiers-types/').then((classifiers) => {
        this.implementedClassifiers = classifiers
        this.classifierId = this.implementedClassifiers[0].id
        this.classifierUrl = this.getClassifierUrlByClassifierId(this.classifierId)
      })
    },
    getClassifierUrlByClassifierId (id) {
      for (let cls of this.implementedClassifiers) {
        if (cls.id === id) {
          return cls.url
        } else {
          return null
        }
      }
    },
    handleError (message) {
      this.errorMessage = message
      this.showError = true
      this.reset_form()
    }
  },
  mounted () {
    this.getClassifiers()
  }
}

</script>

<style scoped>
#uploaded {
  padding: 20px;
  height: 400px;
  width: 400px;
}

.form-group {
  margin-top: 30px;
}

label {
  margin-top: 20px;
}

form {
  margin-bottom: 20px;
}
</style>
