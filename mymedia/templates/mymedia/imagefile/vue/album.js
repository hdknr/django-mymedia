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
  watch:{
      value: function(newValue, oldValue){
          console.log("newvalue", newValue.mediafiles.length)
      }
  },
  computed:{
    main_cols(){return this.show_meta ? 8: 12;},
    meta_cols(){return this.show_meta ? 4: 0;},
  },
  created(){
      this.value.current = this.value.mediafiles[0];
  },
  methods: {
     on_dragstart(position,e) {this.drag = position;},
     on_dragenter(position, e){this.dragenter = position; },
     on_drop(e) {
        this.value.mediafiles.splice(
          this.dragenter, 0,
          this.value.mediafiles.splice(this.drag, 1)[0]);
        this.$emit('input', this.value); },

     selectFile(index){
        Vue.set(this.value, 'current', this.value.mediafiles[index]);
        this.$forceUpdate();      // to make highlight the selected one
      },

     removeFile(index){
       this.value.mediafiles.splice(index, 1);
       if(this.value.mediafiles.length < 1)
          Vue.set(this.value, 'current', null);
       this.$emit('input', this.value);
     },

     addFiles(mediafiles){
      Array.prototype.push.apply(
        this.value.mediafiles, mediafiles);
      this.$emit('input', this.value);
      this.$forceUpdate();      // to make highlight the selected one
      },

      onImageSelected(mediafile, selected){
        if(selected == true){
          this.value.mediafiles.push(mediafile);
          this.$emit('input', this.value);
          this.$forceUpdate();      // to make highlight the selected one
        }
      },

     replaceCurrentMediaFile(item){
       var i = this.value.mediafiles.findIndex(el => el.id === item.id);
       Vue.set(this.value, 'current', item);
       this.value.mediafiles[i] = item;
       this.$forceUpdate();
     }
  }
});
