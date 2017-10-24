{% load staticfiles %}
Vue.options.delimiters = ['{[{', '}]}'];        // Django テンプレートとバッティングしないように変更
Vue.component('gallery-thumbnail',{ props: ['image', 'index'], template: '#gallery-thumbnail-template'});
Vue.component('gallery-carousel',{
    props: ['image', 'index'],
    mounted(){},
    template: '#gallery-carousel-template'
});
Vue.component('gallery-uploader', {
   props: ['instance'],
   data: function(){return {
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
      resetForm(created){
          Vue.set(this, 'image', null);
          Vue.set(this, 'names', {title: '', filename: ''});
          $("#upload-form input").val('');
          $("#imagefile-uploader").modal('hide');
          var p = created ? 1 : null;   // null := current
          this.$emit('on-reset-form', p);
      },
      uploadImage(){
          var config = {headers: {'content-type': 'multipart/form-data'}};
          var data = new FormData($("#upload-form").get(0));
          var tags = data.get('tags');
          if(tags)    // tags must be JSON list
              data.set('tags', JSON.stringify(tags.split(',').map((i)=>i.trim())))
          var vm = this;

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
                thumnail: e.target.result, uploadFile: file, name: file.name};
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
   mounted(){
     var vm = this;
     $("#app").on({
        'shown.bs.modal': function(){
            if(vm.instance){
                Vue.set(vm, 'names', {title: vm.instance.title, filename: vm.instance.filename});
                Vue.set(vm, 'image', {thumnail: vm.instance.data});
                Vue.set(vm, 'tags', vm.instance.tags.join(','));
                Vue.set(vm, 'access', vm.instance.access);
            }
        },
        'hidden.bs.modal': function(){
            Vue.set(vm, 'image', null);
            Vue.set(vm, 'names', {title:'', filename:''});
            $("#upload-form")[0].reset();
            vm.instance = null;
        }
      }, "#imagefile-uploader");
   },
   template: '#gallery-uploader-template'}
);

var app = new Vue({
  el: '#app',
  data: {
      instance: null,
      images: {}
  },
  computed: {
      last_page : function(){
          return this.images.page_range[this.images.page_range.length - 1]
      }
  },
  methods:  {
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
        return axios.get(url).then((res) =>{
            Vue.set(this, 'images', res.data);
            this.firstCarousel();
            this.$emit('GET_AJAX_COMPLETE');
        });
      },
      edit_image: function(image_id){
          var url = "{% url 'mymedia_api:imagefile-detail' pk='___' %}".replace('___', image_id);
          var vm = this;
          return axios.get(url).then((res) =>{
              Vue.set(this, 'instance', res.data);
              $("#imagefile-uploader").modal('show');
              this.$emit('GET_AJAX_COMPLETE');
          });
      },
      select_image: function(){
        // TODO:
        $('#imagefile-picker').modal('hide');
      }
  }
});

app.get_images_page(1);
