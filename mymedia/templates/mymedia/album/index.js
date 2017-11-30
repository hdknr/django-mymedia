var app = new Vue({
  el: '#app',
  components: {
    'mymedia-gallery': Gallery,
    'mymedia-album': AlbumComponent
  },
  data:{
    current_album: null,
    csrftoken: '{{ token }}',
    endpoint: "{% url 'mymedia_api:album-list' %}",
    albums: []
  },
  created(){
    this.refreshData();
  },
  computed: {
  },
  methods:  {
      refreshData(){
        var vm = this;
        return axios.get(vm.endpoint).then((res) => {
          try{
            Vue.set(vm, 'albums',res.data.results);
          }catch(e){
          }
        });
      },
      get_endpoint(album){
          if(album.id){
              return this.endpoint  + album.id + '/';
          }
          return this.endpoint;
      },
      getRef(prefix, value){
          return prefix + "-" + value;
      },
      editTitle(album, index){
        album.edit = true;
        this.$forceUpdate();
      },
      saveTitle(album, index){
        album.edit = false;
        this.$forceUpdate();
      },
      showGallery(album){
        this.current_album = album;
        this.$refs.gallery.$refs.dialog.show();
      },
      updateAlbum(album){
        var url = this.get_endpoint(album);
        var vm = this;
        var config = {};
        axios.defaults.xsrfCookieName = 'csrftoken';
        axios.defaults.xsrfHeaderName = 'X-CSRFToken';
        var method = album.id ? 'patch': 'post';
        return axios[method](url, album, config).then((res) =>{
            vm.albums[vm.albums.indexOf(album)] = res.data;
            Vue.set(vm, 'albums', Object.assign([], vm.albums));
            vm.$forceUpdate();
        });
      },
      deleteAlbum(album){
        var vm = this;
        if(album.id){
          var url = vm.get_endpoint(album);
          var config = {};
          axios.defaults.xsrfCookieName = 'csrftoken';
          axios.defaults.xsrfHeaderName = 'X-CSRFToken';
          return axios.delete(url, album, config).then((res) =>{
              vm.albums = vm.albums.filter(e =>{
                  return e.id != album.id;
              });
          });
        }else{
          console.log(vm.albums);
          vm.albums = vm.albums.filter(e =>{
              return e.id;
          });
        }
      },
      addAlbum(){
          this.albums.splice(0, 0, {title: 'New', mediafiles:[]});
          Vue.set(this, 'albums', Object.assign([], this.albums));
      },
      onShowUploader(image){
        if(image){
          this.$refs.uploader.setOriginal(image);
        }
        this.$refs.uploader.$refs.dialog.show();
      },
      onImageSelected(image, selected){
        if( this.current_album){
          if(selected == true){
              this.current_album.mediafiles = this.current_album.mediafiles.concat([image]);
          }
        }
      }
  }

});
