{% load staticfiles %}
Vue.options.delimiters = ['{[{', '}]}'];        // Django テンプレートとバッティングしないように変更

var Thumbnail = Vue.extend({
    props: ['image', 'index'], template: '#gallery-thumbnail-template',
});
var Carousel = Vue.extend({
    props: ['image', 'index'], template: '#gallery-carousel-template',
});
var Selection = Vue.extend({
    props: ['image', 'index'], template: '#gallery-selection-template',
});

var Uploader = Vue.extend({
   props: [], template: '#gallery-uploader-template',
   mounted(){
     var vm = this;
     $("#imagefile-uploader")
      .off('hidden.bs.modal')
      .on('hidden.bs.modal', function(){
          Vue.set(vm, 'instance',  null);
          Vue.set(vm, 'image', null);
          Vue.set(vm, 'tags', '');
          Vue.set(vm, 'names', {title: '', filename: ''});
          $("#upload-form input").val('');
      });
   },
   data: function(){return {
      instance: null,
      names: {title: '', filename: ''},
      tags: '',
      access: '',
      image: null
   }},
   computed: {
      endpoint: function(){
          if(this.instance){
            return "{% url 'mymedia_api:imagefile-detail' pk='___' %}".replace('___', this.instance.id); }
          else {return "{% url 'mymedia_api:imagefile-list' %}"; }
      }
   },
   methods: {
      editForm(instance){
          Vue.set(this, 'instance', instance);
          this.names.title = instance.title;
          this.names.filename = instance.filename;
          this.tags = instance.tags;
          this.access = instance.access;
          $("#imagefile-uploader").modal('show');
      },
      resetForm(created){
          $("#imagefile-uploader").modal('hide');
          var p = created ? 1 : null;   // null := current
          this.$emit('on-reset-form', p);
      },
      uploadImage(){
          var vm = this;
          var config = {headers: {'content-type': 'multipart/form-data'}};
          var data = new FormData($("#upload-form").get(0));
          var tags = data.get('tags');
          if(tags)    // tags must be JSON list
              data.set('tags', JSON.stringify(tags.split(',').map((i)=>i.trim())))
          var file_data = data.getAll("data");
          if(file_data && file_data[0].size < 1){
              data.delete('data');
          }
          axios.defaults.xsrfCookieName = 'csrftoken';
          axios.defaults.xsrfHeaderName = 'X-CSRFToken';
          var method = vm.instance ? 'patch' : 'post';
          axios[method](vm.endpoint, data, config)
            .then(function(res) {
                vm.instance = null;
                vm.resetForm(false); })
            .catch(function(error) {
                console.log(error.response); });
      },
      createImage(file) {
         var image = new Image();
         var vm = this;
         var reader = new FileReader();
         reader.onload = function(e) {
            var img = {
                thumbnail: e.target.result, uploadFile: file, name: file.name};
             Vue.set(vm, 'image', img);
         };
         reader.readAsDataURL(file);
      },
      onFileChanged(e){
          var files = e.target.files || e.dataTransfer.files;
          this.createImage(files[0]);
          let params = new URLSearchParams();
          params.append('csrfmiddlewaretoken', $('input[name="csrfmiddlewaretoken"]').val());
          params.append('filename',  files[0].name);
          return axios.post("{% url 'mymedia_api:filenames' %}", params)
            .then((res)=>{ Vue.set(this, 'names', res.data); });
      }
   },
});

var Picker = Vue.extend({
  template: '#gallery-picker-template',
  data: function(){
    return {
      selected_list: {},        // selected MediaFiles
      max_selection:1,
      //instance: null,
      images: {}
    };
  },
  components: {
   'gallery-uploader': Uploader,
   'gallery-thumbnail': Thumbnail,
   'gallery-carousel': Carousel,
   'gallery-selection': Selection
  },
  computed: {
      has_results(){
          return this.images.results != null && this.images.results.length > 0;
      },
      last_page : function(){
          return this.images.page_range[this.images.page_range.length - 1]
      }
  },
  methods:  {
      resetPicker(max_selection){
          Vue.set(this, 'max_selection',
            (max_selection == undefined) ? 1 : this.max_selection = max_selection);
          Vue.set(this, 'selected_list', {});
          this.get_images_page(1);
      },
      page_url(page){
        if (page == null || page == undefined)
          page = this.images.current_page == undefined ? 1: this.images.current_page;
        return "{% url 'mymedia_api:imagefile-list' %}?format=json&page=" + page;
      },
      buttonClass(i){
          return this.images.current_page == i ? 'btn-primary' : 'btn-default';
      },
      firstCarousel(){
          jQuery('#myCarousel').carousel(0);
      },
      get_next_page(p) {
          return this.get_images_page(this.images.current_page + p);
      },
      get_images_page(page){
        if (page == null || page == undefined) page = this.images.current_page;
        else if (page < 0) page = 1;
        return this.get_images(this.page_url(page));
      },
      get_images: function(url){
        var vm  = this;
        return axios.get(url).then((res) =>{
            res.data.results.forEach(function(val){
              val.selected =  val.id in vm.selected_list;
            });
            Vue.set(this, 'images', res.data);
            this.firstCarousel();
            // this.$emit('GET_AJAX_COMPLETE');
        });
      },
      edit_image: function(image_id){
          // Edit existing MediaFile(image_id) with Uploader
          var url = "{% url 'mymedia_api:imagefile-detail' pk='___' %}".replace('___', image_id);
          var vm = this;
          return axios.get(url).then((res) =>{
              // Vue.set(vm, 'instance', res.data);
              this.$refs.gallery_uploader.editForm(res.data);
              //this.$emit('GET_AJAX_COMPLETE');
          });
      },
      select_image: function(image){
        if(image.selected){
          var clone = Object.assign({}, image);
          this.selected_list[image.id] = clone;
        }else { // unselected
          delete this.selected_list[image.id];
          this.images.results.filter(
            function(e, i, a){return (e.id == image.id);})
              .map(function(e, i, a){e.selected = false;});
        }
        Vue.set(this, 'selected_list', Object.assign({}, this.selected_list));
        if(Object.keys(this.selected_list).length >= this.max_selection){
            console.log(this.selected_list);
            $('#imagefile-picker').modal('hide');
        }
      }
  }
});


var Slide = Vue.extend({
  template: '#gallery-slide-template',
  data: function(){
    return {
      visible: false,
      callback: function(){},
      mediafiles: [],
      drag: null,
      dragenter: null
    };
  },
  methods: {
     on_dragstart(mediafile,e) {
       Vue.set(this, 'drag', mediafile); },

     on_dragenter(mediafile, e){
       Vue.set(this, 'dragenter', mediafile); },

     on_drop(e) {
       this.mediafiles.splice(
         this.dragenter, 0,
         this.mediafiles.splice(this.drag, 1)[0]);
       this.callback(); },

    removeFile(index){
        this.mediafiles.splice(index, 1);
        this.callback(); },

    showSlide(mediafiles, callback){
        Vue.set(this, 'visible', true);
        Vue.set(this, 'mediafiles', mediafiles);
        if(callback) Vue.set(this, 'callback', callback); },

    addFiles(mediafiles){
        var arr = this.mediafiles.concat(mediafiles);
        Vue.set(this, 'mediafiles', arr);
        this.callback(); }
  }
});

var app = new Vue({
  el: '#app',
  components: {
      'gallery-slide': Slide,
      'gallery-picker': Picker
  },
  computed: {
      selected_list(){
          return   this.$refs.picker.selected_list;
      }
  },
  methods:  {
      getValues(){
          return Object.values(this.$refs.picker.selected_list);
      },
      openSlide(mediafiles, callback){
        this.$refs.slide.showSlide(mediafiles, callback);
      },
      openPicker(count){
        $("#imagefile-picker").modal();
        this.$refs.picker.resetPicker(count);
      }
  }
});
// {#  app.get_images_page(1); #}
