var TextComponent = Vue.extend({
    props: ['value'], template: '#imagefile-text-template',
    data(){
        return{
            editing: false,
            original: ''
        }
    },
    methods: {
      updateText(ev){
        if(ev.target.value && ev.target.value != this.original){
          this.editing = false;
          this.$emit('input', ev.target.value);
        }
        else{
            this.value = this.orginal;
        }
      }
    }
});
