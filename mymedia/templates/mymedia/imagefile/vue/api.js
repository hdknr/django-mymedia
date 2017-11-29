var apiMixin = {
  methods: {
    sendForm(endpoint, method, formData){
        var config = {headers: {'content-type': 'multipart/form-data'}};
        axios.defaults.xsrfCookieName = 'csrftoken';
        axios.defaults.xsrfHeaderName = 'X-CSRFToken';
        return axios[method](endpoint, formData, config);
    },
    sendThumbnail(id, formdata){
      var endpoint = "{% url 'mymedia_api:thumbnail-list' %}";
      var method = 'put';
      if(id){
          method = 'patch';
          endpoint = "{% url 'mymedia_api:thumbnail-detail' pk='___' %}".replace('___', id);
      }
      return this.sendForm(endpoint, method, formdata);
    }
  } {# methods #}
}   {# apiMixin #}
