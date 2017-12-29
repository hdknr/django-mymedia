<template>
  <b-modal id="galleryDialog" ref="dialog" size="lg" title="Gallery"
    @hide="onHiding" @show="onShow">

    <b-container fluid class="p-4 bg-dark" style="overflow-x:scroll;white-space: nowrap;" @scroll="onScrolled">
        <b-col v-for="(i, index) in images" :key="i.id">
          <b-img thumbnail :id="setId('thumb', i.id)" fluid
            :src="i.data" alt="Thumbnail" width="100"></b-img>
          <br>

          <b-checkbox
            @change="$emit('on-select', i, !i.selected)"
            v-model="i.selected" :id="setId('image-selector', i.id)">
          </b-checkbox>

          <b-popover :target="setId('thumb', i.id)" triggers="hover focus" >
             <template slot="title">Preview
              <b-img :src="i.data" fluid ></b-img>
            </template>
          </b-popover>

        </b-col>
    </b-container>

    <mymedia-dropload @on-mediafile-uploaed="onMediafileUpload"> </mymedia-dropload>
    <br> <br> <br> <br>

    <div slot="modal-footer" class="w-100">
    </div>

  </b-modal>
</template>

<style>
.popover {min-width: 50em !important; }

#galleryDialog .col{
  display: inline-block; width:auto;
}
</style>


<script>
import Vue from 'vue'
import Dropload from 'mymedia/bv/Dropload.vue';

export default {
    props: [],
    components: {
      'mymedia-dropload': Dropload,
    },
    data(){
        return{
            hideGate: false,
            current: null,
            selected_list: {},
            response: null,
            images: []
        }
    },
    mounted(){
        this.getNextPage();
    },
    computed: {
       endpoint(){
          return this.$root.env.endpoint['imagefile-list'];
       }
    },
    methods: {
      setId(prefix, id){
        return prefix + "-" + id;
      },
      onShow(){
          this.images.forEach(function(i){i.selected = false;});
      },
      onHiding(evt){
        if(this.hideGate){
            evt.preventDefault();
            this.hideGate = false;
        }
      },
      onMediafileUpload(mediafile){
        this.$emit('on-select', mediafile, true);
      },
      getPageUrl(page){
        if (page == null || page == undefined)
          page = this.response.current_page == undefined ? 1: this.response.current_page + 1;
        else if (page < 0 ) page = 1;
        return  this.ednpoint + "?format=json&page=" + page;
      },
      getImagesPage(page){
          return this.getImages(this.getPageUrl(page));
      },
      getNextPageUrl(){
        if(this.response == null){
          return this.endpoint + "?format=json&page=1";
        }
        return this.response.next;
      },
      getNextPage(){
        this.getImages(this.getNextPageUrl());
      },
      getImages(url){
        if(url == null || url == undefined) return;
        var vm  = this;
        return axios.get(url).then((res) =>{
          vm.response = res.data;
          if(res.data.results) {
            res.data.results.forEach(function(val){
              val.selected =  val.id in vm.selected_list;
            });
            Vue.set(vm, 'images', vm.images.concat(vm.response.results));
          }
        });
      },
      onScrolled(ev){
        if ((event.target.scrollLeft + event.target.offsetWidth) >= event.target.scrollWidth) {
            this.getNextPage();
        }
      }
    }
};
</script>
