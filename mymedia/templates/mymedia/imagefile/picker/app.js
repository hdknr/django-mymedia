{% load staticfiles %}
Vue.options.delimiters = ['{[{', '}]}'];        // Django テンプレートとバッティングしないように変更
Vue.component('gallery-thumbnail',{ props: ['image', 'index'], template: '#gallery-thumbnail-template'});
Vue.component('gallery-carousel',{ props: ['image', 'index'], template: '#gallery-carousel-template'});

var app = new Vue({
  el: '#app',
  data: {
      message: 'Hello',
      pages: [],
      images: {}
  },
  methods: {
      get_images_page: function(p){
        var url = "{% url 'mymaeida_api:imagefile-list' %}?format=json&page=" + p;
        return this.get_images(url);
      },
      get_images: function(url){
        return axios.get(url).then((res) =>{
            Vue.set(this, 'pages', _.range(1, 1 + res.data.count / 16));
            Vue.set(this, 'images', res.data);
            this.$emit('GET_AJAX_COMPLETE');
        });
      },
      select_image: function(){
        $('#imagefile-picker').modal('hide');
      }
  }
});

app.get_images_page(1);
