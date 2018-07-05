/* eslint-disable */

<template>
  <div>
    <h1>ImageRecords ()</h1>
    <Loading :loading="loading"></Loading>
    <table class="table table-bordered table-hover">
      <thead>
      <tr>
        <th>#</th>
        <th>Image</th>
        <th>Url</th>
        <th>Is floor plan</th>
        <th>Classifiers</th>
        <th>Date of Classification</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="image in imageRecords" :key="image.id" @click="selectImageRecord(image)">
        <th>{{image.id}}</th>
        <th>{{image.url}}</th>
        <!--<td></td>-->
        <!--<td></td>-->
        <!--<td></td>-->
        <!--<td>-->
          <!--<button class="btn btn-danger" @click="deleteImageRecord(imageRecord)"> X</button>-->
          <!--<a class="btn btn-primary" v-bind:href="'/imageRecord-update/' + imageRecord.pk"> &#9998; </a>-->
        <!--</td>-->
      </tr>
      </tbody>
    </table>
    <!--<div>-->
      <!--<ul class="list-horizontal">-->
        <!--<li><button class="btn btn-primary" @click="getPreviousPage()">Previous</button></li>-->
        <!--<li v-for="page in pages">-->
          <!--<a class="btn btn-primary" @click="getPage(page.link)"></a>-->
        <!--</li>-->
        <!--<li><button class="btn btn-primary" @click="getNextPage()">Next</button></li>-->
      <!--</ul>-->

    <!--</div>-->

    <!--<div class="card text-center" v-if="selectedImageRecord">-->
      <!--<div class="card-header">-->
        <!--# &#45;&#45;-->
      <!--</div>-->
      <!--<div class="card-block">-->
        <!--<h4 class="card-title"></h4>-->
        <!--<p class="card-text">-->

        <!--</p>-->
        <!--<a class="btn btn-primary" v-bind:href="'/imageRecord-update/' + selectedImageRecord.pk"> &#9998; </a>-->
        <!--<button class="btn btn-danger" @click="deleteImageRecord(selectedImageRecord)"> X</button>-->

      <!--</div>-->

    <!--</div>-->
  </div>
</template>

<script>
/* eslint-disable */
  import {APIService} from '../http/APIService';
  import Loading from './Loading';
  const API_URL = 'http://localhost:8000/floor_plans/api';
  const apiService = new APIService();

  export default {
    name: 'ImageRecordList',
    components: {
      Loading
    },
    data() {
      return {
        selectedImageRecord:null,
        imageRecords: [],
        // numberOfPages:0,
        pages : [],
        numberOfImageRecords:0,
        loading: false,
        nextPageURL:'',
        previousPageURL:''
      };
    },
    methods: {
      getImageRecords(){

        this.loading = true;
        apiService.getImageRecords().then((page) => {
          this.imageRecords = page.data.results;
          // console.log(page);
          // console.log(page.nextlink);
          this.numberOfImageRecords = page.count;
          // this.numberOfPages = page.numpages;
          this.nextPageURL = page.next;
          this.previousPageURL = page.previous;
          // if(this.numberOfPages)
          // {
          //   for(var i = 1 ; i <= this.numberOfPages ; i++)
          //   {
          //     const link = `/api/imageRecords/?page=${i}`;
          //     this.pages.push({pageNumber: i , link: link})
          //   }
          // }
          this.loading = false;
        });
      },
      // getPage(link){
      //   this.loading = true;
      //   apiService.getImageRecordsByURL(link).then((page) => {
      //     this.imageRecords = page.data;
      //     this.nextPageURL = page.nextlink;
      //     this.previousPageURL = page.prevlink;
      //     this.loading = false;
      //   });
      // },
      // getNextPage(){
      //   console.log('next' + this.nextPageURL);
      //   this.loading = true;
      //   apiService.getImageRecordsByURL(this.nextPageURL).then((page) => {
      //     this.imageRecords = page.data;
      //     this.nextPageURL = page.nextlink;
      //     this.previousPageURL = page.prevlink;
      //     this.loading = false;
      //   });
      //
      // },
      // getPreviousPage(){
      //   this.loading = true;
      //   apiService.getImageRecordsByURL(this.previousPageURL).then((page) => {
      //     this.imageRecords = page.data;
      //     this.nextPageURL = page.nextlink;
      //     this.previousPageURL = page.prevlink;
      //     this.loading = false;
      //   });
      //
      // },
      selectImageRecord(imageRecord){
        this.selectedImageRecord = imageRecord;
      }
    },
    mounted() {

      this.getImageRecords();

    },
  }
</script>
<style scoped>
  .list-horizontal li {
    display:inline-block;
  }
  .list-horizontal li:before {
    content: '\00a0\2022\00a0\00a0';
    color:#999;
    color:rgba(0,0,0,0.5);
    font-size:11px;
  }
  .list-horizontal li:first-child:before {
    content: '';
  }
</style>
