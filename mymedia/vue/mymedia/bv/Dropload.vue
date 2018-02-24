<template>
  <b-container fluid class="dropbox">
    <b-form-file class="input-file"
      multiple :name="uploadFieldName" :disabled="isSaving"
      @change="onChanged($event)" accept="image/*">
   </b-form-file>
    <p v-if="isInitial"> Drag your file(s) here to begin<br> or click to browse </p>
    <p v-if="isSaving"> Uploading {{ fileCount }} files... </p>
  </b-container>
</template>


<style lang="scss">
.dropbox {
  outline: 2px dashed grey; /* the dash box */
  outline-offset: -10px;
  background: lightcyan;
  color: dimgray;
  padding: 10px 10px;
  min-height: 50px; /* minimum height */
  position: relative;
  cursor: pointer;
}

.input-file {
  opacity: 0; /* invisible but it's there! */
  width: 100%;
  height: 50px;
  position: absolute;
  cursor: pointer;
}

.dropbox:hover {
  background: lightblue; /* when mouse over to the drop zone, change color */
}

.dropbox p {
  font-size: 1.2em;
  text-align: center;
  padding: 10px 0;
}
</style>

<script>
const STATUS_INITIAL = 0, STATUS_SAVING = 1, STATUS_SUCCESS = 2, STATUS_FAILED = 3;

export default {
  data: function(){
    return {
      tags: 'Photo',
      uploadedFiles: [],
      uploadError: null,
      currentStatus: null,
      access: 'public',
      uploadFieldName: 'data'
    };
  },
  computed: {
    tags_json(){
      try{
         return JSON.stringify(this.tags.split(',').map((i)=>i.trim()) );
       }catch(e) {
         return '["Photo"]'
       }
     },
    isInitial() { return this.currentStatus === STATUS_INITIAL; },
    isSaving() { return this.currentStatus === STATUS_SAVING; },
    isSuccess() { return this.currentStatus === STATUS_SUCCESS; },
    isFailed() { return this.currentStatus === STATUS_FAILED; }
  },
  methods: {
    reset() {
      // reset form to initial state
      this.currentStatus = STATUS_INITIAL;
      this.uploadedFiles = [];
      this.uploadError = null;
    },
    save(formData) {
      // upload data to the server
      this.$root.upload('imagefile', formData)
        .then(res => {
          this.$emit('on-mediafile-uploaed', res.data);
          this.currentStatus = STATUS_INITIAL;
        })
        .catch(err => {
          this.uploadError = err.response;
          this.currentStatus = STATUS_FAILED;
        });
    },
    onChanged(ev){
      //@change="filesChange($event.target.name, $event.target.files);
      // fileCount = $event.target.files.length"
        this.filesChange(event.target.name, event.target.files);
    },
    filesChange(fieldName, fileList) {
      if (!fileList.length) return;
      for(var i in fileList){
          var item = fileList[i];
          console.log(item);
      }

      Array
        .from(Array(fileList.length).keys())
        .map(x => {
          this.currentStatus = STATUS_SAVING;
          var formData = new FormData();
          formData.append(vm.uploadFieldName, fileList[x], fileList[x].name);
          formData.append('tags', vm.tags_json);
          formData.append('access', vm.access);
          vm.save(formData);
        });
    }
  },
  mounted() {
    this.reset();
  }
};
</script>
