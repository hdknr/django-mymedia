const STATUS_INITIAL = 0, STATUS_SAVING = 1, STATUS_SUCCESS = 2, STATUS_FAILED = 3;
var DroploadComponent = Vue.extend({
  template: '#mymedia-dropload-template',
  props: ['album'],
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
      uploadMediaFile(formData)
        .then(x => {
          this.album.mediafiles.push(x.data);     // Add to Album
          this.currentStatus = STATUS_INITIAL;
        })
        .catch(err => {
          this.uploadError = err.response;
          this.currentStatus = STATUS_FAILED;
        });
    },
    filesChange(fieldName, fileList) {
      if (!fileList.length) return;
      var vm = this;
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
});
