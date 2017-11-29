{% load staticfiles %}
var MediaFileComponent = Vue.extend({
    props: ['mediafile'], template: '#imagefile-mediafile-template',
    mixins: [apiMixin],
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
        if(this.nail && this.nail in this.mediafile.thumbnails )
          return this.mediafile.thumbnails[this.nail].data;
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
        var formData = new FormData();
        if(this.uploadingFile){
          formData.append('data', this.uploadingFile, this.uploadingFile.name);
        }
        formData.append('title', this.mediafile.title);
        formData.append('filename', this.mediafile.filename);
        formData.append('tags', JSON.stringify(this.mediafile.tags));
        formData.append('access', this.mediafile.access);
        return this.sendMediaFile(this.mediafile.id, formData);
      },
      uploadThumbnailFile(){
        var thumbnail = this.mediafile.thumbnails[this.nail];
        var formData = new FormData();
        formData.append('data', this.uploadingFile, this.uploadingFile.name);
        formData.append('profile_name', this.nail);
        formData.append('image', this.mediafile.id);
        return this.sendThumbnail(thumbnail.id, formData);
      },
      upload(){
        var vm = this;
        if(this.nail){
          if(this.uploadingFile)
            this.uploadThumbnailFile().then((res) =>{
              this.mediafile.thumbnails[this.nail] = res.data; });
        }else{
            this.uploadMediaFile().then((res) => {
              res.data.thumbnails = vm.mediafile.thumbnails;
              Vue.set(vm, 'mediafile', res.data);
              this.$emit('on-mediafile-updated', res.data);
            });
        }
      }
    }
});
