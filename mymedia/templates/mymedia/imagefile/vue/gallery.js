{% load staticfiles %}
var Gallery = Vue.extend({
    props: [], template: '#imagefile-gallery-template',
    components: {
      'mymedia-dropload': DroploadComponent
    },
    data(){
        return{
            hideGate: false,
            current: null,
            selected_list: {},
            response: null,
            images: []
        }
    },
    mounted(){
        this.getNextPage();
    },
    computed: {
       endpoint(){
           return "{% url 'mymedia_api:imagefile-list' %}";
       }
    },
    methods: {
      setId(prefix, id){
        return prefix + "-" + id;
      },
      onShow(){
          this.images.forEach(function(i){i.selected = false;});
      },
      onHiding(evt){
        if(this.hideGate){
            evt.preventDefault();
            this.hideGate = false;
        }
      },
      onMediafileUpload(mediafile){
        this.$emit('on-select', mediafile, true);
      },
      onEditImage(image, evt){
        console.log("onEditImage......");
        //this.hideGate = true;
        // this.$emit('on-upload', image);
      },
      getPageUrl(page){
        if (page == null || page == undefined)
          page = this.response.current_page == undefined ? 1: this.response.current_page + 1;
        else if (page < 0 ) page = 1;
        return "{% url 'mymedia_api:imagefile-list' %}?format=json&page=" + page;
      },
      getImagesPage(page){
          return this.getImages(this.getPageUrl(page));
      },
      getNextPageUrl(){
        if(this.response == null){
          return "{% url 'mymedia_api:imagefile-list' %}?format=json&page=1";
        }
        return this.response.next;
      },
      getNextPage(){
        this.getImages(this.getNextPageUrl());
      },
      getImages(url){
        if(url == null || url == undefined) return;
        var vm  = this;
        return axios.get(url).then((res) =>{
            res.data.results.forEach(function(val){
              val.selected =  val.id in vm.selected_list;
            });
            vm.response = res.data;
            vm.images = vm.images.concat(vm.response.results)
        });
      },
      onScrolled(ev){
        if ((event.target.scrollLeft + event.target.offsetWidth) >= event.target.scrollWidth) {
            this.getNextPage();
        }
      }
    }
});
