<template>
  <div>
    <h1>ImageRecords ({{ numberOfImageRecords }})</h1>
    <Loading :loading="loading"></Loading>
    <div class="form-group">
      <label for="selCls">Select classifier:</label>
      <select class="form-control" v-model="classifierId" id="selCls">
        <option v-for="cls in implementedClassifiers" v-bind:key="cls.id"
                v-bind:value="cls.id">
          {{cls.algorithm}}
        </option>
      </select>
    </div>
    <table class="table table-bordered table-hover" id="imageRecords">
      <thead>
      <tr>
        <th>ID</th>
        <th>Image</th>
        <th>Is floor plan</th>
        <th>Classify</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="image in imageRecords" :key="image.id" @click="selectImageRecord(image)">
        <th>{{image.id}}</th>
        <td><a :href="getImageURL(image)"><b-img rounded :src="getImageURL(image)" height="250px" width="250px" /></a></td>
        <td v-if="ifImageClassifications(image)">{{ getClassificationByClassifierId(image, classifierId) }}</td>
        <td v-else class="highlight"></td>
        <td>
          <button class="btn btn-primary" @click="classifyImageRecord(image)"> C</button>
          <!--<a class="btn btn-primary" v-bind:href="'/imageRecord-update/' + imageRecord.pk"> &#9998; </a>-->
        </td>
      </tr>
      </tbody>
    </table>
    <div>
      <ul class="list-horizontal">
        <li><button class="btn btn-primary" @click="getPreviousPage()">Previous</button></li>
        <li v-for="page in pages.slice(getStart(), getEnd())" :key="page.pageNumber">
          <button class="btn btn-primary" @click="getPage(page)">{{ page.pageNumber }}</button>
        </li>
        <li><button class="btn btn-primary" @click="getNextPage()">Next</button></li>
      </ul>
    </div>
  </div>
</template>

<script>
import {APIService} from '../http/APIService'
import Loading from './Loading'
import bImg from 'bootstrap-vue/es/components/image/img'

const API_URL = 'http://localhost:8000/floor_plans/api/'
const apiService = new APIService()

function sleep (time) {
  return new Promise((resolve) => setTimeout(resolve, time))
}

export default {
  name: 'ImageRecordList',
  components: {
    Loading,
    'b-img': bImg
  },
  data () {
    return {
      selectedImageRecord: null,
      imageRecords: [],

      classifierId: '',
      classifierUrl: '',
      implementedClassifiers: [],
      selectedImageClassifications: [],

      loading: false,
      pages: [],
      numberOfPages: 0,
      numberOfImageRecords: 0,
      nextPageURL: '',
      previousPageURL: '',
      currentPageNumber: 1,
      maxLinksNumFromCurrent: 5
    }
  },
  methods: {
    getImageRecords (pageNum) {
      this.loading = true
      apiService.getImageRecords(pageNum).then((page) => {
        this.imageRecords = page.results
        this.numberOfImageRecords = page.count
        this.numberOfPages = page.total_pages
        this.nextPageURL = page.next
        this.previousPageURL = page.previous
        if (this.numberOfPages) {
          for (let i = 1; i <= this.numberOfPages; i++) {
            const link = `image_records/?page=${i}`
            this.pages.push({pageNumber: i, link: link})
          }
        }
      })
      this.loading = false
    },
    getPage (page) {
      this.loading = true
      this.currentPageNumber = page.pageNumber
      console.log(this.currentPageNumber)
      apiService.getByURL(API_URL + page.link).then((newPage) => {
        this.imageRecords = newPage.results
        this.nextPageURL = newPage.next
        this.previousPageURL = newPage.previous
      })
      this.loading = false
    },
    getNextPage () {
      this.loading = true
      if (this.nextPageURL !== null) {
        this.currentPageNumber += 1
        apiService.getByURL(this.nextPageURL).then((page) => {
          this.imageRecords = page.results
          this.nextPageURL = page.next
          this.previousPageURL = page.previous
        })
      }
      this.loading = false
    },
    getPreviousPage () {
      this.loading = true
      if (this.previousPageURL !== null) {
        this.currentPageNumber = this.currentPageNumber - 1
        apiService.getByURL(this.previousPageURL).then((page) => {
          this.imageRecords = page.results
          this.nextPageURL = page.next
          this.previousPageURL = page.previous
        })
      }
      this.loading = false
    },
    getStart () {
      const start = this.currentPageNumber - this.maxLinksNumFromCurrent - 1
      return start < 0 ? 0 : start
    },
    getEnd () {
      const end = this.currentPageNumber + this.maxLinksNumFromCurrent
      return end > this.numberOfPages ? this.numberOfPages : end
    },
    selectImageRecord (imageRecord) {
      this.selectedImageRecord = imageRecord
    },
    ifImageClassifications (image) {
      let array = image.classifications
      return typeof array !== 'undefined' && array.length > 0
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
    getClassificationByClassifierId (image, id) {
      for (let cls of image.classifications) {
        if (cls.classifier.id === id) {
          return cls.is_floor_plan
        } else {
          return null
        }
      }
    },
    getImageURL (image) {
      if (image.file !== null) {
        return image.file
      } else {
        return image.origin_url
      }
    },
    classifyImageRecord (image) {
      this.loading = true
      apiService.createClassification({'image_record': image.url, 'classifier': this.classifierUrl})
        .then((result) => {},
          (error) => {
            alert('Could not classify image record. ' + JSON.stringify(error.response.data))
          }
        )
      this.loading = false
      this.$router.push({path: '/image-record-list/page/' + this.currentPageNumber.toString()})
      // wait the database to update
      sleep(1000).then(() => {
        location.reload()
      })
    }
  },
  mounted () {
    if (this.$route.params.pk) {
      this.getImageRecords(this.$route.params.pk)
    } else {
      this.getImageRecords(1)
    }
    this.getClassifiers()
  }
}
</script>

<style scoped>
  .list-horizontal li {
    display:inline-block;
  }
  .list-horizontal li:before {
    content: '\00a0\2022\00a0\00a0';
    color:#999;
    font-size:11px;
  }
  .list-horizontal li:first-child:before {
    content: '';
  }
  .form-group {
    margin-top: 30px;
  }
  #imageRecords td, th {
    vertical-align: middle;
    text-align: center;
  }
  .highlight {
    background-color: #ecff9f;
  }
</style>
