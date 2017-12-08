var AlbumComponent = Vue.extend({
  template: '#mymedia-album-template',
  props: ['value', 'modalState'],     {# value is bound to Album instance #}
  components: {
    'mymedia-gallery': Gallery,
    'mymedia-toggle': ToggleComponent,
    'mymedia-mediafile': MediaFileComponent
  },
  data: function(){
    return {
      show_meta: false,
      drag: null, dragenter: null
    };
  },
  computed:{
    main_cols(){return this.show_meta ? 8: 12;},
    meta_cols(){return this.show_meta ? 4: 0;},
  },
  created(){
      this.value.current = this.value.mediafiles[0];
  },
  methods: {
     on_dragstart(mediafile,e) {this.value.drag = mediafile; },
     on_dragenter(mediafile, e){this.value.dragenter = mediafile; },
     on_drop(e) {
        this.value.mediafiles.splice(
          this.value.dragenter, 0,
          this.value.mediafiles.splice(this.value.drag, 1)[0]);
        this.$emit('input', this.value); },

     selectFile(index){
        this.value.current = this.value.mediafiles[index];
        this.$forceUpdate(); },

     removeFile(index){
       this.value.mediafiles.splice(index, 1);
      this.$emit('input', this.value); },

     addFiles(mediafiles){
      var arr = this.value.mediafiles.concat(mediafiles);
      this.value.mediafiles = arr;
      this.$emit('input', this.value); },

      onImageSelected(mediafile, selected){
        if(selected == true){
            this.value.mediafiles = this.value.mediafiles.concat([mediafile]);
            this.$emit('input', this.value); }
      },

     replaceCurrentMediaFile(item){
       var i = this.value.mediafiles.findIndex(el => el.id === item.id);
       Vue.set(this.value, 'current', item);
       this.value.mediafiles[i] = item;
       this.$forceUpdate();
     }
  }
});
