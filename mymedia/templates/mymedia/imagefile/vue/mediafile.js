{% load staticfiles %}
var MediaFileComponent = Vue.extend({
    props: ['value'], template: '#imagefile-mediafile-template',
    components: {
        'mymedia-text': TextComponent
    },
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
      mediafile(){
        return this.value;
      },
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
        console.log('update...', this.value);
        var formData = new FormData();
        if(this.uploadingFile){
          formData.append('data', this.uploadingFile, this.uploadingFile.name);
        }
        formData.append('title', this.value.title);
        //formData.append('filename', this.value.filename.toLowerCase());
        formData.append('tags', JSON.stringify(this.value.tags));
        formData.append('access', this.value.access);
        return this.sendMediaFile(this.value.id, formData);
      },
      uploadThumbnailFile(){
        var thumbnail = this.value.thumbnails[this.nail];
        var formData = new FormData();
        formData.append('data', this.uploadingFile, this.uploadingFile.name);
        formData.append('profile_name', this.nail);
        formData.append('image', this.value.id);
        return this.sendThumbnail(thumbnail.id, formData);
      },
      save(){
        var vm = this;
        this.uploadMediaFile().then((res) => {
          res.data.thumbnails = vm.mediafile.thumbnails;
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
});
