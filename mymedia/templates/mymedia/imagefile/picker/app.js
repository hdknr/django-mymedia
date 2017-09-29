{% load staticfiles %}
Vue.options.delimiters = ['{[{', '}]}'];        // Django テンプレートとバッティングしないように変更
Vue.component('gallery-thumbnail',{ props: ['image', 'index'], template: '#gallery-thumbnail-template'});
Vue.component('gallery-carousel',{ props: ['image', 'index'], template: '#gallery-carousel-template'});
Vue.component('gallery-uploader',
  {props: [],
   data: function(){return {
      names: {title: '', filename: ''},
      image: null
   }},
   methods: {
      resetForm(){
          Vue.set(this, 'image', null);
          Vue.set(this, 'names', {title: '', filename: ''});
          $("#upload-form input").val('');
          $("#imagefile-uploader").modal('hide');
      },
      uploadImage(){
          var config = {headers: {'content-type': 'multipart/form-data'}};
          var data = new FormData($("#upload-form").get(0));
          var tags = data.get('tags');
          if(tags)    // tags must be JSON list
              data.set('tags', JSON.stringify(tags.split(',').map((i)=>i.trim())))
          var vm = this;
          axios.post("{% url 'mymedia_api:imagefile-list' %}", data, config)
            .then(function(res) { vm.resetForm(); })
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
            Vue.set(vm, 'image', null);
            Vue.set(vm, 'names', {title:'', filename:''});
            $("#upload-form")[0].reset();
        }
      }, "#imagefile-uploader");
   },
   template: '#gallery-uploader-template'}
);

var app = new Vue({
  el: '#app',
  data: {
      message: 'Hello',
      pages: [],
      images: {}
  },
  methods:  {
      firstCarousel(){
          jQuery('#myCarousel').carousel(0);
      },
      get_images_page: function(p){
        var url = "{% url 'mymedia_api:imagefile-list' %}?format=json&page=" + p;
        return this.get_images(url);
      },
      get_images: function(url){
        return axios.get(url).then((res) =>{
            Vue.set(this, 'pages', _.range(1, 1 + res.data.count / 16));
            Vue.set(this, 'images', res.data);
            this.firstCarousel();
            this.$emit('GET_AJAX_COMPLETE');
        });
      },
      select_image: function(){
        $('#imagefile-picker').modal('hide');
      }
  }
});

app.get_images_page(1);
