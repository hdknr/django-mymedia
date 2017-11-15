var Slide = Vue.extend({
  template: '#imagefile-slide-template',
  props: ['modalState'],
  data: function(){
    return {
      callback: function(){},
      mediafiles: [],
      drag: null, dragenter: null
    };
  },
  methods: {
      showSlide(mediafiles, callback){
        this.modalState = true;
        this.mediafiles = mediafiles;
        if(callback) Vue.set(this, 'callback', callback); },
     on_dragstart(mediafile,e) {this.drag = mediafile; },
     on_dragenter(mediafile, e){this.dragenter = mediafile; },
     on_drop(e) {
       this.mediafiles.splice(
         this.dragenter, 0,
         this.mediafiles.splice(this.drag, 1)[0]);
       this.callback(); },

    removeFile(index){
        this.mediafiles.splice(index, 1);
        this.callback(); },

    addFiles(mediafiles){
        var arr = this.mediafiles.concat(mediafiles);
        this.mediafiles = arr;
        this.callback(); }
  }
});
