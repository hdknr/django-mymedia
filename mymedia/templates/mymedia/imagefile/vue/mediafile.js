{% load staticfiles %}
var MediaFileComponent = Vue.extend({
    props: ['mediafile'], template: '#imagefile-mediafile-template',
    data(){
        return{
            'nail':  null,
            'isSaving': false,
            'isUploaderReady': true,
            'uploadingFile': null
        }
    },
    computed: {
      backgound_image(){
          return 'url("' + this.image_url + '")'
      },
      image_url(){
        if(this.nail)
          return this.mediafile.thumbnails[this.nail];
        return this.mediafile.data;
      }
    },
    watch: {
        mediafile: function(val){ this.reset(); }
    },
    methods: {
      setId(prefix, id){
        return prefix + "-" + id;
      },
      reset() {
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

      },
      uploadThumbnailFile(){

      },
      upload(){
        if(self.uploadingFile){
        }
      }
    }
});
