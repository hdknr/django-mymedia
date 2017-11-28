var AlbumComponent = Vue.extend({
  template: '#mymedia-album-template',
  props: ['modalState', 'mediafiles'],

  data: function(){
    return {
      current: null,
      drag: null, dragenter: null
    };
  },
  mounted(){
      this.current = this.mediafiles[0];
  },
  methods: {
     on_dragstart(mediafile,e) {this.drag = mediafile; },
     on_dragenter(mediafile, e){this.dragenter = mediafile; },
     on_drop(e) {
       this.mediafiles.splice(
         this.dragenter, 0,
         this.mediafiles.splice(this.drag, 1)[0]); },

     removeFile(index){
       this.mediafiles.splice(index, 1); },

     addFiles(mediafiles){
      var arr = this.mediafiles.concat(mediafiles);
      this.mediafiles = arr;
    }
  }
});
