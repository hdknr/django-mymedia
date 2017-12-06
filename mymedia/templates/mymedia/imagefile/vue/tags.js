var TagsComponent = Vue.extend({
    props: ['value'], template: '#imagefile-tags-template',
    data(){
        return{
            editing: false,
        }
    },
    methods: {
        popTag(name){
          if(!this.value) this.value = [];
          this.value.splice( this.value.indexOf(name) , 1);
          this.$emit('input', this.value);
        },
        addTag(ev){
          if(!this.value) this.value = [];
          this.value.push(ev.target.value);
          this.editing=false;
          ev.target.value = '';
          this.$emit('input', this.value);
        }
    }
});
