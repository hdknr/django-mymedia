var imageComponent = Vue.extend({
  template: '#imagefile-image-template',
  props: ['value', ],
  components:{
    'mymedia-text': TextComponent,
    'mymedia-gallery': Gallery,
    'mymedia-mediafile': MediaFileComponent,
    'mymedia-toggle': ToggleComponent,
  },
  data: function(){
    return {show_meta: false};
  },
  computed:{
      main_cols(){ return this.show_meta ?  8: 12; },
      meta_cols(){ return this.show_meta ?  4: 0; },
  },
  methods: {
    onImageSelected(image, selected){
      if(selected == true){
          this.$emit('input', image);
          this.$refs.gallery.$refs.dialog.hide();
      }
    }
  }
});
