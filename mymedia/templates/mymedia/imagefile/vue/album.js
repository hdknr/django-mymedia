var AlbumComponent = Vue.extend({
  template: '#mymedia-album-template',
  props: ['value', 'modalState'],     {# value is bound to Album instance #}
  components: {
    'mymedia-mediafile': MediaFileComponent
  },
  data: function(){
    return {
      current: null,
      drag: null, dragenter: null
    };
  },
  created(){
      Vue.set(this, 'current', this.value.mediafiles[0]);
  },
  methods: {
     on_dragstart(mediafile,e) {this.drag = mediafile; },
     on_dragenter(mediafile, e){this.dragenter = mediafile; },
     on_drop(e) {
       this.value.mediafiles.splice(
         this.value.dragenter, 0,
         this.value.mediafiles.splice(this.drag, 1)[0]); },

     removeFile(index){
       this.value.mediafiles.splice(index, 1); },

     addFiles(mediafiles){
      var arr = this.value.mediafiles.concat(mediafiles);
      this.value.mediafiles = arr; },

     replaceCurrentMediaFile(item){
       var i = this.value.mediafiles.findIndex(el => el.id === item.id);
       Vue.set(this, 'current', item);
       this.value.mediafiles[i] = item;
       this.$forceUpdate();
     }
  }
});
