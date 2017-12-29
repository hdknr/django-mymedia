<template>
<b-container fluid>

    <b-row>
      <b-col class="mediafile-view p-1 border border-primary">
        <div v-if="Boolean(value.data)">
          <b-img fluid :src="image_url"></b-img>

          <input type="file" name="uploadingFile"
            ref="uploadingFile"
            v-if="isUploaderReady"
            :disabled="isSaving"
            @change="filesChange($event.target.name, $event.target.files); fileCount = $event.target.files.length"
            accept="image/*">
          </input>
        </div>
      </b-col>
    </b-row>

    <b-row class="pt-1">
      <b-col cols="12" v-if="Boolean(value.data)">

        <b-list-group flush>

          <b-list-group-item v-if="uploadingFile">
            <b-alert show dismissible variant="primary" @dismissed="reset">
              <i class="fa fa-file-image-o" aria-hidden="true"></i>
              {{ uploadingFile.name }}
              <b-btn size="sm" @click="upload">Update</b-btn>
            </b-alert>
          </b-list-group-item>

          <b-list-group-item>
            <b-button-toolbar aria-label="Toolbar with button groups and dropdown menu">
               <b-button-group class="mx-1" size="sm">
                 <b-btn
                  :variant="switchVariant(null)"
                  @click="setCurrentImage(null)">画像</b-btn>
               </b-button-group>
               <b-button-group class="mx-1" size="sm" v-if="mediafile.thumbnails">
                 <b-btn
                    :key="data.id"
                    :variant="switchVariant(name)"
                    @click="setCurrentImage(name)"
                    v-for="(data, name, index) in mediafile.thumbnails">{{ name }}</b-btn>
                </b-button-group>
             </b-button-toolbar>
          </b-list-group-item>


          <b-list-group-item>
            <h4 class="alert-heading">
              <mymedia-text v-model="value.title"> </mymedia-text>
            </h4>
          </b-list-group-item>

          <b-list-group-item>
            ID={{ value.id }}: {{ value.filename}}
          </b-list-group-item>

          <b-list-group-item>
            <mymedia-tags v-model="value.tags"> </mymedia-tags>
          </b-list-group-item>

          <b-list-group-item>
            <b-button size="sm" @click="save">Update</b-button>
          </b-list-group-item>


        </b-list-group flush>

      </b-col>
    </b-row>

</b-container>

</template>

<style>
.mediafile-view {
  align-items:center;
  display:flex;
  height:300px; width:300px;
}
.mediafile-view .img-fluid {
  margin:0 auto;      // horizontal centering
  width:auto; height:auto;
  max-width:100%; max-height:100%;
}

.mediafile-view input[type='file']{
   line-height: 0px;
   //z-index: 1;
   opacity: 0;
   border: none;
   border-radius: 3px;
   background: grey;
   position: absolute;
   left: 0px; top: 0px;
   width: 100%; height: 100%;
}
</style>

<script>
import Vue from 'vue'
import Text from 'mymedia/bv/Text'
import Tags from 'mymedia/bv/Tags'

export default {
    props: ['value'],
    components: {'mymedia-text': Text, 'mymedia-tags': Tags},
    data(){
      return{
        'nail':  null,
        'isSaving': false,
        'isUploaderReady': true,
        'uploadingFile': null
      }
    },
    computed: {
      mediafile(){
        return this.value;
      },
      backgound_image(){
          return 'url("' + this.image_url + '")'
      },
      image_url(){
        if(Boolean(this.value.data)) {
          if(this.nail && this.nail in this.mediafile.thumbnails )
            return this.mediafile.thumbnails[this.nail].data;
          return this.mediafile.data;
        }
      }
    },
    watch: {
        mediafile: function(val){
            Vue.nextTick(()=>{ this.reset();});
        }
    },
    methods: {
      reset() {
        if(this.mediafile.thumbnails && !(this.nail in this.mediafile.thumbnails)){
          Vue.set(this, 'nail', null);
        }
        Vue.set(this, 'uploadingFile', null);
        Vue.set(this, 'isUploaderReady', false);
        this.$nextTick(()=> { Vue.set(this, 'isUploaderReady', true)});
      },
      setCurrentImage(nail){
          this.nail = nail;
          this.reset();
      },
      switchVariant(name){
          return (name == this.nail) ? "primary" : "outline-primary";
      },
      filesChange(fieldName, fileList) {
        if (!fileList.length) return;
        var vm = this;
        Array
          .from(Array(fileList.length).keys())
          .map(x => {vm.uploadingFile = fileList[x];});
      },
      uploadMediaFile(){
        var formData = new FormData();
        if(this.uploadingFile){
          formData.append('data', this.uploadingFile, this.uploadingFile.name);
        }
        formData.append('title', this.value.title);
        formData.append('tags', JSON.stringify(this.value.tags));
        formData.append('access', this.value.access);
        return this.$root.upload('imagefile-list', formData, this.value);
      },

      uploadThumbnailFile(){
        var thumbnail = this.value.thumbnails[this.nail];
        var formData = new FormData();
        formData.append('data', this.uploadingFile, this.uploadingFile.name);
        formData.append('profile_name', this.nail);
        formData.append('image', this.value.id);
        return this.$root.upload('thumbnail-list', formData, thumbnail);
      },

      save(){
        var vm = this;
        this.uploadMediaFile().then((res) => {
          res.data.thumbnails = vm.mediafile.thumbnails;
          vm.$emit('input', this.value);
          vm.$emit('on-mediafile-updated', res.data);
        });
      },
      upload(){
        var vm = this;
        if(this.nail){
          if(this.uploadingFile)
            this.uploadThumbnailFile().then((res) =>{
              vm.mediafile.thumbnails[this.nail] = res.data;
              vm.reset();
            });
        }else{
            this.save();
        }
      }
    }
};
</script>
