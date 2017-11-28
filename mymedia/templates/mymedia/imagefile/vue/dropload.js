const STATUS_INITIAL = 0, STATUS_SAVING = 1, STATUS_SUCCESS = 2, STATUS_FAILED = 3;

function endpoinMediaFile(id){
  if(id) return "{% url 'mymedia_api:imagefile-detail' pk='___' %}".replace('___', id);
  else return "{% url 'mymedia_api:imagefile-list' %}";
}

function uploadMediaFile(formData, mediafile_id){
    var endpoint = endpoinMediaFile(mediafile_id);
    var method = (mediafile_id) ? 'patch' : 'post';
    var config = {headers: {'content-type': 'multipart/form-data'}};
    axios.defaults.xsrfCookieName = 'csrftoken';
    axios.defaults.xsrfHeaderName = 'X-CSRFToken';
    return axios[method](endpoint, formData, config);
}

var DroploadComponent = Vue.extend({
  template: '#mymedia-dropload-template',
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
          this.$emit('on-mediafile-uploaed', x.data);
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
